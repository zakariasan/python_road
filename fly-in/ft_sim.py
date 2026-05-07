from models import Game


def ft_simulate(game):
    n          = game.nb_drones
    end_name   = game.e_hub.name
    pos        = [game.s_hub.name] * n   # all start at start
    done       = [False] * n
    sim_turn   = 0

    while not all(done):
        sim_turn += 1
        turn_moves = []

        # --- who is sitting in each hub right now ---
        occ = {}
        for i in range(n):
            if done[i]:
                continue
            occ[pos[i]] = occ.get(pos[i], 0) + 1

        # --- each drone decides ---
        for i in range(n):
            if done[i]:
                continue

            # Q1: already at goal?
            if pos[i] == end_name:
                done[i] = True
                continue

            # Q2: what is my best next hop?
            path = A_star(game, pos[i])
            if not path or len(path) < 2:
                continue
            next_hub = path[1]

            # Q3: is it full?
            capacity = next_hub.meta.max_drones
            if next_hub.name == end_name:
                capacity = 999   # end hub unlimited

            current  = occ.get(next_hub.name, 0)
            leaving  = 1 if pos[i] != next_hub.name else 0  

            if current - leaving < capacity:
                # ✅ move
                occ[pos[i]]        = occ.get(pos[i], 0) - 1
                occ[next_hub.name] = occ.get(next_hub.name, 0) + 1
                pos[i]             = next_hub.name
                turn_moves.append(f"D{i+1}-{next_hub.name}")
                if next_hub.name == end_name:
                    done[i] = True
            # else: wait, do nothing

        print(f"Turn {sim_turn}: {' '.join(turn_moves)}")

    print(f"\n✅ {n} drones done in {sim_turn} turns")
