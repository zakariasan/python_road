# -. check if the file is txt extention
# -. skip all comments
# -. read nb_drones > 0  (any number of drones must be > 0)
# 4. file must have the start_hub and end_hub
# 5.1 zome have : uniq name  and valide coodrination
# 5.2 no dashes and spaces
# 6 connection no duplication structure be like zone01-zone02 [metadata]

# reading lines
# check line
#   > the key is valide what is expected to be not
#   repeated while checking others
#   > the value is valide depend on what we have
# is it a valide file
# then reading the file again.
def ft_check_drones(game: dict, key: str, val: str):
    """Check number of drones

    Args:
        game: the dictionnary that contain the game
        key: nb_drones
        value: nbr of drones

    Raises:
        val is not a number
    """
    try:
        if 'nb_drones' not in game:
            nbr = ('', int(val))[val.isdigit()]
            if nbr and nbr > 0:
                game[key] = nbr
            else:
                raise ValueError("Number of drones must be constante digites")
        else:
            raise ValueError("Set muliple values of nb_drones")
    except Exception as e:
        print(e)


def ft_check_hub(game: dict, key: str, val: str):
    """Check hub type

    Args:
        game: the dictionnary that contain the game
        key: hub or start_hub or end_hub
        val: data of the hub

    Raises:
        hub is not valide
    """
    try:
        if 'hubs' not in game:
            game['hubs'] = {}
        hubs = game['hubs']
        if ((key == 'start_hub'
                or key == 'end_hub')
                and key not in hubs):
            nbr = ('', int(val))[val.isdigit()]
            if nbr and nbr > 0:
                game[key] = nbr
            else:
                raise ValueError("Number of drones must be constante digites")
        else:
            raise ValueError("Set muliple values of nb_drones")
    except Exception as e:
        print(e)


def ft_check_connexion(game: dict, key: str, val: str):
    """Check hub type

    Args:
        game: the dictionnary that contain the game
        key: hub or start_hub or end_hub
        val: data of the hub

    Raises:
        hub is not valide
    """
    pass


def ft_parser(filename: str):
    """Get data from filename  of the era drones hubs and connexions

    Args:
        filename: name of the path file
    """
    if not filename.endswith(".txt"):
        raise ValueError("Invalide extension Expected '.txt'")
    else:
        with open(filename, 'r') as f:
            game = {}
            for line in f:
                value = line.strip()
                if value.startswith('#') or value == '':
                    continue
                elif ':' not in value:
                    raise ValueError("Structure key:Value needed in path.txt")
                else:
                    required_key = [
                            'nb_drones',
                            'start_hub',
                            'hub',
                            'end_hub',
                            'connection'
                            ]
                key, val = value.split(':')
                key = key.strip()
                val = val.strip()
                if key in required_key:
                    if key == 'nb_drones':
                        ft_check_drones(game, key, val)
                    elif key == 'hub'\
                            or key == 'end_hub'\
                            or key == 'start_hub':
                        ft_check_hub(game, key, val)
                    else:
                        ft_check_connexion(game, key, val)
                else:
                    raise ValueError(f"data should be like {required_key}")
