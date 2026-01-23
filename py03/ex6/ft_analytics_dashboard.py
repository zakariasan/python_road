"""
an analytics dashboard using comprehensions — Python’s most
data into pure insights!
"""
game_data = {
        "players": {
            "alice": {
                "level": 41,
                "total_score": 2300,
                "sessions_played": 22,
                "favorite_mode": "ranked",
                "achievements_count": 5,
                "achievements": [
                    "first_blood",
                    "level_master",
                    "speed_runner",
                    "treasure_seeker",
                    "boss_hunter"
                    ],
            },
            "bob": {
                "level": 16,
                "total_score": 1800,
                "sessions_played": 27,
                "favorite_mode": "ranked",
                "achievements_count": 3,
                "achievements": ["pixel_perfect", "combo_king", "explorer"]
            },
            "charlie": {
                "level": 44,
                "total_score": 2150,
                "sessions_played": 21,
                "favorite_mode": "ranked",
                "achievements_count": 7,
                "achievements": [
                    "pixel_perfect",
                    "combo_king",
                    "explorer",
                    "first_kill",
                    "level_10",
                    "boss_slayer",
                    "combo_king"
                    ],
            },
            "diana": {
                "level": 3,
                "total_score": 2050,
                "sessions_played": 13,
                "favorite_mode": "casual",
                "achievements_count": 4,
                "achievements": [
                    "pixel_perfect",
                    "combo_king",
                    "explorer",
                    "boss_slayer"
                    ]
            },
        },
        "game_modes": ["casual", "competitive", "ranked"],
        "game_regions": ["north", "east", "central"],
        "achievements": [
            "first_blood", "level_master", "speed_runner", "treasure_seeker",
            "boss_hunter", "pixel_perfect", "combo_king", "explorer",
        ],
    }
players = game_data["players"]

print("=== Game Analytics Dashboard ===\n")
print("=== List Comprehension Examples ===")

high_scores = [
        name for name, data in players.items() if data["total_score"] > 2000
        ]
mid_scores = [
        name for name, data in players.items() if data["total_score"] == 2000
        ]
double_scores = [data['total_score'] * 2 for name, data in players.items()]
active_players = [
        name for name, data in players.items() if data["sessions_played"] > 15
        ]
print(f"High scorers (>2000): {high_scores}")
print(f"Scores doubled: {double_scores}")
print(f"Active players: {active_players}\n")

print("=== Dict Comprehension Examples ===")
scores = {
        name: data['total_score'] for name, data in players.items()
        }
score_cat = {
        'high': len(high_scores),
        'medium': len(mid_scores),
        'low': len(players) - len(high_scores)
        }
ach_cnt = {
        name: data['achievements_count'] for name, data in players.items()
        }
print(f"Player scores: {scores}")
print(f"Score categories: {score_cat}")
print(f"Achievement counts: {ach_cnt}\n")

print("=== Set Comprehension Examples ===")
uni_players = set(players)
uni_ach = set(elm for data in players.values() for elm in data['achievements'])
active_reg = set(game_data['game_regions'])
print(f"Unique players: {uni_players}")
print(f"Unique achievements: {uni_ach}")
print(f"Active regions: {active_reg}\n")

print("=== Combined Analysis ===")
print(f"Total players: {len(players)}")
print(f"Total unique achievements: {ach_cnt}")
avg_scores = [
        data['total_score'] for data in players.values()]
print(f"Average score: {sum(avg_scores)/len(players)}")

top_name = ""
top_score = 0
for name, data in players.items():
    if data['total_score'] > top_score:
        top_score = data['total_score']
        top_name = name
        top_ach = data['achievements_count']

print("Top performer: ", end="")
print(f"{top_name} ({top_score} points, {top_ach} achievements)")
