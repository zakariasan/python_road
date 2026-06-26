/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coder_utils.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/24 02:12:55 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/06/24 02:16:14 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	get_order(t_coder *c, t_dongle **first, t_dongle **second)
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

void	release_owned(t_dongle *d, t_coder *c)
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

int	take_dongles(t_coder *c, t_dongle *first, t_dongle *second)
{
	t_hub	*hub;

	hub = c->hub;
	dongle_acquire(first, c);
	if (is_over(hub))
	{
		release_owned(first, c);
		return (-1);
	}
	if (second)
	{
		dongle_acquire(second, c);
		if (is_over(hub))
		{
			dongle_release(first, hub);
			release_owned(second, c);
			return (-1);
		}
	}
	return (0);
}
