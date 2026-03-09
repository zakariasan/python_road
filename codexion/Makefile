CC	=	cc
NAME	=	codexion
CFLAGS	=	-Wall -Wextra -Werror -I. -pthread
SRC	=	$(wildcard *.c)
OBJ	=	$(SRC:.c=.o)
MAKE	=	make

all:	$(NAME)
	
$(NAME):	$(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o $(NAME)

%.o:	%.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ)

fclean:	clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
