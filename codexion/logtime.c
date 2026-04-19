#include "codexion.h"
#include <pthread.h>
#include <stdio.h>
#include <string.h>

long	get_time_ms(void)
{
	struct timeval	tv;

	gettimeofday(&tv, NULL);
	return (long)((tv.tv_sec * 1000) + (tv.tv_usec / 1000));
}

void	loging(t_coder *coder, char *action)
{
	if (is_over(coder->hub))
		return;
	pthread_mutex_lock(&coder->hub->print_mutex);
	if (strcmp(action,"is compiling") == 0)
		coder->last_compile = get_time_ms();
	if (!coder->hub->over || strcmp(action, "burned out") == 0)
		printf("%ld %d %s\n", get_time_ms() - coder->hub->start_time,
				coder->id, action);
	pthread_mutex_unlock(&coder->hub->print_mutex);
}
