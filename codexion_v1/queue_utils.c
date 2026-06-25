/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   queue_utils.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/24 05:34:49 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/06/24 05:56:31 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	dq_push(t_dongle *d, t_coder *c)
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

void	dq_pop(t_dongle *d, int coder_id)
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

static int	winner(t_scheduler sched, t_waiter *wa, t_waiter *wb)
{
	if (sched == FIFO)
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

int	dq_best(t_dongle *d)
{
	int			a;
	int			b;

	a = d->queue[0].active;
	b = d->queue[1].active;
	if (!a && !b)
		return (-1);
	if (!a)
		return (d->queue[1].coder_id);
	if (!b)
		return (d->queue[0].coder_id);
	return (winner(d->scheduler, &d->queue[0], &d->queue[1]));
}
