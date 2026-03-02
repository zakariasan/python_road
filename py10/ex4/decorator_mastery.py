"""
Exercise 4: Master's Tower - Decorator mastery and class methods
"""
import functools
import time


def spell_timer(func: callable) -> callable:
    """ Time execution decorator """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """how many seconds can the function make it"""
        print(f"Casting {func.__name__}...")
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Spell completed in {end - start:.3f} seconds")
        return result
    return wrapper


def power_validator(min_power: int) -> callable:
    """ power _validator decorator with min_power """
    def decorator(func: callable) -> callable:
        """ deco try """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """ wrapper of the decorator """
            power = kwargs.get('power', None)
            if power is None:
                for arg in args:
                    if isinstance(arg, (int, float)):
                        power = arg
                        break
            if power is None or power < min_power:
                return "Insufficient power for this spell"
            return func(*args, **kwargs)
        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> callable:
    """ Retry decorator """
    def decorator(func: callable) -> callable:
        """ decorator creation """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """ warapper maek it """
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print(
                            "Spell failed, retrying... "
                            f"(attempt {attempt}/{max_attempts})")
            return f"Spell casting failed after {max_attempts} attempts"
        return wrapper
    return decorator


class MageGuild:
    """ mage Guild """
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        """ checker to validate this """
        return len(name) >= 3 and all(c.isalpha() or c.isspace() for c in name)

    @power_validator(min_power=10)
    def cast_spell(self, power: int, spell_name: str) -> str:
        """ cast spell print """
        return f"Successfully cast {spell_name} with {power} power"


if __name__ == '__main__':
    try:
        print("Testing spell timer...\n")

        @spell_timer
        def fireball():
            time.sleep(0.101)
            return "Fireball cast!"

        print(f"Result: {fireball()}")

        print("\nTesting power validator...")

        @power_validator(min_power=20)
        def ice_spike(power, target):
            return f"Ice spike hits {target} for {power} damage"

        print(ice_spike(30, "Dragon"))
        print(ice_spike(10, "Dragon"))

        print("\nTesting retry spell...")
        attempt_count = [0]

        @retry_spell(max_attempts=3)
        def unstable_spell():
            attempt_count[0] += 1
            if attempt_count[0] < 3:
                raise Exception("Spell unstable!")
            return "Unstable spell succeeded!"

        print(unstable_spell())

        print("\nTesting MageGuild...")
        print(MageGuild.validate_mage_name("Gandalf"))
        print(MageGuild.validate_mage_name("X2"))

        guild = MageGuild()
        print(guild.cast_spell("Lightning", 15))
        print(guild.cast_spell("Lightning", 5))
    except Exception as e:
        print(f"Error: {str(e)}")
