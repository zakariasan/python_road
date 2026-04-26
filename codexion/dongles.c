/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongles.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/19 13:25:22 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/04/26 17:14:53 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	init_dongle(t_dongle *dongle, int id, long cooldown, int owner)
{
	dongle->id = id;
	dongle->cooldown = cooldown;
	dongle->owner = owner;
	dongle->released = get_time_ms() - cooldown;
}


void	release_dongle(t_dongle *dongle, t_hub *hub)
{
	pthread_mutex_lock(&hub->server->mutex);
	dongle->owner = -1;
	dongle->released = get_time_ms();
	pthread_cond_broadcast(&hub->server->list_cond);
	pthread_mutex_unlock(&hub->server->mutex);

//	pthread_mutex_lock(&hub->server->mutex);
//	pthread_cond_broadcast(&hub->server->list_cond);
//	pthread_mutex_unlock(&hub->server->mutex);
}
