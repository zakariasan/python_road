/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_over.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/19 13:08:59 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/04/26 21:30:13 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	ft_over(t_hub *hub, t_manager manager)
{
	int	i;

	i = 0;
	if (pthread_join(manager.thread, NULL) != 0)
		return (-1);
	if (pthread_join(hub->server->thread, NULL) != 0)
		return (-1);
	i = 0;
	while (i < hub->num_coders)
	{
		if (pthread_join(hub->coders[i].thread, NULL) != 0)
		{
			set_over(hub);
			return (-1);
		}
		i++;
	}
	pthread_mutex_destroy(&hub->server->mutex);
	pthread_cond_destroy(&hub->server->list_cond);
	pthread_mutex_destroy(&hub->over_mutex);
	pthread_mutex_destroy(&hub->print_mutex);
	free(hub->server->list_heap);
	free(hub->server);
	free(hub->dongles);
	free(hub->coders);
	return (0);
}
