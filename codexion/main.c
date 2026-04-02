/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/12 01:38:01 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/04/02 22:33:37 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"
#include <pthread.h>

int ft_codexion(t_hub *hub)
{
	t_coder 	*coder;
	t_dongle 	*dongle;
	int			i;

	i = 0;
	dongle = malloc(sizeof(t_dongle) * hub->num_coders);
	coder = malloc(sizeof(t_coder) * hub->num_coders);
	if (!coder || !dongle)
		return (-1);
	while (i < hub->num_coders)
	{
		init_coder(&coder[i], i + 1,
				hub->time_to_compile,
				hub->time_to_debug,
				hub->time_to_refactor);
		init_dongle(&dongle[i], i + 1,
				hub->dongle_cooldown, -1);
		i++;
	}
	while (--i >= 0)
	{
		coder[i].right = &dongle[i];
		coder[i].left = &dongle[(i + 1) % hub->num_coders];
	}
	while (++i < hub->num_coders)
	{
		if (pthread_create(&(coder + i)->thread, NULL, coder_rotine, &coder[i]) != 0)
			return (-1);
	}
	while (--i >= 0)
	{
		if (pthread_join(coder->thread, NULL) != 0)
			return (-1);
	}
	while (++i < hub->num_coders)
	{
		pthread_mutex_destroy(&dongle[i].mutex);
	}
	free(dongle);
	free(coder);
	return (0);
};

int main(int ac, char **av)
{
  t_hub hub;

  if (ft_parser(ac, av, &hub) != 0)
    return (-1);
  ft_codexion(&hub);
  return (0);
}
