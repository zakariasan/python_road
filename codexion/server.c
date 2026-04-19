/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   server.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/19 17:46:23 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/04/19 17:58:46 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	ft_list(t_req *a, t_req *b, t_scheduler opt)
{
	if (opt == FIFO)
		return(a->time < b->time);
	if (opt == EDF)
		return (a->coder.deadline);
	return(a->time < b->time);
}
