/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 22:46:41 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/06/23 22:46:42 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	ft_init_hub(t_hub *hub)
{
	int	i;

	hub->coders = malloc(sizeof(t_coder) * hub->num_coders);
	hub->dongles = malloc(sizeof(t_dongle) * hub->num_coders);
	if (!hub->coders || !hub->dongles)
	{
		free(hub->coders);
		free(hub->dongles);
		return (-1);
	}
	hub->over = 0;
	hub->start_time = get_time_ms();
	i = 0;
	while (i < hub->num_coders)
	{
		init_dongle(&hub->dongles[i], i + 1, hub->dongle_cooldown,
			hub->scheduler);
		i++;
	}
	i = 0;
	while (i < hub->num_coders)
	{
		init_coder(&hub->coders[i], i + 1, hub);
		i++;
	}
	pthread_mutex_init(&hub->over_mutex, NULL);
	pthread_cond_init(&hub->over_cond, NULL);
	pthread_mutex_init(&hub->print_mutex, NULL);
	return (0);
}
