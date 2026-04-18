#include "codexion.h"

void init_coder(t_coder *coder,int id, t_hub *hub)
{
	coder->id = id;
	coder->counter = 0;
	coder->right = NULL;
	coder->left = NULL;
	coder->hub = hub;
	coder->last_compile = hub->start_time;
	coder->right =  &hub->dongles[id];
	coder->left = &hub->dongles[(id + 1) % hub->num_coders];
}

void	*coder_rotine(void *args)
{
	t_coder	*coder;

	coder = (t_coder *)args;
	
	while(!is_over(coder->hub))
	{
		if (coder->id % 2 == 0)
		{
			if (!take_dongle(coder->left, coder))
				break;
			if (!take_dongle(coder->right, coder))	
				break;		

		}
		else
		{
			if (!take_dongle(coder->right, coder))	
				break;
			if (!take_dongle(coder->left, coder))
				break;

		}
		coder->last_compile = get_time_ms();
		loging(coder, "is compiling");
		usleep(coder->hub->time_to_compile * 1000);
		release_dongle(coder->left);
		release_dongle(coder->right);
		loging(coder, "is debugging");
		usleep(coder->hub->time_to_debug * 1000);
		loging(coder, "is refactoring");
		usleep(coder->hub->time_to_refactor * 1000);
		coder->counter++;
	}
	return (NULL);
}
