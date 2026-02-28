import os
import json
from collections import Counter

LISTINGS_DIR = os.path.join(os.path.dirname(__file__), "..", "listings")


def get_categories():
    room_types = Counter()
    listing_types = Counter()

    for filename in os.listdir(LISTINGS_DIR):
        if not filename.endswith(".json"):
            continue
        with open(os.path.join(LISTINGS_DIR, filename), "r", encoding="utf-8") as f:
            data = json.load(f)

        rt = data.get("room_type")
        lt = data.get("listing_type")

        if rt:
            room_types[rt] += 1
        if lt:
            listing_types[lt] += 1

    print("=" * 60)
    print("ROOM TYPE CATEGORIES")
    print("=" * 60)
    for value, count in room_types.most_common():
        print(f"  {value}  ({count})")

    print()
    print("=" * 60)
    print("LISTING TYPE CATEGORIES")
    print("=" * 60)
    for value, count in listing_types.most_common():
        print(f"  {value}  ({count})")

    print()
    print(f"Total unique room types   : {len(room_types)}")
    print(f"Total unique listing types : {len(listing_types)}")
    print(f"Total listings scanned     : {sum(room_types.values())}")


if __name__ == "__main__":
    get_categories()
