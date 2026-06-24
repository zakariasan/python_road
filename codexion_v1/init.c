/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 22:46:41 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/06/24 03:30:10 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	queue_free(t_dongle *d)
{
	free(d->queue);
	d->queue = NULL;
	d->q_size = 0;
}

static void	destroy_dongles(t_hub *hub, int n)
{
	int	i;

	i = 0;
	while (i < n)
	{
		pthread_mutex_destroy(&hub->dongles[i].mutex);
		pthread_cond_destroy(&hub->dongles[i].cond);
		queue_free(&hub->dongles[i]);
		i++;
	}
}

int	ft_init_hub(t_hub *hub)
{
	int	i;

	hub->coders = malloc(sizeof(t_coder) * hub->num_coders);
	hub->dongles = malloc(sizeof(t_dongle) * hub->num_coders);
	if (!hub->coders || !hub->dongles)
		return (free(hub->coders), free(hub->dongles), -1);
	hub->over = 0;
	hub->start_time = get_time_ms();
	i = -1;
	while (++i < hub->num_coders)
	{
		if (init_dongle(&hub->dongles[i], i + 1, hub->dongle_cooldown,
				hub->scheduler) != 0)
		{
			destroy_dongles(hub, i);
			return (free(hub->coders), free(hub->dongles), -1);
		}
	}
	i = -1;
	while (++i < hub->num_coders)
		init_coder(&hub->coders[i], i + 1, hub);
	pthread_mutex_init(&hub->over_mutex, NULL);
	pthread_cond_init(&hub->over_cond, NULL);
	pthread_mutex_init(&hub->print_mutex, NULL);
	return (0);
}
