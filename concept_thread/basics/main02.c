/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main02.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zhaouzan <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/11 15:43:39 by zhaouzan          #+#    #+#             */
/*   Updated: 2026/04/11 18:07:33 by zhaouzan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

int counter = 0;
int t1_done = 0;
pthread_cond_t cond;
pthread_mutex_t locker;

void* worker(void* arg)
{
	int id;
	pthread_t t_id;
	int i;

	id  = *(int *)arg;
	t_id = pthread_self();
	if (id == 2)
	{
		pthread_mutex_lock(&locker);
		while(t1_done == 0)
			pthread_cond_wait(&cond, &locker);
		pthread_mutex_unlock(&locker);
	}
	pthread_mutex_lock(&locker);
	i = -1;
	while (++i < 5000)
		counter++;
	if (id == 1)
	{
		t1_done = 1;
		pthread_cond_broadcast(&cond);
	}
	pthread_mutex_unlock(&locker);
	printf("=>Counter: %d\n Updated by: [T%lu]---[N-%d]\n ", counter, t_id, id);
	return NULL;
}

int main()
{
	int cnt;
	pthread_t t1;
	pthread_t t2;
	int id1;
	int id2;

	id1 = 1;
	id2 = 2;
	
	pthread_mutex_init(&locker, NULL);
	pthread_cond_init(&cond, NULL);
	pthread_create(&t1, NULL,worker, &id1);
	pthread_create(&t2, NULL,worker, &id2);
	pthread_join(t1, NULL);
	pthread_join(t2, NULL);
	pthread_cond_destroy(&cond);
    pthread_mutex_destroy(&locker);

	return (0);
}
