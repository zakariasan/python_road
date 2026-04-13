/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main01.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/11 15:43:39 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/04/11 16:24:40 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <pthread.h>
#include <stdio.h>
#include <unistd.h>
// with mutex 
// Limitation #1 — No Parallelism (Serialization)
// 3) Limitation #2 — Performance degradation
//
int counter = 0;
pthread_mutex_t locker;

void* worker(void* arg)
{
	pthread_t t_id;
	int i;

	pthread_mutex_lock(&locker);
	i = -1;
	t_id = pthread_self();
	while (++i < 5000)
	{
		counter++;
	}

	pthread_mutex_unlock(&locker);
	printf("=>Counter: %d\n Updated by: [T%lu]\n", counter, t_id);
	return NULL;
}

int main()
{
	int cnt;
	pthread_t t1;
	pthread_t t2;
	
	pthread_mutex_init(&locker, NULL);
	pthread_create(&t1, NULL,worker, NULL);
	pthread_create(&t2, NULL,worker, NULL);
	pthread_join(t1, NULL);
	pthread_join(t2, NULL);
    pthread_mutex_destroy(&locker);

	return (0);
}
