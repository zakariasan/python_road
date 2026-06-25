/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parser.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/13 21:34:44 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/06/25 15:48:56 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	ft_get_values(char **av, t_hub *hub)
{
	hub->num_coders = atoi(av[1]);
	hub->time_to_burnout = atoi(av[2]);
	hub->time_to_compile = atoi(av[3]);
	hub->time_to_debug = atoi(av[4]);
	hub->time_to_refactor = atoi(av[5]);
	hub->compiles_required = atoi(av[6]);
	hub->dongle_cooldown = atoi(av[7]);
	if (strcmp(av[8], "edf") == 0)
		hub->scheduler = EDF;
	else
		hub->scheduler = FIFO;
}

static int	is_number(char *s)
{
	int	i;

	i = 0;
	if (!s || !s[0])
		return (0);
	while (s[i])
	{
		if (s[i] < '0' || s[i] > '9')
			return (0);
		i++;
	}
	return (1);
}

static int	ft_check_params(int ac, char **av)
{
	int	i;

	i = 1;
	while (i < ac - 1)
	{
		if (i == 1 && atoi(av[i]) == 0)
		{
			fprintf(stderr, "Error: No coder [%s]\n", av[i]);
			return (-1);
		}
		if (!is_number(av[i]) || atoi(av[i]) < 0)
		{
			fprintf(stderr, "Error: invalid argument [%s]\n", av[i]);
			return (-1);
		}
		i++;
	}
	if (strcmp(av[i], "fifo") != 0 && strcmp(av[i], "edf") != 0)
	{
		fprintf(stderr, "Error: scheduler must be 'fifo' or 'edf'\n");
		return (-1);
	}
	return (EXIT_SUCCESS);
}

int	ft_parser(int ac, char **av, t_hub *hub)
{
	if (ac != 9)
	{
		fprintf(stderr, "Usage: ./codexion num_coders time_to_burnout"
			" time_to_compile time_to_debug time_to_refactor"
			" compiles_required dongle_cooldown scheduler\n");
		return (-1);
	}
	if (ft_check_params(ac, av) != 0)
		return (EXIT_FAILURE);
	ft_get_values(av, hub);
	return (EXIT_SUCCESS);
}
