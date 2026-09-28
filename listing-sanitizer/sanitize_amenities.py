import re
from utils import get_sanitized_directory, process_json_files

# ==============================================================================
# AMENITY NAME CLEANING
# ==============================================================================

# Known amenity names where the description gets glued to the name.
# Maps: raw concatenated prefix → clean amenity name
KNOWN_PREFIXES = {
    'Essentials': 'Essentials',
    'Kitchen': 'Kitchen',
    'Dedicated workspace': 'Dedicated workspace',
    'Cooking basics': 'Cooking basics',
    'Dishes and silverware': 'Dishes and silverware',
    'Private entrance': 'Private entrance',
    'Bed linens': 'Bed linens',
    'Building staff': 'Building staff',
    'Breakfast': 'Breakfast',
    'Pets allowed': 'Pets allowed',
    'Long term stays allowed': 'Long term stays allowed',
    'Elevator': 'Elevator',
    'Single level home': 'Single level home',
    'Host greets you': 'Host greets you',
    'Self check-in': 'Self check-in',
    'Lockbox': 'Lockbox',
    'Free washer': 'Free washer',
    'Free dryer': 'Free dryer',
    'Paid washer': 'Paid washer',
    'Paid dryer': 'Paid dryer',
    'Room-darkening shades': 'Room-darkening shades',
    'Outdoor furniture': 'Outdoor furniture',
    'Outdoor dining area': 'Outdoor dining area',
    'Security cameras': 'Security cameras',
    'Cleaning before checkout': 'Cleaning before checkout',
    'Luggage dropoff allowed': 'Luggage dropoff allowed',
    'Pack \'n play': 'Pack \'n play',
    'Children\'s books and toys': 'Children\'s books and toys',
    'High chair': 'High chair',
    'Window guards': 'Window guards',
    'Crib': 'Crib',
    'Baby safety gates': 'Baby safety gates',
    'Board games': 'Board games',
    'Babysitter recommendations': 'Babysitter recommendations',
    'Children\'s dinnerware': 'Children\'s dinnerware',
    'Baby bath': 'Baby bath',
    'Baby monitor': 'Baby monitor',
    'Changing table': 'Changing table',
}

# Sort by length (longest first) so longer prefixes match before shorter ones
_SORTED_PREFIXES = sorted(KNOWN_PREFIXES.keys(), key=len, reverse=True)


def clean_amenity_name(raw_name):
    """
    Clean a single amenity string by separating the name from its description.

    Examples:
      "EssentialsTowels, bed sheets, soap..."  →  "Essentials"
      "KitchenSpace where guests can cook..."  →  "Kitchen"
      "Dedicated workspaceIn a common space"   →  "Dedicated workspace"
      "Hair dryer"                             →  "Hair dryer"
      "45 inch HDTV with standard cable"       →  "45 inch HDTV with standard cable"
    """
    if not raw_name or not isinstance(raw_name, str):
        return raw_name

    # Try matching known prefixes
    for prefix in _SORTED_PREFIXES:
        if raw_name.startswith(prefix) and len(raw_name) > len(prefix):
            # Check that the character after the prefix is uppercase or not a space
            # (to distinguish "Kitchen" from "KitchenAid" vs "Kitchen and dining")
            rest = raw_name[len(prefix):]
            if rest[0].isupper() or rest[0].isdigit():
                return prefix
        elif raw_name == prefix:
            return prefix

    # Handle TV size pattern: "45 inch HDTV with standard cable" → keep as-is
    # Handle "X inch" pattern
    tv_match = re.match(r'(\d+"\s+\w+|\d+\s+inch\s+\w+.*)', raw_name)
    if tv_match:
        return raw_name

    # Generic fallback: detect camelCase-like boundary where a lowercase letter
    # is immediately followed by an uppercase letter mid-string
    # e.g. "SmokerSmoke allowed" — split at "rS"
    split = re.split(r'(?<=[a-z])(?=[A-Z])', raw_name, maxsplit=1)
    if len(split) == 2 and len(split[0]) > 3:
        return split[0]

    return raw_name


def clean_unavailable_item(raw_name):
    """
    Clean "Not included" items.

    Examples:
      "Unavailable: KitchenKitchen"        →  "Kitchen"
      "Unavailable: WasherWasher"          →  "Washer"
      "Unavailable: Smoke alarmSmoke alarm" →  "Smoke alarm"
      "Unavailable: Carbon monoxide alarmCarbon monoxide alarmThis place..." → "Carbon monoxide alarm"
    """
    if not raw_name or not isinstance(raw_name, str):
        return raw_name

    # Strip "Unavailable: " prefix
    text = re.sub(r'^Unavailable:\s*', '', raw_name)

    if not text:
        return raw_name

    # The name is duplicated: "KitchenKitchen" or "Smoke alarmSmoke alarm"
    # Try to find the longest prefix that repeats
    half = len(text) // 2
    for length in range(half + 5, 2, -1):
        candidate = text[:length]
        if text[length:].startswith(candidate):
            return candidate.strip()

    # If no duplication pattern found, just take the text before any description
    return clean_amenity_name(text)


def process_amenities(data, filename):
    """Sanitize amenities: clean names, separate available from unavailable."""
    raw_amenities = data.get('amenities')

    if not raw_amenities or not isinstance(raw_amenities, dict):
        data['amenities'] = []
        return data

    available = []
    not_included = []

    for category, items in raw_amenities.items():
        if not isinstance(items, list):
            continue

        if category == 'Not included':
            for item in items:
                cleaned = clean_unavailable_item(item)
                if cleaned and cleaned not in not_included:
                    not_included.append(cleaned)
        else:
            for item in items:
                cleaned = clean_amenity_name(item)
                if cleaned and cleaned not in available:
                    available.append(cleaned)

    # Store as a flat sorted list of available amenities only
    # (not-included items are dropped — they indicate what's missing, not what's present)
    data['amenities'] = sorted(available)

    return data


if __name__ == "__main__":
    dir_to_sanitize = get_sanitized_directory()
    process_json_files(dir_to_sanitize, process_amenities, "Amenities sanitization")
