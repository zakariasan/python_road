/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coders.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/19 13:20:30 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/04/24 20:46:30 by zhaouzan         ###   ########.fr       */
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
	coder->last_compile = hub->start_time;
	coder->right = &hub->dongles[id - 1];
	coder->left = &hub->dongles[(id) % hub->num_coders];
	//pthread_mutex_init(&coder->coder_mutex, NULL);
}

void	*coder_rotine(void *args)
{
	t_coder	*coder;

	coder = (t_coder *)args;
	while (!is_over(coder->hub))
	{
		//requesting the dongles
		req_compile(coder->hub->server, coder);	

		//pthread_mutex_lock(&coder->hub->server->mutex);
		if (coder->allowed)
		{
			coder->last_compile = get_time_ms();
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
			usleep(500);
			coder->counter++;
			coder->deadline = coder->deadline + coder->hub->time_to_burnout;
		}

		//pthread_mutex_unlock(&coder->coder_mutex);
		if (coder->counter >= coder->hub->compiles_required)
			break;
	}
	return (NULL);
}
