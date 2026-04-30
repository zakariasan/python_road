
def ft_update_game(key, value, game):
    pass


def ft_check_connection(key, value):
    pass


def ft_check_start_end_hub(key: str, val: str, game: dict):
    """Check the value of hub

    Args:
        val: value get by the pathfile
    """
    if len(val.split(' ') != 4):
        raise ValueError("hub structure is not valide.")
    elif key in game:
        raise ValueError("Duplicated hubs.")
    else:
        name, x, y, meta = val.split(' ')
        try:
            if '-' in name:
                raise ValueError("Names of hubs can't has dashes")
            x = int(x)
            y = int(y)

            # check name > double name or 
            # check x,y 
            # check meta
        except Exception as e:
            print(e)


def ft_check_drones(val: str, game: dict):
    """Check number of drones
    Args:
        value: nbr of drones
    Raises:
        val is not a number
    """
    try:
        nbr = int(val)
        if not val.isdigit() or nbr <= 0:
            raise ValueError("Number of drones must be a digites")
        else:
            game['nb_drones'] = nbr
    except Exception as e:
        print(e)


def ft_valide_key(key: str, game: dict) -> None:
    """Check the key part
    Args:
        key: key value.
        game: dict of the game
    """
    req_key: list = [
            'nb_drones',
            'start_hub',
            'hub',
            'end_hub',
            'connection'
            ]
    rep: list = [
            'nb_drones',
            'start_hub',
            'end_hub',
            ]
    if key not in req_key or (key in rep and key in game):
        raise ValueError("Invalide key or duplicated key")


def ft_valide_value(key: str, value: str, game: dict) -> None:
    """Check the value part.

    Args:
        value: value that we need to check.
        game: dict of the game
    """
    if key == 'nb_drones':
        ft_check_drones(value, game)
    elif key == 'start_hub' or key == 'end_hub':
        ft_check_start_end_hub(key, value, game)
    elif key == 'connection':
        ft_check_connection(key, value)


def ft_valide_file(filename: str) -> dict:
    """ Check if the path file is valide
    Args:
        filename: file path.
    Raises:
        Not a valide file
    Return:
        game dict contains key and values
    """
    game: dict = {}
    if filename.endswith('.txt') and len(filename.split('.')) == 2:
        with open(filename, 'r') as f:
            for line in f:
                value = line.strip()
                if value.startswith('#') or value == '':
                    continue
                elif ':' not in value or len(value.split(':')) != 2:
                    raise ValueError('Invalide Structure in path file.')
                else:
                    key, val = value.split(":")
                    ft_valide_key(key, game)
                    ft_valide_value(key, val, game)
                    ft_update_game(key, val, game)
    else:
        raise ValueError("Invalide file")
    return game
