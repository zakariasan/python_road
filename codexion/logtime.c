#include "codexion.h"

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
	//pthread_mutex_lock(&hub->print);
	printf("%lld %d %s\n", now, coder_id, action);
	//pthread_mutex_unlock(&hub->print);
}
