/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongles.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/19 13:25:22 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/06/23 00:00:00 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	init_dongle(t_dongle *d, int id, int cooldown, t_scheduler sched)
{
	d->id = id;
	d->owner = -1;
	d->cooldown = cooldown;
	d->released = get_time_ms() - cooldown;
	d->scheduler = sched;
	d->queue[0].active = 0;
	d->queue[1].active = 0;
	pthread_mutex_init(&d->mutex, NULL);
	pthread_cond_init(&d->cond, NULL);
}

/* Add coder to the dongle's 2-slot queue. */
static void	dq_push(t_dongle *d, t_coder *c)
{
	int	i;

	i = 0;
	while (i < 2)
	{
		if (!d->queue[i].active)
		{
			d->queue[i].coder_id = c->id;
			d->queue[i].arrived = get_time_ms();
			d->queue[i].deadline = c->deadline;
			d->queue[i].active = 1;
			return ;
		}
		i++;
	}
}

/* Remove coder from the dongle's queue. */
static void	dq_pop(t_dongle *d, int coder_id)
{
	int	i;

	i = 0;
	while (i < 2)
	{
		if (d->queue[i].active && d->queue[i].coder_id == coder_id)
		{
			d->queue[i].active = 0;
			return ;
		}
		i++;
	}
}

/*
** Returns the coder_id of the highest-priority waiter:
**   FIFO: lowest arrived timestamp wins.
**   EDF : lowest deadline wins (tie-break: lower coder_id).
** Returns -1 if queue is empty.
*/
static int	dq_best(t_dongle *d)
{
	int		a;
	int		b;
	t_waiter	*wa;
	t_waiter	*wb;

	a = d->queue[0].active;
	b = d->queue[1].active;
	if (!a && !b)
		return (-1);
	if (!a)
		return (d->queue[1].coder_id);
	if (!b)
		return (d->queue[0].coder_id);
	wa = &d->queue[0];
	wb = &d->queue[1];
	if (d->scheduler == FIFO)
	{
		if (wa->arrived <= wb->arrived)
			return (wa->coder_id);
		return (wb->coder_id);
	}
	if (wa->deadline < wb->deadline)
		return (wa->coder_id);
	if (wb->deadline < wa->deadline)
		return (wb->coder_id);
	if (wa->coder_id < wb->coder_id)
		return (wa->coder_id);
	return (wb->coder_id);
}

/*
** Block until this coder is the highest-priority waiter, the dongle is free,
** and the cooldown has elapsed. Uses timedwait when cooldown is the only blocker.
*/
void	dongle_acquire(t_dongle *d, t_coder *c)
{
	long		cooldown_end;
	struct timespec	ts;

	pthread_mutex_lock(&d->mutex);
	dq_push(d, c);
	while (!is_over(c->hub))
	{
		if (d->owner == -1 && dq_best(d) == c->id
			&& get_time_ms() - d->released >= (long)d->cooldown)
		{
			d->owner = c->id;
			dq_pop(d, c->id);
			pthread_mutex_unlock(&d->mutex);
			return ;
		}
		cooldown_end = d->released + d->cooldown;
		if (d->owner == -1 && dq_best(d) == c->id
			&& get_time_ms() < cooldown_end)
		{
			ts.tv_sec = cooldown_end / 1000;
			ts.tv_nsec = (cooldown_end % 1000) * 1000000;
			pthread_cond_timedwait(&d->cond, &d->mutex, &ts);
		}
		else
			pthread_cond_wait(&d->cond, &d->mutex);
	}
	dq_pop(d, c->id);
	pthread_mutex_unlock(&d->mutex);
}

/*
** Release the dongle: mark free, record release time, wake all waiters on
** this dongle so they can re-evaluate their priority.
*/
void	dongle_release(t_dongle *d, t_hub *hub)
{
	(void)hub;
	pthread_mutex_lock(&d->mutex);
	d->owner = -1;
	d->released = get_time_ms();
	pthread_cond_broadcast(&d->cond);
	pthread_mutex_unlock(&d->mutex);
}
