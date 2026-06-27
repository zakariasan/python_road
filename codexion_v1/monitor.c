/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/24 00:22:29 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/06/27 00:00:00 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

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

static t_coder	*find_burned(t_hub *hub)
{
	long	now;
	int		i;

	now = get_time_ms();
	i = 0;
	while (i < hub->num_coders)
	{
		if (now > hub->coders[i].deadline)
			return (&hub->coders[i]);
		i++;
	}
	return (NULL);
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

static void	wait_deadline(t_hub *hub)
{
	struct timespec	ts;
	long			min;
	int				i;

	min = hub->coders[0].deadline;
	i = 1;
	while (i < hub->num_coders)
	{
		if (hub->coders[i].deadline < min)
			min = hub->coders[i].deadline;
		i++;
	}
	ts.tv_sec = min / 1000;
	ts.tv_nsec = (min % 1000) * 1000000;
	pthread_cond_timedwait(&hub->over_cond, &hub->over_mutex, &ts);
}

void	*monitor_routine(void *args)
{
	t_hub	*hub;
	t_coder	*burned;

	hub = (t_hub *)args;
	burned = NULL;
	pthread_mutex_lock(&hub->over_mutex);
	while (!hub->over)
	{
		burned = find_burned(hub);
		if (burned || all_done(hub))
		{
			hub->over = 1;
			pthread_cond_broadcast(&hub->over_cond);
			break ;
		}
		wait_deadline(hub);
	}
	pthread_mutex_unlock(&hub->over_mutex);
	if (burned)
		loging(burned, "burned out");
	wake_all_dongles(hub);
	return (NULL);
}
