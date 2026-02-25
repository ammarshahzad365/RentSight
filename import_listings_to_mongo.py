#!/usr/bin/env python3
"""Import JSON listing files from `listings/` into MongoDB.

Usage:
  - Set `MONGO_URI` environment variable to your MongoDB connection string (default: mongodb://localhost:27017)
  - Run: `python3 import_listings_to_mongo.py`

Behavior:
  - Reads all `*.json` files from the `listings/` directory
  - For each file, loads the JSON and uses the listing `id` (if present) or the filename (without extension)
    as the MongoDB `_id` to ensure uniqueness.
  - Performs upsert replace operations in batches for efficiency.
"""
import glob
import json
import os
import sys
from pymongo import MongoClient, ReplaceOne


LISTINGS_DIR = "listings"
DB_NAME = os.environ.get("MONGO_DB", "rentsightlistings")
COLLECTION_NAME = os.environ.get("MONGO_COLLECTION", "listings")
# MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
MONGO_URI = 'mongodb+srv://amunim_db_user:oluDyD9UrXmNOF3c@rentsight.pxc0yaz.mongodb.net/'
BATCH_SIZE = 500


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def make_doc_id(doc, filename):
    # prefer an existing id field if it's present
    def to_safe_bson_id(val):
        # Mongo/BSON supports 64-bit signed integers. If the value is outside
        # that range, return it as a string to avoid overflow.
        try:
            n = int(val)
        except Exception:
            return str(val)

        if -(1 << 63) <= n <= (1 << 63) - 1:
            return n
        return str(val)

    for key in ("_id", "id", "listing_id"):
        if key in doc:
            return to_safe_bson_id(doc[key])
    # fallback to filename without extension (string)
    return os.path.splitext(os.path.basename(filename))[0]


def main():
    files = sorted(glob.glob(os.path.join(LISTINGS_DIR, "*.json")))
    if not files:
        print(f"No JSON files found in {LISTINGS_DIR}/")
        sys.exit(1)

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    coll = db[COLLECTION_NAME]

    ops = []
    total = 0
    for path in files:
        try:
            doc = load_json(path)
        except Exception as e:
            print(f"Skipping {path}: failed to load JSON: {e}")
            continue

        _id = make_doc_id(doc, path)
        doc_copy = dict(doc)
        doc_copy["_id"] = _id

        ops.append(ReplaceOne({"_id": _id}, doc_copy, upsert=True))

        if len(ops) >= BATCH_SIZE:
            result = coll.bulk_write(ops)
            total += len(ops)
            print(f"Upserted batch of {len(ops)} (matched={result.matched_count}, upserted={len(result.upserted_ids)})")
            ops = []

    if ops:
        result = coll.bulk_write(ops)
        total += len(ops)
        print(f"Upserted final batch of {len(ops)} (matched={result.matched_count}, upserted={len(result.upserted_ids)})")

    print(f"Imported/updated {total} documents into {DB_NAME}.{COLLECTION_NAME}")


if __name__ == "__main__":
    main()
