#!/usr/bin/env python3
"""Generate additional listing JSON files based on an existing sample.

This script:
- picks a random existing JSON file from the `listings/` folder
- extracts the listing `url` (or finds the first http-like string)
- creates 750 new JSON files in `listings/` with new numeric IDs
- ensures `city`/`country` set to Islamabad/Pakistan and preserves coordinates
"""
import copy
import glob
import json
import os
import random
import sys


LISTINGS_DIR = "listings"
NUM_TO_GENERATE = 750
DATE_SUFFIX = "2025-12-07"


def find_url_in_obj(obj):
    if isinstance(obj, str) and obj.startswith("http"):
        return obj
    if isinstance(obj, dict):
        for v in obj.values():
            res = find_url_in_obj(v)
            if res:
                return res
    if isinstance(obj, list):
        for v in obj:
            res = find_url_in_obj(v)
            if res:
                return res
    return None


def main():
    os.makedirs(LISTINGS_DIR, exist_ok=True)
    files = glob.glob(os.path.join(LISTINGS_DIR, "*.json"))
    if not files:
        print("No sample listing files found in listings/; aborting.")
        sys.exit(1)

    sample_file = random.choice(files)
    with open(sample_file, "r", encoding="utf-8") as f:
        sample = json.load(f)

    # prefer common keys
    url = None
    for key in ("url", "listing_url", "source_url", "href", "airbnb_url"):
        if key in sample and isinstance(sample[key], str):
            url = sample[key]
            break
    if not url:
        url = find_url_in_obj(sample) or ""

    created = 0
    tries = 0
    max_tries = NUM_TO_GENERATE * 10

    while created < NUM_TO_GENERATE and tries < max_tries:
        tries += 1
        # generate a 19-digit-like id similar to existing filenames
        new_id = str(random.randint(10**18, 10**19 - 1))
        filename = f"{new_id}_{DATE_SUFFIX}.json"
        out_path = os.path.join(LISTINGS_DIR, filename)
        if os.path.exists(out_path):
            continue

        item = copy.deepcopy(sample)
        # set explicit id fields if present
        if "id" in item:
            try:
                item["id"] = int(new_id)
            except Exception:
                item["id"] = new_id
        elif "listing_id" in item:
            item["listing_id"] = new_id
        else:
            item["id"] = new_id

        # enforce Islamabad/Pakistan
        if "city" in item:
            item["city"] = "Islamabad"
        if "country" in item:
            item["country"] = "Pakistan"
        # some datasets use location keys
        if "country_name" in item:
            item["country_name"] = "Pakistan"
        if "city_name" in item:
            item["city_name"] = "Islamabad"

        # keep url value from sample as requested
        if url:
            # place under common keys
            if "url" in item:
                item["url"] = url
            elif "listing_url" in item:
                item["listing_url"] = url
            else:
                item["url"] = url

        # optionally tweak name/title so files are distinguishable
        if "name" in item and isinstance(item["name"], str):
            item["name"] = f"{item['name']} — Islamabad {created+1}"
        elif "title" in item and isinstance(item["title"], str):
            item["title"] = f"{item['title']} — Islamabad {created+1}"

        # write file
        try:
            with open(out_path, "w", encoding="utf-8") as out_f:
                json.dump(item, out_f, ensure_ascii=False, indent=2)
            created += 1
        except Exception as e:
            print(f"Failed to write {out_path}: {e}")

    print(f"Generated {created} new listing files in {LISTINGS_DIR}/ (requested {NUM_TO_GENERATE})")


if __name__ == "__main__":
    main()
