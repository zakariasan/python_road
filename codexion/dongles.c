#include "codexion.h"
#include <pthread.h>

void init_dongle(t_dongle *dongle, int id, long cooldown, int owner)
{
	dongle->id = id;
	dongle->cooldown = cooldown;
	dongle->owner = owner;
	dongle->released = 0;
	pthread_mutex_init(&dongle->mutex, NULL);
	pthread_cond_init(&dongle->cond, NULL);
}

int take_dongle(t_dongle *dongle, t_coder *coder)
{
	long now;

	pthread_mutex_lock(&dongle->mutex);
	while (!is_over(coder->hub))
	{
		now = get_time_ms();
		if (dongle->owner == -1 && now - dongle->released >= dongle->cooldown)
			break;
		pthread_cond_wait(&dongle->cond, &dongle->mutex);
	}
	if(is_over(coder->hub))
	{
		pthread_mutex_unlock(&dongle->mutex);
		return (0);
	}
	dongle->owner = coder->id;
	pthread_mutex_unlock(&dongle->mutex);
	loging(coder, "has taken a dongle");
	return(1);
}

void	release_dongle(t_dongle *dongle)
{
	pthread_mutex_lock(&dongle->mutex);
	dongle->owner = -1;
	dongle->released = get_time_ms();
	pthread_cond_broadcast(&dongle->cond);
	pthread_mutex_unlock(&dongle->mutex);
}
