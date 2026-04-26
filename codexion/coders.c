/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coders.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/19 13:20:30 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/04/26 20:54:53 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"
#include <pthread.h>

void	init_coder(t_coder *coder, int id, t_hub *hub)
{
	coder->id = id;
	coder->counter = 0;
	coder->right = NULL;
	coder->left = NULL;
	coder->deadline = hub->start_time + hub->time_to_burnout;
	coder->hub = hub;
	coder->last_compile = get_time_ms();
	coder->right = &hub->dongles[id - 1];
	coder->left = &hub->dongles[(id) % hub->num_coders];
}

void	*coder_rotine(void *args)
{
	t_coder	*coder;

	coder = (t_coder *)args;
	//if (coder->id % 2 == 0)
	//	usleep(10);
	while (!is_over(coder->hub))
	{
		req_compile(coder->hub->server, coder);	
		coder->last_compile = get_time_ms();
		coder->deadline = coder->last_compile + coder->hub->time_to_burnout;
		loging(coder, "has taken a dongle");
		loging(coder, "has taken a dongle");
		loging(coder, "is compiling");
		usleep(coder->hub->time_to_compile * 1000);
		release_dongle(coder->left, coder->hub);
		release_dongle(coder->right, coder->hub);
		
		loging(coder, "is debugging");
		usleep(coder->hub->time_to_debug * 1000);
		loging(coder, "is refactoring");
		usleep(coder->hub->time_to_refactor * 1000);
		///usleep(500);
		coder->counter++;

		//pthread_mutex_unlock(&coder->coder_mutex);
		//if (coder->counter >= coder->hub->compiles_required)
		//	break;
	}
	return (NULL);
}
