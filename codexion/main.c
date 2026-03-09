#include "codexion.h"

int main(int ac, char **av)
{
	if (ac != 9)
		return (-1);
	if (atoi(av[1]) <= 1)
		return (-1);
	
	return (0);
}
