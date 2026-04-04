#include "codexion.h"

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
				loging(var->coders[i].id, var->hub->start_time, "burned out");
				usleep(10000);
				var->hub->over = 1;
				return (NULL);
			}	
			i++;
		}
		usleep(1000);
	}
	return (NULL);
}
