from models import Game, Hub, Metadata, Zone, Net
from errors import ParseError, ValidationError
from typing import Optional


class Parser:
    """Parsing Part before the simulation"""

    def __init__(self, filename: str) -> None:
        """Start Parsing the file"""
        self.filename = filename
        self.game = Game()

    def ft_check_connection(self, value: str) -> None:
        """Check the connection part
        connection name1-name2 [metadata]

        Args:
            Key: keys get
            value: string to parse
            game: object needed
        """
        chunks = value.split()
        if not chunks or len(chunks) > 2:
            raise ParseError("Invalid connection format.")

        link, meta = chunks if len(chunks) == 2 else chunks + [""]
        chunks = link.split("-")
        if len(chunks) != 2 or not chunks[0] or not chunks[1]:
            raise ParseError("Invalide Connection link format.")
        n1, n2 = chunks
        if (n1 not in self.game.all_names()) \
                or (n2 not in self.game.all_names()):
            raise ParseError("Unknown name Link.")

        k1 = f"{n1}-{n2}"
        k2 = f"{n2}-{n1}"

        if k1 in self.game.net or k2 in self.game.net:
            raise ValueError("Duplicated network")
        meta_data = self.ft_parse_meta(meta, 'connection')
        self.game.net[k1] = Net(n1, n2, meta_data)

    def ft_parse_meta(self, meta_d: Optional[str], parent: str) -> Metadata:
        """parse meta data [zone='4 types' color=None ]

        Args:
            meta: part of string define metadata [zone, color]
            parent: key has metadata

        Return:
            Meta object that has zone color [max_drones/max_link]
        """
        if not meta_d:
            return Metadata()
        if not (meta_d.startswith("[") and meta_d.endswith("]")):
            raise ValueError("Metadata structure must be [start-end]")

        meta: str = meta_d[1:-1].strip()
        if not meta:
            raise ValidationError("Fill the metadata or remove []")

        ele: list[str] = [
                    "zone",
                    "color",
                    "max_drones",
                    ] if 'hub' in parent else ["max_link_capacity"]
        meta_obj = Metadata()
        for item in meta.split():
            if "=" not in item:
                raise ValueError("Metadata struture not respected.key=val")
            k, v = item.split("=", 1)
            if k not in ele:
                raise ValueError("Metadata not montioned in subject.")
            elif k == "zone":
                try:
                    meta_obj.zone = Zone(v)
                except ValueError:
                    raise ValueError("Invalide zone type")
            elif k == "color":
                meta_obj.color = v
            elif k == "max_drones":
                if int(v) <= 0:
                    raise ValueError("max_drones must be <postive int>")
                if parent == 'start_hub' or parent == 'end_hub':
                    self.check_start_end(v)
                meta_obj.max_drones = int(v)
            elif k == "max_link_capacity":
                if int(v) <= 0:
                    raise ValueError("max_drones must be <postive int>")
                meta_obj.max_link_capacity = int(v)
        return meta_obj

    def check_start_end(self, value: str) -> None:
        """Checking the start and end part with max_drones

        Args:
            value: nbr of drones
        """
        if int(value) < self.game.nb_drones:
            raise ValidationError(
                    "Start and End should have at least number of drones")

    def ft_split_meta(self, value: str) -> tuple[str, str]:
        """Split the Hub string before parsing/validation"""
        if "[" in value:
            i = value.index("[")
            return value[:i].strip(), value[i:].strip()
        return value.strip(), ""

    def ft_check_hub(self, key: str, value: str) -> None:
        """check hub
        Args:
            key: name of key member
            value: value of the key
            game: object of the Game
        """
        data: str
        meta: Optional[str]
        data, meta = self.ft_split_meta(value)
        chunks: list[str] = data.split()
        if len(chunks) != 3:
            raise ParseError("Invalide hub format.")
        name: str = chunks[0]
        x_s: str = chunks[1]
        y_s: str = chunks[2]

        try:
            x: int = int(x_s)
            y: int = int(y_s)
        except ValueError:
            raise ParseError("Coordinates must be integers.")
        if meta == "":
            meta = None

        if name in self.game.all_hubs():
            raise ValidationError("Duplicate Hub name.")

        if (x, y) in self.game.all_coords():
            raise ValidationError(f"Duplicated coor({x},{y})")
        meta_data: Metadata = self.ft_parse_meta(meta, key)
        hub: Hub = Hub(name, x, y, meta_data)

        if key == "start_hub":
            if self.game.s_hub:
                raise ValidationError("Multiple start hub.")
            self.game.s_hub = hub
        elif key == "end_hub":
            if self.game.e_hub:
                raise ValidationError("Multiple end hub.")
            self.game.e_hub = hub
        else:
            self.game.hubs[name] = hub

    def ft_check_drones(self, val: str) -> None:
        """Check number of drones
        Args:
            value: nbr of drones
        Raises:
            val is not a number
        """
        if self.game.nb_drones == 0:
            if not val.isdigit():
                raise ParseError("nbr of drones must be integer")
            nbr: int = int(val)
            if nbr <= 0:
                raise ValidationError("Number of drones must be positive int.")
            self.game.nb_drones = nbr
        else:
            raise ParseError("Duplicated nbr of drones.")

    def ft_valide_key(self, key: str) -> None:
        """Check the key part

        Args:
            key: key value.
            game: dict of the game
        """
        req_key: set[str] = {
                "nb_drones",
                "start_hub",
                "hub",
                "end_hub",
                "connection"
                }
        if key not in req_key:
            raise ParseError(f"Invalide key or duplicated key:{key}")

    def ft_valide_value(self, key: str, value: str) -> None:
        """Check the value part.

        Args:
            value: value that we need to check.
            game: dict of the game
        """
        if key == "nb_drones":
            self.ft_check_drones(value)

        elif key in ("start_hub", "end_hub", "hub"):
            self.ft_check_hub(key, value)

        elif key == "connection":
            self.ft_check_connection(value)

    def ft_parse(self) -> Game:
        """Check if the path file is valide
        Args:
            filename: file path.
        Raises:
            Not a valide file
        Return:
            game dict contains key and values
        """
        if self.filename.endswith(".txt"):
            with open(self.filename, "r") as f:
                for i, line in enumerate(f, 1):
                    value = line.strip()

                    if value.startswith("#") or value == "":
                        continue
                    if '#' in value:
                        value = value.split('#', 1)[0].strip()
                    if ":" not in value:
                        raise ParseError(f"Line {i}: Invalide Structure.")
                    try:
                        key, val = value.split(":", 1)
                        key = key.strip()
                        val = val.strip()
                        self.ft_valide_key(key)
                        self.ft_valide_value(key, val)
                    except (ValueError, ParseError, ValidationError) as e:
                        raise ValidationError(f"Line {i}: Error:{e}")
            if not self.game.check_game():
                raise ValueError(
                        "ERROR: Check map file start or end is Missing.")
        else:
            raise ValueError("Invalide file")
        return self.game
