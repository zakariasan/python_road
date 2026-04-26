/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_server.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/19 17:46:23 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/04/26 21:28:00 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

t_coder	*ft_get_coder(int id, t_hub *hub)
{
	int		i;

	i = 0;
	while (i < hub->num_coders)
	{
		if (id == hub->coders[i].id)
			return (&hub->coders[i]);
		i++;
	}
	return (NULL);
}

t_req	*ft_remove(t_req *req, t_req *prev, t_server *srv)
{
	t_req	*tmp;

	tmp = req->next;
	if (!prev)
		srv->list_heap = tmp;
	else
		prev->next = tmp;
	srv->heap_size--;
	free(req);
	return (tmp);
}

void	ft_grant_if_possible(t_server *srv, t_hub *hub)
{
	t_coder	*coder;
	t_req	*req;
	t_req	*prev;

	req = srv->list_heap;
	prev = NULL;
	while (req)
	{
		coder = ft_get_coder(req->coder_id, hub);
		if (coder && is_possible(coder, hub) == 1)
		{
			coder->left->owner = coder->id;
			coder->right->owner = coder->id;
			coder->allowed = 1;
			pthread_cond_broadcast(&srv->list_cond);
			req = ft_remove(req, prev, srv);
			prev = NULL;
			req = srv->list_heap;
			continue ;
		}
		prev = req;
		req = req->next;
	}
}

void	*ft_server_routine(void *args)
{
	t_hub		*hub;
	t_server	*srv;

	hub = (t_hub *)args;
	srv = hub->server;
	pthread_mutex_lock(&srv->mutex);
	while (!is_over(hub))
	{
		while (srv->heap_size == 0 && !is_over(hub))
			pthread_cond_wait(&srv->list_cond, &srv->mutex);
		if (is_over(hub))
			break ;
		ft_grant_if_possible(srv, hub);
		if (srv->heap_size > 0 && !is_over(hub))
		{
			pthread_mutex_unlock(&srv->mutex);
			usleep(hub->dongle_cooldown * 1000);
			pthread_mutex_lock(&srv->mutex);
		}
	}
	pthread_cond_broadcast(&srv->list_cond);
	pthread_mutex_unlock(&srv->mutex);
	return (NULL);
}
