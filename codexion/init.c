/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/13 22:06:34 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/04/13 22:10:57 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int ft_init_hub(t_hub *hub)
{
	t_coder 	*coder;
	t_dongle 	*dongle;
	int			i;

	i = 0;
	dongle = malloc(sizeof(t_dongle) * hub->num_coders);
	coder = malloc(sizeof(t_coder) * hub->num_coders);
	if (!coder || !dongle)
		return (-1);
	
	while (i < hub->num_coders)
	{
		init_coder(&coder[i], i + 1, hub);
		init_dongle(&dongle[i], i + 1,
				hub->dongle_cooldown, -1);
		i++;
	}
	i = 0;
	while (i < hub->num_coders)
	{
		coder[i].hub = hub;
		coder[i].start_time = coder[i].hub->start_time;
		coder[i].last_compile = coder[i].hub->start_time;
		coder[i].right = &dongle[i];
		coder[i].left = &dongle[(i + 1) % hub->num_coders];
		i++;
	}
	i = 0;
	pthread_mutex_init(&hub->print, NULL);
	hub->over = 0;
	//var->coders = coder;
	//var->hub = hub;
	//if (pthread_create(&var->thread, NULL, var_rotine, var) != 0)
	//		return (-1);
	while (i < hub->num_coders)
	{
		coder[i].last_compile = get_time_ms();
		if (pthread_create(&(coder + i)->thread, NULL, coder_rotine, &coder[i]) != 0)
			return (-1);
		i++;
	}
//	i = 0;
  //if (pthread_join(var->thread, NULL) != 0)
	//	return (-1);
	
	return (0);
};

