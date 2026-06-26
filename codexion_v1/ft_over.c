/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_over.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/19 13:08:59 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/06/26 22:24:23 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	ft_over(t_hub *hub)
{
	int	i;

	if (pthread_join(hub->monitor, NULL) != 0)
		return (-1);
	i = -1;
	while (++i < hub->num_coders)
	{
		if (pthread_join(hub->coders[i].thread, NULL) != 0)
		{
			set_over(hub);
			return (-1);
		}
	}
	destroy_hub(hub);
	return (0);
}

int	is_over(t_hub *hub)
{
	int	res;

	pthread_mutex_lock(&hub->over_mutex);
	res = hub->over;
	pthread_mutex_unlock(&hub->over_mutex);
	return (res);
}

void	set_over(t_hub *hub)
{
	pthread_mutex_lock(&hub->over_mutex);
	hub->over = 1;
	pthread_cond_broadcast(&hub->over_cond);
	pthread_mutex_unlock(&hub->over_mutex);
}

int	all_done(t_hub *hub)
{
	int	i;
	int	done;

	i = 0;
	done = 1;
	pthread_mutex_lock(&hub->over_mutex);
	while (i < hub->num_coders)
	{
		if (hub->coders[i].counter < hub->compiles_required)
		{
			done = 0;
			break ;
		}
		i++;
	}
	pthread_mutex_unlock(&hub->over_mutex);
	return (done);
}
