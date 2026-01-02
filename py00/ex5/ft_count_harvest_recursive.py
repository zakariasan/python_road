def ft_count_harvest_recursive(days=None, x=1):
    """
    Count days until harvest using iteration.
    """
    if days is None:
        days = int(input("Days until harvest: "))
    
    if x <= days:
        print(f"Day {x}")
        ft_count_harvest_recursive(days, x + 1)
    else:
        print("Harvest time!")
