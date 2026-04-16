#include "codexion.h"

void init_coder(t_coder *coder,int id, t_hub *hub)
{
	coder->time_to_compile = hub->time_to_compile;
	coder->time_to_debug = hub->time_to_debug;
	coder->time_to_refactor = hub->time_to_refactor;
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
		if (coder->hub->over)
			return (NULL);
		//if(take_dongles(coder->left, coder->right, coder) == 0)
		//	return (NULL);
		while (coder->left->owner != coder->id)
			take_dongle(coder->left, coder);
		while (coder->right->owner != coder->id)
			take_dongle(coder->right, coder);
		
		if (coder->left->owner == coder->right->owner )
		{
		coder->last_compile = get_time_ms();
		loging(coder, "is compiling");
		usleep(coder->time_to_compile * 1000);
		release_dongle(coder->left);
		release_dongle(coder->right);
		loging(coder, "is debugging");
		usleep(coder->time_to_debug * 1000);
		loging(coder, "is refactoring");
		usleep(coder->time_to_refactor * 1000);
		coder->counter++;
		}
	}
	return (NULL);
}
