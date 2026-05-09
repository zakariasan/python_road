from models import Game, Hub, Metadata, Zone, Net
from errors import ParseError, ValidationError
from typing import Optional


def ft_check_connection(value: str, game: Game):
    """ Check the connection part
    connection name1-name2 [metadata]

    Args:
        Key: keys get
        value: string to parse
        game: object needed
    """
    chunks = value.split()
    if not chunks or len(chunks) > 2:
        raise ParseError("Invalid connection format.")

    link, meta = chunks if len(chunks) == 2 else chunks + ['']
    chunks = link.split('-')
    if len(chunks) != 2 or not chunks[0] or not chunks[1]:
        raise ParseError('Invalide Connection link format.')
    n1, n2 = chunks
    if (n1 not in game.all_names())\
            or (n2 not in game.all_names()):
        raise ParseError('Unknown name Link.')

    k1 = f"{n1}-{n2}"
    k2 = f"{n2}-{n1}"

    if k1 in game.net or k2 in game.net:
        raise ValueError('Duplicated network')
    meta = ft_parse_meta(meta)
    game.net[k1] = Net(n1, n2, meta)


def ft_parse_meta(meta: Optional[str]) -> Metadata:
    """ parse meta data [zone='4 types' color=None ]

    Args:
        meta: part of string define metadata [zone, color]

    Return:
        Meta object that has zone color [max_drones/max_link]
    """
    if not meta:
        return Metadata()
    if not (meta.startswith('[') and meta.endswith(']')):
        raise ValueError("Metadata structure must be [start-end]")

    meta: str = meta[1:-1].strip()
    if not meta:
        return Metadata()

    ele: list = ['zone', 'color', 'max_drones', 'max_link_capacity']
    meta_obj = Metadata()
    for item in meta.split():
        if '=' not in item:
            raise ValueError("Metadata struture not respected.key=val")
        k, v = item.split('=', 1)
        if k not in ele:
            raise ValueError("Metadata not montioned in subject.")
        elif k == 'zone':
            try:
                meta_obj.zone = Zone(v)
            except ValueError:
                raise ValueError("Invalide zone type")
        elif k == 'color':
            meta_obj.color = v
        elif k == 'max_drones':
            nbr = int(v)
            meta_obj.max_drones = int(v)
        elif k == 'max_link_capacity':
            nbr = int(v)
            meta_obj.max_link_capacity = nbr
    return meta_obj


def ft_split_meta(value: str):
    """ Split the Hub string before parsing/validation"""
    if '[' in value:
        i = value.index('[')
        return value[:i].strip(), value[i:].strip()
    return value.strip(), ''


def ft_check_hub(key: str, value: str, game: Game) -> None:
    """check hub

    Args:
        key: name of key member
        value: value of the key
        game: object of the Game
    """
    data, meta = ft_split_meta(value)
    chunks: str = data.split()
    if len(chunks) != 3:
        raise ParseError("Invalide hub format.")
    name, x, y = chunks

    try:
        x: int = int(x)
        y: int = int(y)
    except ValueError:
        raise ParseError("Coordinates must be integers.")
    if meta == '':
        meta = None

    if name in game.all_hubs():
        raise ValidationError("Duplicate Hub name.")

    if (x, y) in game.all_coords():
        raise ValidationError(f"Duplicated coor({x},{y})")
    meta = ft_parse_meta(meta)
    hub = Hub(name, x, y, meta)

    if key == 'start_hub':
        if game.s_hub:
            raise ValidationError("Multiple start hub.")
        game.s_hub = hub
    elif key == 'end_hub':
        if game.e_hub:
            raise ValidationError("Multiple end hub.")
        game.e_hub = hub
    else:
        game.hubs[name] = hub


def ft_check_drones(val: str, game: Game) -> None:
    """Check number of drones
    Args:
        value: nbr of drones
    Raises:
        val is not a number
    """
    if game.nb_drones == 0:
        if not val.isdigit():
            raise ParseError("nbr of drones must be integer")
        nbr: int = int(val)
        if nbr <= 0:
            raise ValidationError("Number of drones must be positive int")
        game.nb_drones = nbr
    else:
        raise ParseError("Duplicated nbr of drones.")


def ft_valide_key(key: str, game: Game) -> None:
    """Check the key part

    Args:
        key: key value.
        game: dict of the game
    """
    req_key: list = {
            'nb_drones',
            'start_hub',
            'hub',
            'end_hub',
            'connection'
            }
    if key not in req_key:
        raise ParseError(f"Invalide key or duplicated key:{key}")


def ft_valide_value(key: str, value: str, game: Game) -> None:
    """Check the value part.

    Args:
        value: value that we need to check.
        game: dict of the game
    """
    if key == 'nb_drones':
        ft_check_drones(value, game)

    elif key in ('start_hub', 'end_hub', 'hub'):
        ft_check_hub(key, value, game)

    elif key == 'connection':
        ft_check_connection(value, game)


def ft_valide_file(filename: str) -> Game:
    """ Check if the path file is valide
    Args:
        filename: file path.
    Raises:
        Not a valide file
    Return:
        game dict contains key and values
    """
    if filename.endswith('.txt') and len(filename.split('.')) == 2:
        game = Game()
        with open(filename, 'r') as f:
            for i, line in enumerate(f, 1):
                value = line.strip()

                if value.startswith('#') or value == '':
                    continue
                if ':' not in value or len(value.split(':')) != 2:
                    raise ParseError(f'Line {i}: Invalide Structure.')
                try:
                    key, val = value.split(":", 1)
                    key = key.strip()
                    val = val.strip()
                    ft_valide_key(key, game)
                    ft_valide_value(key, val, game)
                except (ValueError, ParseError, ValidationError) as e:
                    raise ValidationError(f'Line {i}: Error:{e}')
        if not game.check_game():
            raise ValueError("Missing drones")
    else:
        raise ValueError("Invalide file")
    return game
