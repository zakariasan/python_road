/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/13 22:06:34 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/04/23 00:29:49 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"
#include <pthread.h>
#include <stdlib.h>

int	ft_init_server(t_server *srv, t_hub *hub)
{
	srv->coders = hub->coders;	
	srv->list_heap = malloc(sizeof(t_req) * hub->num_coders);
	if(!srv->list_heap)
		return (-1);
	pthread_mutex_init(&srv->mutex, NULL);
	pthread_cond_init(&srv->list_cond, NULL);
	return (0);
}

void	*ft_server_routine(void *args)
{

}

t_req	*ft_push(t_server *srv, t_req *req)
{
	return req;
}
void	req_compile(t_server *srv, t_coder *coder)
{
	t_req	req;

	req.coder_id = coder->id;
	req.time = get_time_ms();
	coder->allowed = 0;

	pthread_mutex_lock(&srv->mutex);

	ft_push(srv, &req);
	pthread_cond_broadcast(&srv->list_cond);
	while (!coder->allowed && !is_over(coder->hub))
		pthread_cond_wait(&srv->list_cond, &srv->mutex);
	pthread_mutex_unlock(&srv->mutex);
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
	while (i < hub->num_coders)
	{
		init_coder(&coder[i], i + 1, hub);
		init_dongle(&dongle[i], i + 1, hub->dongle_cooldown, -1);
		i++;
	}
	hub->over = 0;
	pthread_mutex_init(&hub->over_mutex, NULL);
	pthread_mutex_init(&hub->print_mutex, NULL);
	return (0);
};
