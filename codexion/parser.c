#include "codexion.h"


void  ft_get_values(char **av, t_hub *hub)
{
	hub->num_coders = atoi(av[1]);
	hub->time_to_burnout = atoi(av[2]);
	hub->time_to_compile = atoi(av[3]);
	hub->time_to_debug = atoi(av[4]);
	hub->time_to_refactor = atoi(av[5]);
	hub->compiles_required = atoi(av[6]);
	hub->dongle_cooldown = atoi(av[7]);
	hub->scheduler = av[8];
}

int ft_parser(int ac, char **av, t_hub *hub)
{
  int i;
  int item;

  i = 1;
  if (ac != 9)
  {
    fprintf(stderr, "Usage: ./codexion num_coders time_to_burnout "
            "time_to_compile time_to_debug time_to_refactor "
            "compiles_required dongle_cooldown scheduler\n");
    return (-1);
  }
  while (i < ac - 1)
  {
    item = atoi(av[i]);
    if (item < 0)
    {
      fprintf(stderr, "Error: invalid argument [%s]\n", av[i]);
      return (-1);
    }
    i++;
  }
  if (strcmp(av[i], "fifo") != 0 && strcmp(av[i], "edf") != 0)
  {
    fprintf(stderr, "Error: scheduler must be 'fifo' or 'edf'\n");
    return (-1);
  }
  ft_get_values(av, hub);
  return (0);
}
