#include "codexion.h"

void init_dongle(t_dongle *dongle, int id, long cooldown, int owner)
{
	dongle->id = id;
	dongle->d_cooldown = cooldown;
	dongle->owner = owner;
	pthread_mutex_init(&dongle->mutex, NULL);
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

	now = get_time_ms();
	pthread_mutex_lock(&left->mutex);
	if (left->owner != -1 || now - left->released < left->d_cooldown)
	{
		pthread_mutex_unlock(&left->mutex);
		return (0);
	}
	pthread_mutex_lock(&right->mutex);
	if (right->owner != -1 || now - right->released < right->d_cooldown)
	{
		pthread_mutex_unlock(&left->mutex);
		pthread_mutex_unlock(&right->mutex);
		return (0);
	}
	left->owner = coder->id;
	right->owner = coder->id;
	pthread_mutex_unlock(&left->mutex);
	pthread_mutex_unlock(&right->mutex);
	loging(coder->id, time, "has taken a dongle");
	loging(coder->id, time, "has taken a dongle");
	return(1);
}

void	release_dongle(t_dongle *dongle)
{
	pthread_mutex_lock(&dongle->mutex);
	dongle->owner = -1;
	dongle->released = get_time_ms();
	pthread_mutex_unlock(&dongle->mutex);
}
