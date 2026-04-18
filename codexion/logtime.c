#include "codexion.h"
#include <pthread.h>
#include <stdio.h>

long long	get_time_ms(void)
{
	struct timeval	tv;

	gettimeofday(&tv, NULL);
	return (long long)((tv.tv_sec * 1000) + (tv.tv_usec / 1000));
}

void	loging(t_coder *coder, char *action)
{
	pthread_mutex_lock(&coder->hub->print_mutex);
	if (!is_over(coder->hub))
	{
	printf("%lld %d %s\n", get_time_ms() - coder->hub->start_time, coder->id, action);
	}
	pthread_mutex_unlock(&coder->hub->print_mutex);
}
