/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_req.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/26 21:14:32 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/04/26 21:25:26 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	is_possible(t_coder *coder, t_hub *hub)
{
	long	now;

	if (coder->left == coder->right)
		return (0);
	now = get_time_ms();
	if (coder->left->owner != -1
		|| now - coder->left->released
		< hub->dongle_cooldown)
	{
		return (0);
	}
	if (coder->right->owner != -1
		|| now - coder->right->released
		< hub->dongle_cooldown)
		return (0);
	return (1);
}

t_req	*ft_edf(t_req *tmp, t_req *item, t_server *srv)
{
	t_req	*prev;

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
			prev->next = tmp;
			tmp->next = item;
			return (srv->list_heap);
		}
		prev = item;
		item = item->next;
	}
	prev->next = tmp;
	return (srv->list_heap);
}

t_req	*ft_push(t_server *srv, t_req *req)
{
	t_req	*tmp;
	t_req	*item;

	item = srv->list_heap;
	tmp = ft_create_item(req);
	srv->heap_size++;
	if (!item)
	{
		srv->list_heap = tmp;
	}
	else if (srv->scheduler == FIFO)
	{
		while (item->next)
			item = item->next;
		item->next = tmp;
	}
	else if (srv->scheduler == EDF)
		return (ft_edf(tmp, item, srv));
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
