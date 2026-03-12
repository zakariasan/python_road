/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/12 01:36:23 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/03/12 03:28:00 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

# include <unistd.h>
# include <stdio.h>
# include <pthread.h>
# include <stdlib.h>

typedef struct s_dongle
{
	long long	released;
	long		d_cooldown;
	int			id;
	int			owner;
}				t_dongle;

typedef struct s_coder
{
	long long	start_time;
	pthread_t	thread;
	t_dongle	*right;
	t_dongle	*left;
	long		time_to_compile;
	long		time_to_debug;
	long		time_to_refactor;
	int			id;
}				t_coder;

enum e_scheduler
{
	fifo,
	edf
};

#endif
