/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coders.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/24 02:05:29 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/06/26 20:34:50 by zhaouzan         ###   ########.fr       */
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

static void	compile_time(t_coder *c, t_hub *hub)
{
	pthread_mutex_lock(&hub->over_mutex);
	c->last_compile = get_time_ms() + hub->time_to_compile;
	c->deadline = c->last_compile + hub->time_to_burnout;
	c->counter++;
	pthread_mutex_unlock(&hub->over_mutex);
}

static void	work_time(t_coder *c, t_hub *hub, t_dongle *first, t_dongle *second)
{
	loging(c, "has taken a dongle");
	if (second)
		loging(c, "has taken a dongle");
	loging(c, "is compiling");
	u_sleep(hub, hub->time_to_compile);
	dongle_release(first, hub);
	if (second)
		dongle_release(second, hub);
	loging(c, "is debugging");
	u_sleep(hub, hub->time_to_debug);
	loging(c, "is refactoring");
	u_sleep(hub, hub->time_to_refactor);
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
	if (!second)
	{
		pthread_mutex_lock(&hub->over_mutex);
		while (!hub->over)
			pthread_cond_wait(&hub->over_cond, &hub->over_mutex);
		pthread_mutex_unlock(&hub->over_mutex);
		return (NULL);
	}
	while (!is_over(hub))
	{
		if (take_dongles(coder, first, second) != 0)
			return (NULL);
		compile_time(coder, hub);
		work_time(coder, hub, first, second);
	}
	return (NULL);
}
