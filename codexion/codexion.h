/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/12 01:36:23 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/04/04 01:13:13 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

# include <unistd.h>
# include <stdio.h>
# include <pthread.h>
# include <stdlib.h>
# include <sys/time.h>
# include <stdlib.h>
# include <string.h>

typedef struct s_dongle
{
  pthread_mutex_t mutex;
	long long	released;
	long		d_cooldown;
	int			id;
	int			owner;
}				t_dongle;

enum e_scheduler
{
	fifo,
	edf
};

typedef struct    s_hub
{
	int					num_coders;
	int					time_to_burnout;
	int					time_to_compile;
	int					time_to_debug;
	int					time_to_refactor;
	int					compiles_required;
	int					dongle_cooldown;
	char*				scheduler;
	int					over;
	pthread_mutex_t		print;
	long long			start_time;
}                 t_hub;

typedef struct s_coder
{
	long long	start_time;
	long long	last_compile;
	t_hub		*hub;
	int			counter;
	pthread_t	thread;
	t_dongle	*right;
	t_dongle	*left;
	int			time_to_compile;
	int			time_to_debug;
	int			time_to_refactor;
	int			id;
}				t_coder;

typedef	struct s_var
{
	pthread_t	thread;
	t_coder		*coders;
	t_hub		*hub;
}				t_var;

long long	get_time_ms(void);
void	loging(int coder_id, long long start_time, char *action);
void init_dongle(t_dongle *dongle, int id, long cooldown, int owner);
void take_dongle(t_dongle *dongle, t_coder *coder, long long time);
int take_dongles(t_dongle *left, t_dongle *right, t_coder *coder, long long time);
void	release_dongle(t_dongle *dongle);
void init_coder(t_coder *coder,int id, long compile, long debug, long refactor);

void	*coder_rotine(void *args);

void	*var_rotine(void *args);

int ft_parser(int ac, char **av, t_hub *hub);

#endif
