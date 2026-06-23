/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/12 01:36:23 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/06/23 00:00:00 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

# include <unistd.h>
# include <stdio.h>
# include <pthread.h>
# include <stdlib.h>
# include <sys/time.h>
# include <string.h>

typedef struct s_hub	t_hub;

typedef enum e_scheduler
{
	FIFO,
	EDF
}			t_scheduler;

/*
** 2-slot priority queue embedded in each dongle.
** A dongle sits between exactly 2 coders, so at most 2 waiters at any time.
** FIFO: grant to the waiter with the smallest arrived timestamp.
** EDF : grant to the waiter with the smallest deadline.
*/
typedef struct s_waiter
{
	int		coder_id;
	long	arrived;
	long	deadline;
	int		active;
}			t_waiter;

typedef struct s_dongle
{
	int				id;
	int				owner;
	long			released;
	int				cooldown;
	pthread_mutex_t	mutex;
	pthread_cond_t	cond;
	t_waiter		queue[2];
	t_scheduler		scheduler;
}				t_dongle;

typedef struct s_coder
{
	int				id;
	long			deadline;
	int				counter;
	long			last_compile;
	pthread_t		thread;
	t_dongle		*left;
	t_dongle		*right;
	t_hub			*hub;
}				t_coder;

/*
** Monitor replaces the old manager: sleeps via timedwait until the nearest
** coder deadline, then checks for burnout or completion.
** over_cond is signalled whenever a deadline changes or over is set.
*/
typedef struct s_hub
{
	pthread_mutex_t	print_mutex;
	pthread_mutex_t	over_mutex;
	pthread_cond_t	over_cond;
	pthread_t		monitor;
	long			start_time;
	t_scheduler		scheduler;
	int				num_coders;
	int				time_to_burnout;
	int				time_to_compile;
	int				time_to_debug;
	int				time_to_refactor;
	int				compiles_required;
	int				dongle_cooldown;
	t_dongle		*dongles;
	t_coder			*coders;
	int				over;
}				t_hub;

/* logtime.c */
long	get_time_ms(void);
void	loging(t_coder *coder, char *action);

/* monitor.c */
void	*monitor_routine(void *args);
int		is_over(t_hub *hub);
void	set_over(t_hub *hub);
void	wake_all_dongles(t_hub *hub);

/* dongles.c */
void	init_dongle(t_dongle *dongle, int id, int cooldown, t_scheduler sched);
void	dongle_acquire(t_dongle *d, t_coder *c);
void	dongle_release(t_dongle *d, t_hub *hub);

/* coders.c */
void	init_coder(t_coder *coder, int id, t_hub *hub);
void	*coder_routine(void *args);

/* init.c */
int		ft_init_hub(t_hub *hub);

/* parser.c */
int		ft_parser(int ac, char **av, t_hub *hub);

/* ft_over.c */
int		ft_over(t_hub *hub);

#endif
