/* ************************************************************************** */
/*																			  */
/*														  :::	   ::::::::   */
/*	 main.c												:+:		 :+:	:+:   */
/*													  +:+ +:+		  +:+	  */
/*	 By: zhaouzan <marvin@42.fr>					+#+  +:+	   +#+		  */
/*												  +#+#+#+#+#+	+#+			  */
/*	 Created: 2026/03/12 01:38:01 by zhaouzan		   #+#	  #+#			  */
/*	 Updated: 2026/04/19 12:46:52 by zhaouzan		  ###	########.fr		  */
/*																			  */
/* ************************************************************************** */

#include "codexion.h"
#include <pthread.h>

int	ft_codexion(t_hub *hub)
{
	t_coder		*coder;
	//t_dongle	*dongle;
	t_manager	manager;
	int			i;

	i = 0;
	coder = hub->coders;
	//dongle = hub->dongles;
	manager.coders = coder;
	manager.hub = hub;
	if (pthread_create(&manager.thread
			, NULL, manager_rotine, &manager) != 0)
		return (-1);
		
//	printf("server ptr: %p\n", (void *)hub->server);
	if (pthread_create(&hub->server->thread ,NULL, ft_server_routine, hub) != 0)
		return (-1);
	while (i < hub->num_coders)
	{
		if (pthread_create(&(coder + i)->thread
				, NULL, coder_rotine, &coder[i]) != 0)
			return (-1);
		i++;
	}
	ft_over(hub, manager);
	return (0);
}

int	main(int ac, char **av)
{
	t_hub	hub;

	if (ft_parser(ac, av, &hub) != 0)
		return (-1);
	if (ft_init_hub(&hub) != 0)
		return (-1);
	if (ft_codexion(&hub) != 0)
		return(-1);
	return (0);
}
