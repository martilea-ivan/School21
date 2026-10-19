import json
import os

from datalayer.deserializers import player_from_dict, level_from_dict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RECORDS_FILE = os.path.join(BASE_DIR, "records.json")
SAVE_FILE = os.path.join(BASE_DIR, "savegame.json")


def load_records():
    try:
        with open(RECORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_records(records):
    with open(RECORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def add_record(name, level, gold, stats):
    records = load_records()
    records.append({
        "name": name,
        "level": level,
        "gold": gold,
        "enemies_killed": stats.enemies_killed,
        "food_eaten": stats.food_eaten,
        "elixirs_drunk": stats.elixirs_drunk,
        "scrolls_read": stats.scrolls_read,
        "hits_dealt": stats.hits_dealt,
        "hits_missed": stats.hits_missed,
        "cells_moved": stats.cells_moved,
        "treasures_collected": stats.treasures_collected,
        "hp_lost": stats.hp_lost,
        "levels_passed": stats.levels_passed,
        "deaths": stats.deaths,
    })
    records.sort(key=lambda r: r["gold"], reverse=True)
    save_records(records)


def get_top_records(limit=10):
    return load_records()[:limit]


def has_save():
    return os.path.exists(SAVE_FILE)


def save_game(player, level):
    data = {
        "player": player.to_dict(),
        "level": level.to_dict(),
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_game():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return None

    player = player_from_dict(data["player"])
    level = level_from_dict(data["level"])
    return player, level


def delete_save():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)