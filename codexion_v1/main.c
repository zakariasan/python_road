/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/12 01:38:01 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/06/23 00:00:00 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	ft_codexion(t_hub *hub)
{
	int	i;

	if (pthread_create(&hub->monitor, NULL, monitor_routine, hub) != 0)
		return (-1);
	i = 0;
	while (i < hub->num_coders)
	{
		if (pthread_create(&hub->coders[i].thread,
				NULL, coder_routine, &hub->coders[i]) != 0)
			return (-1);
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
