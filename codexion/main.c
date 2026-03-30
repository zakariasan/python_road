/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/12 01:38:01 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/03/30 10:01:56 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int ft_codexion(t_hub *hub)
{
	t_coder 	*coder;
	t_dongle 	*dongle;

  	printf("t_hub--->%d", hub->num_coders);
	dongle = malloc(sizeof(t_dongle) * 2);
	coder = malloc(sizeof(t_coder) * 2);
	if (!coder || !dongle)
		return (-1);
	init_coder(coder, 1, 200, 200, 200);
	init_coder(coder + 1, 2, 200, 200, 200);
	init_dongle(dongle, 1, 200, -1);
	init_dongle(dongle + 1, 1, 200, -1);
	coder[0].right = dongle;
	coder[0].left = dongle + 1;
	
	coder[1].right = dongle;
	coder[1].left = dongle + 1;

	coder->start_time = get_time_ms();
	(coder + 1)->start_time = get_time_ms();

	if (pthread_create(&coder->thread, NULL, coder_rotine, coder) != 0)
		return (-1);
	if (pthread_create(&(coder + 1)->thread, NULL, coder_rotine, coder + 1) != 0)
		return (-1);
	if (pthread_join(coder->thread, NULL) != 0)
		return (-1);
	if (pthread_join((coder + 1)->thread, NULL) != 0)
  {
		return (-1);
  }
  pthread_mutex_destroy(&dongle[0].mutex);
  pthread_mutex_destroy(&dongle[1].mutex);
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
