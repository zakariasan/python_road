#include "codexion.h"
#include <bits/pthreadtypes.h>
#include <pthread.h>

void init_dongle(t_dongle *dongle, int id, long cooldown, int owner)
{
	dongle->id = id;
	dongle->d_cooldown = cooldown;
	dongle->owner = owner;
	pthread_mutex_init(&dongle->mutex, NULL);
	pthread_cond_init(&dongle->cond, NULL);
}

void take_dongle(t_dongle *dongle, t_coder *coder, long long time)
{
	long long	time_used;

	pthread_mutex_lock(&dongle->mutex);
	time_used = get_time_ms() - dongle->released;
	if (dongle->owner == -1 && time_used >= dongle->d_cooldown)
	{
		dongle->owner = coder->id;
		pthread_mutex_unlock(&dongle->mutex);
		loging(coder->id, time, "has taken a dongle");
		return;
	}
	pthread_mutex_unlock(&dongle->mutex);
}

int take_dongles(t_dongle *left, t_dongle *right, t_coder *coder, long long time)
{
	long long	now;

	while(1)
	{
		if (coder->hub->over)
			return(0);
	now = get_time_ms();
	pthread_mutex_lock(&left->mutex);
	while (left->owner != -1 || now - left->released < left->d_cooldown || coder->hub->over)
	{
		if (coder->hub->over)
		{
			pthread_mutex_unlock(&left->mutex);
			return (0);
		}
		pthread_cond_wait(&left->cond, &left->mutex);
	}
	if (coder->hub->over)
	{
		pthread_mutex_unlock(&left->mutex);
		return (0);
	}

	left->owner = coder->id;

	pthread_mutex_unlock(&left->mutex);
	//  right one time 
	pthread_mutex_lock(&right->mutex);
	now = get_time_ms();
	if (right->owner == -1 && now - right->released >= right->d_cooldown && !coder->hub->over)
	{
		right->owner = coder->id;
		pthread_mutex_unlock(&right->mutex);
		loging(coder->id, time, "has taken a dongle");
		loging(coder->id, time, "has taken a dongle");
		return (1);
	}
	pthread_mutex_unlock(&right->mutex);
	release_dongle(left);
	return(1);
	}
}

void	release_dongle(t_dongle *dongle)
{
	pthread_mutex_lock(&dongle->mutex);
	dongle->owner = -1;
	dongle->released = get_time_ms();
	pthread_cond_broadcast(&dongle->cond);
	pthread_mutex_unlock(&dongle->mutex);
}
