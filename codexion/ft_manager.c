#include "codexion.h"
#include <pthread.h>

int is_over(t_hub *hub)
{
	int res;

	pthread_mutex_lock(&hub->over_mutex);
	res = hub->over;
	pthread_mutex_unlock(&hub->over_mutex);
	return (res);
}

void set_over(t_hub *hub)
{
	pthread_mutex_lock(&hub->over_mutex);
	hub->over = 1;
	pthread_mutex_unlock(&hub->over_mutex);
}

void	*manager_rotine(void *args)
{
	t_manager	*manager;
	int		i;

	manager = (t_manager *)args;
	while (!is_over(manager->hub))
	{
		i = 0;
		while (i < manager->hub->num_coders)
		{
			if (get_time_ms() - manager->coders[i].last_compile > manager->hub->time_to_burnout)
			{
				loging(&manager->coders[i], "burned out");
				set_over(manager->hub);
				i = 0;
				while (i < manager->hub->num_coders)
				{
					pthread_cond_broadcast(&manager->coders[i].left->cond);
					pthread_cond_broadcast(&manager->coders[i].right->cond);
					i++;
				}
				return (NULL);
			}	
			i++;
		}
		usleep(500);
	}
	return (NULL);
}
