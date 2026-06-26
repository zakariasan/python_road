/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 00:00:00 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/06/23 00:00:00 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	is_over(t_hub *hub)
{
	int	res;

	pthread_mutex_lock(&hub->over_mutex);
	res = hub->over;
	pthread_mutex_unlock(&hub->over_mutex);
	return (res);
}

void	set_over(t_hub *hub)
{
	pthread_mutex_lock(&hub->over_mutex);
	hub->over = 1;
	pthread_cond_broadcast(&hub->over_cond);
	pthread_mutex_unlock(&hub->over_mutex);
}

/*
** Lock order rule: over_mutex must NEVER be held when locking dongle->mutex.
** wake_all_dongles is always called AFTER releasing over_mutex.
*/
void	wake_all_dongles(t_hub *hub)
{
	int	i;

	i = 0;
	while (i < hub->num_coders)
	{
		pthread_mutex_lock(&hub->dongles[i].mutex);
		pthread_cond_broadcast(&hub->dongles[i].cond);
		pthread_mutex_unlock(&hub->dongles[i].mutex);
		i++;
	}
}

static long	earliest_deadline(t_hub *hub)
{
	long	min;
	int		i;

	min = hub->coders[0].deadline;
	i = 1;
	while (i < hub->num_coders)
	{
		if (hub->coders[i].deadline < min)
			min = hub->coders[i].deadline;
		i++;
	}
	return (min);
}

static int	all_done(t_hub *hub)
{
	int	i;

	i = 0;
	while (i < hub->num_coders)
	{
		if (hub->coders[i].counter < hub->compiles_required)
			return (0);
		i++;
	}
	return (1);
}

/*
** Monitor uses timedwait set to the nearest burnout deadline.
** A coder signals over_cond after each compile so the monitor recalculates.
**
** Lock discipline: over_mutex is RELEASED before any call to wake_all_dongles
** or loging() to avoid inversion with dongle->mutex (coders hold dongle->mutex
** while calling is_over() which acquires over_mutex).
*/
void	*monitor_routine(void *args)
{
	t_hub		*hub;
	long		min_dl;
	long		now;
	int			i;
	struct timespec	ts;
	t_coder		*burned;

	hub = (t_hub *)args;
	pthread_mutex_lock(&hub->over_mutex);
	while (!hub->over)
	{
		if (all_done(hub))
		{
			hub->over = 1;
			break ;
		}
		min_dl = earliest_deadline(hub);
		ts.tv_sec = min_dl / 1000;
		ts.tv_nsec = (min_dl % 1000) * 1000000;
		pthread_cond_timedwait(&hub->over_cond, &hub->over_mutex, &ts);
		if (hub->over)
			break ;
		now = get_time_ms();
		burned = NULL;
		i = 0;
		while (i < hub->num_coders)
		{
			if (now >= hub->coders[i].deadline)
			{
				burned = &hub->coders[i];
				hub->over = 1;
				break ;
			}
			i++;
		}
		if (burned)
		{
			pthread_mutex_unlock(&hub->over_mutex);
			loging(burned, "burned out");
			wake_all_dongles(hub);
			return (NULL);
		}
	}
	pthread_mutex_unlock(&hub->over_mutex);
	wake_all_dongles(hub);
	return (NULL);
}
