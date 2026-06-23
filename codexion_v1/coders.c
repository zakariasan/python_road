/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coders.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/19 13:20:30 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/06/23 00:00:00 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	init_coder(t_coder *coder, int id, t_hub *hub)
{
	coder->id = id;
	coder->counter = 0;
	coder->hub = hub;
	coder->last_compile = hub->start_time;
	coder->deadline = hub->start_time + hub->time_to_burnout;
	coder->right = &hub->dongles[id - 1];
	coder->left = &hub->dongles[id % hub->num_coders];
}

/*
** Always acquire the lower-id dongle first (resource ordering).
** This breaks the circular wait condition and prevents deadlock.
*/
static void	get_order(t_coder *c, t_dongle **first, t_dongle **second)
{
	if (c->left == c->right)
	{
		*first = c->left;
		*second = NULL;
	}
	else if (c->left->id < c->right->id)
	{
		*first = c->left;
		*second = c->right;
	}
	else
	{
		*first = c->right;
		*second = c->left;
	}
}

/*
** If simulation ended while we held a dongle, release it so other
** threads can unblock and terminate cleanly.
*/
static void	release_owned(t_dongle *d, t_coder *c)
{
	if (!d)
		return ;
	pthread_mutex_lock(&d->mutex);
	if (d->owner == c->id)
	{
		d->owner = -1;
		d->released = get_time_ms();
		pthread_cond_broadcast(&d->cond);
	}
	pthread_mutex_unlock(&d->mutex);
}

void	*coder_routine(void *args)
{
	t_coder		*coder;
	t_hub		*hub;
	t_dongle	*first;
	t_dongle	*second;

	coder = (t_coder *)args;
	hub = coder->hub;
	get_order(coder, &first, &second);
	while (!is_over(hub))
	{
		dongle_acquire(first, coder);
		if (is_over(hub))
		{
			release_owned(first, coder);
			return (NULL);
		}
		if (second)
		{
			dongle_acquire(second, coder);
			if (is_over(hub))
			{
				dongle_release(first, hub);
				release_owned(second, coder);
				return (NULL);
			}
		}
		coder->last_compile = get_time_ms();
		pthread_mutex_lock(&hub->over_mutex);
		coder->deadline = coder->last_compile + hub->time_to_burnout;
		coder->counter++;
		pthread_cond_signal(&hub->over_cond);
		pthread_mutex_unlock(&hub->over_mutex);
		loging(coder, "has taken a dongle");
		if (second)
			loging(coder, "has taken a dongle");
		loging(coder, "is compiling");
		usleep(hub->time_to_compile * 1000);
		dongle_release(first, hub);
		if (second)
			dongle_release(second, hub);
		loging(coder, "is debugging");
		usleep(hub->time_to_debug * 1000);
		loging(coder, "is refactoring");
		usleep(hub->time_to_refactor * 1000);
	}
	return (NULL);
}
