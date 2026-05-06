import sys
from ft_valide_file import ft_valide_file
from errors import ParseError, ValidationError
from ft_viewer import run


def main():
    """ Starting the Game of fly-in """

    if len(sys.argv) != 2:
        print("Usage: python path_file.txt", sys.argv)

    else:

        try:
            game = ft_valide_file(sys.argv[1])
            run(game)
            print(f'>>>>{game.nb_drones}')
            print(f'>>>>{game.s_hub}')
            print(f'>>>>{game.e_hub}')
            for item in game.hubs:
                print(f'\n>>>>{item}: {game.hubs[item]}')
            print(f'>>>>{game.net}')
        except Exception as e:
            print(f'Config Error: {e}')


if __name__ == '__main__':
    main()
