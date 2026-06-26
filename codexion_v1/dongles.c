/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongles.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/24 05:25:12 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/06/25 19:06:43 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	init_dongle(t_dongle *d, int id, int cooldown, t_scheduler sched)
{
	t_waiter	*q;

	q = malloc(sizeof(t_waiter) * 2);
	if (!q)
		return (-1);
	d->queue = q;
	d->q_size = 0;
	d->id = id;
	d->owner = -1;
	d->cooldown = cooldown;
	d->released = get_time_ms() - cooldown;
	d->scheduler = sched;
	d->queue[1].active = 0;
	d->queue[0].active = 0;
	pthread_mutex_init(&d->mutex, NULL);
	pthread_cond_init(&d->cond, NULL);
	return (0);
}

int	my_turn(t_dongle *d, int id)
{
	return (d->owner == -1 && dq_best(d) == id);
}

static void	wait_cooldown(t_dongle *d)
{
	long			cooldown_end;
	struct timespec	ts;

	cooldown_end = d->released + d->cooldown;
	ts.tv_sec = cooldown_end / 1000;
	ts.tv_nsec = (cooldown_end % 1000) * 1000000;
	pthread_cond_timedwait(&d->cond, &d->mutex, &ts);
}

void	dongle_acquire(t_dongle *d, t_coder *c)
{
	pthread_mutex_lock(&d->mutex);
	dq_push(d, c);
	while (!is_over(c->hub))
	{
		if (my_turn(d, c->id))
		{
			if (get_time_ms() - d->released >= (long)d->cooldown)
			{
				d->owner = c->id;
				dq_pop(d, c->id);
				pthread_mutex_unlock(&d->mutex);
				return ;
			}
			wait_cooldown(d);
		}
		else
			pthread_cond_wait(&d->cond, &d->mutex);
	}
	dq_pop(d, c->id);
	pthread_mutex_unlock(&d->mutex);
}

void	dongle_release(t_dongle *d, t_hub *hub)
{
	(void)hub;
	pthread_mutex_lock(&d->mutex);
	d->owner = -1;
	d->released = get_time_ms();
	pthread_cond_broadcast(&d->cond);
	pthread_mutex_unlock(&d->mutex);
}
