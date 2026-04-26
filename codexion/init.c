/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/13 22:06:34 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/04/26 20:54:36 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"
#include <pthread.h>
#include <stdlib.h>

int	ft_init_server(t_hub *hub)
{
	t_server *srv;
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

t_req *ft_remove(t_req *req, t_req *prev,t_server *srv)
{
	t_req *tmp;

	tmp = req->next;
	if (!prev)
		srv->list_heap = tmp;
	else
		prev->next = tmp;
	srv->heap_size--;
	free(req);
	return (tmp);
}

int	is_possible(t_coder *coder, t_hub *hub)
{
	long	now;

	if (coder->left  == coder->right)
		return (0);
	now = get_time_ms();
	if (coder->left->owner != -1
			|| now - coder->left->released
			< hub->dongle_cooldown)
	{
		return (0);
	}
	if (coder->right->owner != -1 || now - coder->right->released
			< hub->dongle_cooldown)
	{
		return (0);
	}

	return (1);
}

void	ft_grant_if_possible(t_server *srv, t_hub *hub)
{
	t_coder *coder;
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
			req = ft_remove(req, prev,srv);
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
	t_hub	*hub;
	t_server *srv;

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

t_req	*ft_create_item(t_req *req)
{
	t_req *tmp;
	
	tmp = malloc(sizeof(t_req));
	if (!tmp)
		return (NULL);
	tmp->coder_id = req->coder_id;
	tmp->deathline = req->deathline;
	tmp->time = req->time;
	tmp->next = NULL;
	return (tmp);
}

t_req	*ft_push(t_server *srv, t_req *req)
{
	t_req	*tmp;
	t_req	*item;
	t_req	*prev;

	item = srv->list_heap;
	tmp = ft_create_item(req);
	srv->heap_size++;
	if (!item)
	{
		srv->list_heap = tmp;
	}
	else if (srv->scheduler == FIFO)
	{
		while(item->next)
			item = item->next;
		item->next = tmp;
	}
	else if (srv->scheduler == EDF)
	{
		if (tmp->deathline < item->deathline)
		{
			tmp->next = item;
			srv->list_heap = tmp;
			return (tmp);
		}
		prev = item;
		item = item->next;
		while (item->next)
		{
			if (tmp->deathline < item->deathline)
			{
				prev->next =tmp;
				tmp->next = item;
				return (srv->list_heap);
			}
			prev = item;
			item = item->next;
		}
		prev->next = tmp;
	}
	return (req);
}

void	req_compile(t_server *srv, t_coder *coder)
{
	t_req	req;

	req.coder_id = coder->id;
	req.time = get_time_ms();
	req.deathline = coder->deadline;

	pthread_mutex_lock(&srv->mutex);
	coder->allowed = 0;
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
};
