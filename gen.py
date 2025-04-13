import random
import json
import itertools

def db_read():
    try:
        with open("gen_db.json") as f:
            data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = {}
    return data


def create_json(data):
    numbers = ['1', '2', '3', '4', '5', '6']
    all_codes = [''.join(code) for code in itertools.product(numbers, repeat=4)]
    for code in all_codes:
        data[code] = {"playcount": 0, "turn_count": 0}
    with open("gen_db.json", "w") as f:
        json.dump(data, f, indent=4)


def gen():
    """
    function intended to generate a random code with biases to codes that have a statistic proclivity to win
    an algorithm will beat this regardless and not notice this, but maybe there's a human pattern in the data,
    one that might be exploited, so it may stump future players.
    :return: viable code for player initiated game
    """
    db = db_read()
    if len(db) == 0:
        create_json(db)
        codes = list(db.keys())
        return random.choice(codes)
    else:
        codes = []
        priority_codes = [code for code, stats in db.items() if stats["playcount"] == 0]

        if priority_codes:
            return random.choice(priority_codes)
        else:
            for code, stats in db.items():
                if stats["playcount"] > 0:
                    weight = stats["turn_count"] // stats["playcount"]
                    codes.extend([code] * max(1, weight))

            if codes:
                return random.choice(codes)
            else:
                return random.choice(list(db.keys()))


def db_insert(db):
    key = db[-1]
    turn_count = len(db)
    db = db_read()
    a, b = db[key]['turn_count'], db[key]['playcount']
    b += 1
    a = a + turn_count
    db[key]['turn_count'], db[key]['playcount'] = a, b
    with open("gen_db.json", "w") as f:
        json.dump(db, f, indent=4)
