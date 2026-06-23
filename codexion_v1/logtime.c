/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   logtime.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/19 14:28:40 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/06/23 00:00:00 by zhaouzan         ###   ########.fr       */
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
	if (!is_burned && is_over(coder->hub))
		return ;
	pthread_mutex_lock(&coder->hub->print_mutex);
	printf("%ld %d %s\n",
		get_time_ms() - coder->hub->start_time,
		coder->id,
		action);
	pthread_mutex_unlock(&coder->hub->print_mutex);
}
