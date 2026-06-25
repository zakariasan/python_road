/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/24 00:22:29 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/06/25 19:19:22 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"
#include <unistd.h>

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
	t_coder	*burned;
	long	now;
	int		i;

	now = get_time_ms();
	burned = NULL;
	i = 0;
	pthread_mutex_lock(&hub->over_mutex);
	while (i < hub->num_coders)
	{
		if (now >= hub->coders[i].deadline)
		{
			burned = &hub->coders[i];
			break ;
		}
		i++;
	}
	pthread_mutex_unlock(&hub->over_mutex);
	return (burned);
}

void	*monitor_routine(void *args)
{
	t_hub		*hub;
	t_coder		*burned;

	hub = (t_hub *)args;
	burned = NULL;
	while (!is_over(hub))
	{
		if (all_done(hub))
			return (set_over(hub), wake_all_dongles(hub), NULL);
		burned = find_burned(hub);
		if (burned)
			return (set_over(hub), wake_all_dongles(hub),
				loging(burned, "burned out"), NULL);
		usleep(1000);
	}
	wake_all_dongles(hub);
	return (NULL);
}
