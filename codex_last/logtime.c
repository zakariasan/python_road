/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   logtime.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/19 14:28:40 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/06/26 20:33:38 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

long	get_time_ms(void)
{
	struct timeval	tv;

	gettimeofday(&tv, NULL);
	return ((long)(tv.tv_sec * 1000) + (long)(tv.tv_usec / 1000));
}

void	loging(t_coder *coder, char *action)
{
	int	is_burned;

	is_burned = (strcmp(action, "burned out") == 0);
	pthread_mutex_lock(&coder->hub->print_mutex);
	if (!is_burned && is_over(coder->hub))
	{
		pthread_mutex_unlock(&coder->hub->print_mutex);
		return ;
	}
	printf("%ld %d %s\n",
		get_time_ms() - coder->hub->start_time,
		coder->id,
		action);
	pthread_mutex_unlock(&coder->hub->print_mutex);
}

void	u_sleep(t_hub *hub, int ms)
{
	struct timespec	ts;
	long			end;

	end = get_time_ms() + ms;
	ts.tv_sec = end / 1000;
	ts.tv_nsec = (end % 1000) * 1000000;
	pthread_mutex_lock(&hub->over_mutex);
	while (!hub->over && get_time_ms() < end)
		pthread_cond_timedwait(&hub->over_cond, &hub->over_mutex, &ts);
	pthread_mutex_unlock(&hub->over_mutex);
}
