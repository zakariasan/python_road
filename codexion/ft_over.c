/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_over.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/19 13:08:59 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/04/24 18:46:51 by zhaouzan         ###   ########.fr       */
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
	i = 0;
	while (i < hub->num_coders)
	{
		pthread_mutex_destroy(&hub->dongles[i].mutex);
		pthread_cond_destroy(&hub->dongles[i].cond);
		i++;
	}
	free(hub->dongles);
	free(hub->coders);
	return (0);
}
