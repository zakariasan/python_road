#include "codexion.h"

void init_coder(t_coder *coder,int id, long compile, long debug, long refactor)
{
	coder->time_to_compile = compile;
	coder->time_to_debug = debug;
	coder->time_to_refactor = refactor;
	coder->id = id;
	coder->right = NULL;
	coder->left = NULL;
}

void	*coder_rotine(void *args)
{
	t_coder	*coder;

	coder = (t_coder *)args;
	
	coder->start_time = get_time_ms();
	while(coder->left->owner != coder->id)
		take_dongle(coder->left, coder, coder->start_time);

	while(coder->right->owner != coder->id)
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
