/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/12 01:38:01 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/03/14 13:07:23 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/time.h>

void init_coder(t_coder *coder,int id, long compile, long debug, long refactor)
{
	coder->time_to_compile = compile;
	coder->time_to_debug = debug;
	coder->time_to_refactor = refactor;
	coder->id = id;
	coder->right = NULL;
	coder->left = NULL;
}

void init_dongle(t_dongle *dongle, int id, long cooldown, int owner)
{
	dongle->id = id;
	dongle->d_cooldown = cooldown;
	dongle->owner = owner;
}

long long	get_time_ms(void)
{
	struct timeval	tv;

	gettimeofday(&tv, NULL);
	return (long long)((tv.tv_sec * 1000) + (tv.tv_usec / 1000));
}

void	loging(int coder_id, long long start_time, char *action)
{
	long long	now;
 
	now = get_time_ms() - start_time;
	printf("%lld %d %s\n", now, coder_id, action);
}

void take_dongle(t_dongle *dongle, t_coder *coder, long long time)
{
	long long	time_used;

	time_used = get_time_ms() - dongle->released;
	if (dongle->owner == -1 && time_used >= dongle->d_cooldown)
	{
		dongle->owner = coder->id;
		loging(coder->id, time, "has taken a dongle");
		return;
	}
}

void	release_dongle(t_dongle *dongle)
{
	dongle->owner = -1;
	dongle->released = get_time_ms();
}

void	*coder_rotine(void *args)
{
	t_coder	*coder;

	coder = (t_coder *)args;
	take_dongle(coder->left, coder, coder->start_time);
	take_dongle(coder->right, coder, coder->start_time);
	if (coder->left->owner == coder->id && coder->right->owner == coder->id)
	{
		loging(coder->id, coder->start_time, "is compiling");
		usleep(coder->time_to_compile * 1000);
		release_dongle(coder->left);
		release_dongle(coder->right);
		loging(coder->id, coder->start_time, "is debugging");
		usleep(coder->time_to_debug * 1000);
		loging(coder->id, coder->start_time, "is refactoring");
		usleep(coder->time_to_refactor * 1000);
		
	}
	return (NULL);
}

int main()
{
	t_coder 	*coder;
	t_dongle 	*dongle;

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
		return (-1);
	return (0);
};

