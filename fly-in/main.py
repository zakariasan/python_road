import sys
from ft_valide_file import ft_valide_file
from errors import ParseError, ValidationError
from ft_viewer import run


def main() -> None:
    """ Starting the Game of fly-in """

    if len(sys.argv) != 2:
        print("Usage: python path_file.txt", sys.argv)

    else:

        try:
            game = ft_valide_file(sys.argv[1])
            if game.s_hub is None or game.e_hub is None:
                raise ValidationError("Missing start or End")
            game.s_hub.meta.max_drones = game.nb_drones
            game.e_hub.meta.max_drones = game.nb_drones
            run(game)
        except (ParseError, ValidationError) as e:
            print(f'{e}')


if __name__ == '__main__':
    main()
