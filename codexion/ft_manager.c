/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_manager.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/19 13:27:13 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/04/24 20:16:26 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

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
	pthread_mutex_unlock(&hub->over_mutex);
}

void	*manager_rotine(void *args)
{
	t_manager	*manager;
	int			i;
	int			w_done;

	manager = (t_manager *)args;
	while (!is_over(manager->hub))
	{
		i = 0;
		w_done = 1;
		while (i < manager->hub->num_coders)
		{
			if (manager->coders[i].counter < manager->hub->compiles_required)
				w_done = 0;
			i++;
		}
		i = 0;
		if (w_done)
		{
			set_over(manager->hub);
			while (i < manager->hub->num_coders)
				pthread_cond_broadcast(&manager->hub->dongles[i++].cond);
			pthread_mutex_lock(&manager->hub->server->mutex);
			pthread_cond_broadcast(&manager->hub->server->list_cond);
			pthread_mutex_unlock(&manager->hub->server->mutex);
			return (NULL);
		}
		while (i < manager->hub->num_coders)
		{
			if (get_time_ms() - manager->coders[i].last_compile
				> manager->hub->time_to_burnout)
			{
				loging(&manager->coders[i], "burned out");
				set_over(manager->hub);
				i = 0;
				while (i < manager->hub->num_coders)
					pthread_cond_broadcast(&manager->hub->dongles[i++].cond);
				pthread_mutex_lock(&manager->hub->server->mutex);
				pthread_cond_broadcast(&manager->hub->server->list_cond);
				pthread_mutex_unlock(&manager->hub->server->mutex);
				return (NULL);
			}
			i++;
		}
	}
	return (NULL);
}
