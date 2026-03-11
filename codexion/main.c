#include "codexion.h"
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

void *coder_rotine(void *args)
{
  t_coder *coder;

  coder = (t_coder*)args;
  printf("Coder Created\n");
  printf("id : %d\ncompiling_time : %ld\ndebuging : %ld\n ref : %ld",
         coder->id, coder->time_to_compile, coder->time_to_debug, coder->time_to_refactor
         );

  printf("\nprint dongle right: %d", coder->right->id);
  printf("\nprint dongle left: %d", coder->left->id);
  //take dongle left take_dongle(left)

  //take dongle right take_dongle(right)
  //Login X is compiling
  //
  //release_dongle(left) and release_dongle(right)

  printf("Coder %d is compiling...\n", coder->id);
  usleep(coder->time_to_compile * 1000);

  printf("Coder %d is debugging...\n", coder->id);
  usleep(coder->time_to_debug * 1000);

  printf("Coder %d is refactoring...\n", coder->id);
  usleep(coder->time_to_refactor * 1000);


  printf("Coder %d done.\n", coder->id);

  return (NULL);
}


int main()
{
	t_coder *coder;
  t_dongle *dongle;

  dongle = malloc(sizeof(t_dongle) * 2);
	coder = malloc(sizeof(t_coder));
	if (!coder)
		return (-1);

	coder->time_to_compile = 2000;
	coder->time_to_debug = 1000;
	coder->time_to_refactor = 1000;
	coder->id = 1;
	coder->right = NULL;
	coder->left = NULL;

  (dongle + 0)->d_cooldown = 10;
  dongle[0].id = 12;
  dongle[0].owner = -1;

  (dongle + 1)->d_cooldown = 10;
  dongle[1].id = 22;
  dongle[1].owner = -1;

  coder->right = dongle;
  coder->left = dongle + 1;
  if (pthread_create(&coder->thread, NULL, coder_rotine, coder) != 0)
  {
	  free(coder);
	  return (-1);
  }
  if (pthread_join(coder->thread, NULL) != 0)
	  return (-1);
  free(coder);
	return (0);
};


/*
 *What a Dongle Needs Right Now
ctypedef struct s_dongle
{
    int             id;
    int             held_by;      // -1 = free, otherwise coder id holding it
    long            cooldown_ms;
    long long       release_time; // when it was released (for cooldown)
    pthread_mutex_t mutex;
}   t_dongle;
```

## What `take_dongle` and `release_dongle` Should Do
```
take_dongle:
    lock the mutex
    check if dongle is free AND cooldown has passed
    if yes → mark held_by = coder->id, unlock, return
    if no  → wait... (for now just spin or usleep, real waiting comes later)
    unlock

release_dongle:
    lock the mutex
    mark held_by = -1
    record release_time = now
    unlock
The Challenge For You To Try
Wire up your existing coder routine to:

Call take_dongle(left) → log "X has taken a dongle"
Call take_dongle(right) → log "X has taken a dongle"
Log "X is compiling", usleep compile time
Call release_dongle(left) and release_dongle(right)
Continue to debug → refactor
 */
