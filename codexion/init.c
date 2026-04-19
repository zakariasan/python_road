/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/13 22:06:34 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/04/19 14:27:52 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	ft_init_hub(t_hub *hub)
{
	t_coder		*coder;
	t_dongle	*dongle;
	int			i;

	i = 0;
	dongle = malloc(sizeof(t_dongle) * hub->num_coders);
	coder = malloc(sizeof(t_coder) * hub->num_coders);
	if (!coder || !dongle)
		return (-1);
	hub->dongles = dongle;
	hub->coders = coder;
	hub->start_time = get_time_ms();
	while (i < hub->num_coders)
	{
		init_coder(&coder[i], i + 1, hub);
		init_dongle(&dongle[i], i + 1, hub->dongle_cooldown, -1);
		i++;
	}
	i = 0;
	while (i < hub->num_coders)
	{
		coder[i].last_compile = hub->start_time;
		coder[i].right = &dongle[i];
		coder[i].left = &dongle[(i + 1) % hub->num_coders];
		i++;
	}
	hub->over = 0;
	pthread_mutex_init(&hub->over_mutex, NULL);
	pthread_mutex_init(&hub->print_mutex, NULL);
	return (0);
};
