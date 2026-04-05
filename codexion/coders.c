#include "codexion.h"

void init_coder(t_coder *coder,int id, long compile, long debug, long refactor)
{
	coder->time_to_compile = compile;
	coder->time_to_debug = debug;
	coder->time_to_refactor = refactor;
	coder->id = id;
	coder->counter = 0;
	coder->right = NULL;
	coder->left = NULL;
}

void	*coder_rotine(void *args)
{
	t_coder	*coder;

	coder = (t_coder *)args;
	
	while(coder->counter < coder->hub->compiles_required)
	{	
		while(!coder->hub->over && coder->left->owner != coder->id)
			take_dongles(coder->left, coder->right, coder, coder->start_time);
		if (coder->hub->over)
			return (NULL);

		if (coder->left->owner == coder->id && coder->right->owner == coder->id)
		{
			coder->last_compile = get_time_ms();
			pthread_mutex_lock(&coder->hub->print);
			loging(coder->id, coder->start_time, "is compiling");
			pthread_mutex_unlock(&coder->hub->print);
			usleep(coder->time_to_compile * 1000);
			release_dongle(coder->left);
			release_dongle(coder->right);
			pthread_mutex_lock(&coder->hub->print);
			loging(coder->id, coder->start_time, "is debugging");
			pthread_mutex_unlock(&coder->hub->print);
			usleep(coder->time_to_debug * 1000);
			pthread_mutex_lock(&coder->hub->print);
			loging(coder->id, coder->start_time, "is refactoring");
			pthread_mutex_unlock(&coder->hub->print);
			usleep(coder->time_to_refactor * 1000);
			coder->counter++;
		}
	}
	return (NULL);
}
