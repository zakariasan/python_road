/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/13 22:06:34 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/04/26 21:29:18 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	ft_init_server(t_hub *hub)
{
	t_server	*srv;

	hub->server = malloc(sizeof(t_server));
	if (!hub->server)
		return (-1);
	srv = hub->server;
	hub->server->scheduler = hub->scheduler;
	srv->coders = hub->coders;
	srv->list_heap = NULL;
	srv->heap_size = 0;
	pthread_mutex_init(&srv->mutex, NULL);
	pthread_cond_init(&srv->list_cond, NULL);
	return (0);
}

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
	hub->over = 0;
	while (i < hub->num_coders)
	{
		init_coder(&coder[i], i + 1, hub);
		init_dongle(&dongle[i], i + 1, hub->dongle_cooldown, -1);
		i++;
	}
	pthread_mutex_init(&hub->over_mutex, NULL);
	pthread_mutex_init(&hub->print_mutex, NULL);
	if (ft_init_server(hub) != 0)
		return (-1);
	return (0);
}

t_req	*ft_create_item(t_req *req)
{
	t_req	*tmp;

	tmp = malloc(sizeof(t_req));
	if (!tmp)
		return (NULL);
	tmp->coder_id = req->coder_id;
	tmp->deathline = req->deathline;
	tmp->time = req->time;
	tmp->next = NULL;
	return (tmp);
}
