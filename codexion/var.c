#include "codexion.h"
#include <pthread.h>

void	*var_rotine(void *args)
{
	t_var	*var;
	int		i;
	long long now;

	var = (t_var *)args;
	while (1)
	{
		i = 0;
		now = get_time_ms();
		while (i < var->hub->num_coders)
		{
			if (now - var->coders[i].last_compile > var->hub->time_to_burnout)
			{
				pthread_mutex_lock(&var->hub->print);
				loging(var->coders[i].id, var->hub->start_time, "burned out");
				pthread_mutex_unlock(&var->hub->print);
				var->hub->over = 1;
				i = 0;
				while (i < var->hub->num_coders)
				{
					pthread_cond_broadcast(&var->coders[i].left->cond);
					pthread_cond_broadcast(&var->coders[i].right->cond);
					i++;
				}
				return (NULL);
			}	
			i++;
		}
		usleep(1000);
	}
	return (NULL);
}
