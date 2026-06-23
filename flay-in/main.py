import sys
import os
from ft_parser import Parser
from errors import ParseError, ValidationError
from ft_viewer import Viewer
from ft_config import Config
from ft_sim import Sim


class FlyIn:
    """Starting from her flying there"""

    def __init__(self) -> None:
        """starting point """
        self.fly_in()

    @staticmethod
    def clear_terminal() -> None:
        """Clear the output of terminal"""
        if os.name == 'posix':
            os.system('clear')

    @staticmethod
    def ft_get_file() -> str:
        """first check the file format"""
        if len(sys.argv) != 2:
            raise ValueError(
                    "Usage: python main.py path_file.txt \n"
                    +
                    "or Usage: make file=path_file.txt")
        filename = sys.argv[1]
        if not filename.endswith('.txt'):
            raise ValueError("File must be a .txt")
        return filename

    def fly_in(self) -> None:
        """ Starting the Game of fly-in """
        try:
            filename = self.ft_get_file()
            parser = Parser(filename)
            game = parser.ft_parse()
            if game.s_hub is None or game.e_hub is None or game.s_hub.meta.zone == Zone.blocked:
                raise ValidationError("Missing start or End")
            if game.s_hub.meta.max_drones == 1:
                game.s_hub.meta.max_drones = game.nb_drones
            if game.e_hub.meta.max_drones == 1:
                game.e_hub.meta.max_drones = game.nb_drones
            config = Config(game)
            sim = Sim(game)
            viewer = Viewer(sim, config)
            viewer.run()
        except (ValueError, ParseError, ValidationError) as e:
            print(f'{e}')
        except KeyboardInterrupt:
            self.clear_terminal()
            print('Exit.^_^')


if __name__ == '__main__':
    FlyIn()
