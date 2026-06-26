/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/25 15:48:43 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/06/25 15:48:43 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	fail_start(t_hub *hub, int created)
{
	set_over(hub);
	wake_all_dongles(hub);
	pthread_join(hub->monitor, NULL);
	while (created-- > 0)
		pthread_join(hub->coders[created].thread, NULL);
	destroy_hub(hub);
	return (-1);
}

int	ft_codexion(t_hub *hub)
{
	int	i;

	if (pthread_create(&hub->monitor, NULL, monitor_routine, hub) != 0)
		return (destroy_hub(hub), -1);
	i = 0;
	while (i < hub->num_coders)
	{
		if (pthread_create(&hub->coders[i].thread,
				NULL, coder_routine, &hub->coders[i]) != 0)
			return (fail_start(hub, i));
		i++;
	}
	return (ft_over(hub));
}

int	main(int ac, char **av)
{
	t_hub	hub;

	if (ft_parser(ac, av, &hub) != 0)
		return (1);
	if (ft_init_hub(&hub) != 0)
		return (1);
	if (ft_codexion(&hub) != 0)
		return (1);
	return (0);
}
