"""
Exercise 4: Master's Tower - Decorator mastery and class methods
"""
import functools
import time


def spell_timer(func: callable) -> callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Casting {func.__name__}...")
        start  = time.time()
        result = func(*args, **kwargs)
        end    = time.time()
        print(f"Spell completed in {end - start:.3f} seconds")
        return result
    return wrapper


def power_validator(min_power: int) -> callable:
    def decorator(func: callable) -> callable:
        @functools.wraps(func)
        def wrapper(power, *args, **kwargs):
            if power < min_power:
                return "Insufficient power for this spell"
            return func(power, *args, **kwargs)
        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> callable:
    def decorator(func: callable) -> callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print(f"Spell failed, retrying... (attempt {attempt}/{max_attempts})")
            return f"Spell casting failed after {max_attempts} attempts"
        return wrapper
    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        return len(name) >= 3 and all(c.isalpha() or c.isspace() for c in name)

    @power_validator(min_power=10)
    def cast_spell(self, power: int, spell_name: str) -> str:
        return f"Successfully cast {spell_name} with {power} power"


if __name__ == '__main__':
    print("Testing spell timer...")

    @spell_timer
    def fireball():
        time.sleep(0.1)
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
    print(guild.cast_spell(15, "Lightning"))
    print(guild.cast_spell(5,  "Lightning"))
