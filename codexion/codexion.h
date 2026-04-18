/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/12 01:36:23 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/04/11 01:57:47 by zhaouzan         ###   ########.fr       */
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


typedef struct s_hub t_hub;
typedef enum e_scheduler
{
	FIFO,
	EDF
}			t_scheduler;

typedef struct s_dongle
{
	pthread_mutex_t	mutex;
	pthread_cond_t	cond;
	long			released;
	int				cooldown;
	int				id;
	int				owner;
	int				is_available;	
	t_scheduler		scheduler;
}					t_dongle;

typedef struct s_coder
{
	long		last_compile;
	int			counter;
	pthread_t	thread;
	t_dongle	*right;
	t_dongle	*left;
	int			id;
	t_hub		*hub;
}				t_coder;

typedef struct s_manager
{
	pthread_t	thread;
	t_coder		*coders;
	t_hub		*hub;
}				t_manager;


typedef struct s_hub
{
	pthread_mutex_t	print_mutex;
	pthread_mutex_t	over_mutex;
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


int is_over(t_hub *hub);
void set_over(t_hub *hub);
int			ft_init_hub(t_hub *hub);
long long	get_time_ms(void);
void		loging(t_coder *coder, char *action);
void		init_dongle(t_dongle *dongle, int id, long cooldown, int owner);
int			take_dongle(t_dongle *dongle, t_coder *coder);
void		release_dongle(t_dongle *dongle);
void		init_coder(t_coder *coder, int id, t_hub *hub);
void		*coder_rotine(void *args);
//void		*var_rotine(void *args);
void	*manager_rotine(void *args);
//int			take_dongles(t_dongle *left, t_dongle *right, t_coder *coder);
int			ft_parser(int ac, char **av, t_hub *hub);

#endif
