#ifndef CODEXION_H
# define CODEXION_H

#include <unistd.h>
#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>

typedef struct s_dongle
{
	long	d_cooldown;
	int		id;
  int   owner;
}				t_dongle;


typedef struct s_coder
{
	pthread_t	thread;
	t_dongle	*right;
	t_dongle	*left;
	long		time_to_compile;
	long		time_to_debug;
	long		time_to_refactor;
	int			id;
}				t_coder;

enum scheduler
{
	fifo,
	edf
};

#endif
