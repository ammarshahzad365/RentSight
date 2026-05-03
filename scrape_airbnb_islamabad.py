"""
scrape_airbnb_islamabad.py
----------------------------------

This script demonstrates how one might use Selenium WebDriver to automate
the collection of listing data from Airbnb for stays in Islamabad.  It
implements the general process followed manually during research:

  1. Navigate to the search results page for the desired date range.
  2. Wait for listings to load and then iterate through each result card.
  3. Open each listing in a new tab, wait for the JavaScript to load the
     property page, and extract details such as title, pricing, capacity,
     amenity highlights, and rating breakdown.
  4. Append the collected information to a list of dictionaries and
     optionally save the results to a JSON file.

Important considerations:

• This script is provided for educational purposes only.  Before running any
  automated scraping on Airbnb, you must review their Terms of Service to
  ensure that your actions comply.  Many websites prohibit or limit
  automated data collection, and violating those terms may result in
  account suspension or legal action.
• AirBnB’s interface is highly dynamic and subject to change.  The CSS
  selectors used here were based on the site structure at the time this
  script was written and may need to be updated in the future.
• The script uses explicit waits (via WebDriverWait) to allow pages to load
  fully.  Without these waits, the automation may attempt to read elements
  that have not yet rendered, leading to exceptions.
• You will need to install Selenium and download a compatible driver (e.g.
  chromedriver) and ensure it is available on your PATH.  See
  https://selenium.dev/documentation/ for setup details.
"""

import json
import time
import re
import sys
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Callable, Any
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from islamabad_sectors import lahore_areas, karachi_areas, islamabad_sectors, faisalabad_areas


# ─────────────────────────────────────────────────────────────────────────────
# City → bounding-box list resolver
# Add a new city here by inserting another elif branch.
# ─────────────────────────────────────────────────────────────────────────────

CITY_SEARCH_NAMES: dict[str, str] = {
    "islamabad": "Islamabad--Pakistan",
    "lahore":    "Lahore--Pakistan",
    "karachi":   "Karachi--Pakistan",
    "faisalabad": "Faisalabad--Pakistan",
}


def get_areas(city: str) -> list:
    """Return the bounding-box list for *city* (case-insensitive).

    Raises ValueError for unknown cities so the caller gets a clear message.
    To add a new city (e.g. Faisalabad) just add its data list to
    islamabad_sectors.py, import it here, insert an elif branch below, and
    add its Airbnb search slug to CITY_SEARCH_NAMES above.
    """
    city = city.lower().strip()
    if city == "islamabad":
        return islamabad_sectors
    elif city == "lahore":
        return lahore_areas
    elif city == "karachi":
        return karachi_areas
    elif city == "faisalabad":
        return faisalabad_areas
    else:
        raise ValueError(
            f"Unknown city '{city}'. Supported cities: {', '.join(CITY_SEARCH_NAMES)}"
        )

# Global set of listing IDs already scraped (loaded once at import)
EXISTING_LISTING_IDS: set[str] = set()

# Retry window (seconds) before giving up on a failed page or coords run
RETRY_WINDOW_SECONDS = 5 * 60

def _init_existing_ids(directory: str = "listings") -> None:
    """Populate EXISTING_LISTING_IDS from filenames in listings directory.

    Filenames formatted as <listing_id>_<date>.json. We only need the ID part.
    """
    path = Path(directory)
    if not path.exists():
        return
    for file in path.glob("*.json"):
        stem = file.stem
        if "_" in stem:
            listing_id = stem.rsplit("_", 1)[0]
            if listing_id:
                EXISTING_LISTING_IDS.add(listing_id)

# _init_existing_ids() is called inside scrape_islamabad_listings() once the
# city (and therefore the listings directory) is known.

@dataclass
class Review:
    review_id: str
    metadata: str
    text: str

    def __repr__(self):
        return f"Review(id={self.review_id}, metadata={self.metadata[:30]}..., text={self.text[:30]}...)"


@dataclass
class Listing:
    """Container for details about an Airbnb listing."""

    id: str
    title: str
    listing_type: str
    room_type: str
    price: str
    max_guests: Optional[int]
    bedrooms: Optional[int]
    beds: Optional[int]
    baths: Optional[float]
    rating_overall: Optional[float]
    rating_cleanliness: Optional[float]
    rating_accuracy: Optional[float]
    rating_checkin: Optional[float]
    rating_communication: Optional[float]
    rating_location: Optional[float]
    rating_value: Optional[float]
    reviews: List[Review] = None  # Optional, can be populated later
    amenities: Optional[Dict[str, List[str]]] = None  # Section -> list of amenities
    url: str = None
    checkin_date: str = None  # Check-in date in YYYY-MM-DD format
    checkout_date: str = None  # Check-out date in YYYY-MM-DD format
    search_date: str = None  # Date when this listing was scraped
    search_coords: Optional[str] = None  # Coords string used for the map search that found this listing
    # Google Maps derived data (added via injected hook script)
    map_init_center: Optional[dict] = None      # {lat: float, lng: float}
    map_idle_center: Optional[dict] = None      # {lat: float, lng: float}
    map_idle_bounds: Optional[dict] = None      # {sw: {lat,lng}, ne: {lat,lng}}


def extract_listing_id(url: str) -> str:
    """Extract the Airbnb numeric/slug listing id between '/rooms/' and a following '?' if present."""
    try:
        match = re.search(r"/rooms/([^/?#]+)", url)
        if match:
            return match.group(1)
        # Fallback to last path segment without query
        return url.rstrip("/").split("/")[-1].split("?")[0]
    except Exception:
        return url


def parse_listing_details(
    driver: webdriver.Chrome, checkin: str, checkout: str, search_coords: Optional[str] = None
) -> Optional[Listing]:
    """
    Given a WebDriver instance and the URL of a listing, this function
    assumes the listing page is already loaded in the current tab, waits 
    for the content to load, and extracts relevant details. If any required 
    elements are not found, the function returns None.
    """
    # The listing page should already be loaded in the current tab
    # No need to call driver.get(url) anymore

    try:
        # Wait until the title appears; this indicates the page has loaded.
        title_el = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        title = title_el.text.strip()
        time.sleep(5)
        try: 
            close_el = driver.find_element(By.CSS_SELECTOR, 'button[aria-label=Close]')
            if close_el:
                close_el.click()
        except Exception:
            print("No initial close button found or clickable.")

        # Initialize containers that may be populated later
        amenities: Optional[Dict[str, List[str]]] = None

        # Extract listing id from the URL path, stripping any query params.
        url = driver.current_url
        listing_id = extract_listing_id(url)
        # If we've already scraped this listing ID (any day), skip heavy parsing.
        if listing_id in EXISTING_LISTING_IDS:
            print(f"Skip parse: listing {listing_id} already exists.")
            return None
        # Inject Google Maps hook script (captures map init center, idle center & bounds)
        try:
            hook_script = r"""
            (() => {
                if (window.__gmapsHookInstalled) return; // prevent double install
                window.__gmapsHookInstalled = true;
                const store = window._gmapsHookData = {
                    markerInits: [],
                    markerSetPositions: [],
                    markerPositionChanged: [],
                    mapInitCenter: null,
                    mapIdleCenter: null,
                    mapIdleBounds: null,
                    mapFitBounds: []
                };
                const log = (type, payload) => {
                    try { store.lastEvent = { type, ts: Date.now(), payload }; } catch {}
                };
                let patched = false;
                function patchOnce() {
                    if (patched || !window.google?.maps) return false;
                    const { maps } = google;
                    if (!maps.Marker || !maps.Map) return false;
                    // Patch Marker
                    const OriginalMarker = maps.Marker;
                    function PatchedMarker(opts = {}) {
                        try {
                            const p = opts.position;
                            if (p) {
                                const lat = typeof p.lat === 'function' ? p.lat() : p.lat;
                                const lng = typeof p.lng === 'function' ? p.lng() : p.lng;
                                store.markerInits.push({ lat, lng, title: opts.title || '' });
                                log('marker_init', { lat, lng });
                            }
                        } catch {}
                        const m = new OriginalMarker(opts);
                        const _setPosition = m.setPosition;
                        m.setPosition = function(pos) {
                            try {
                                const lat = typeof pos.lat === 'function' ? pos.lat() : pos.lat;
                                const lng = typeof pos.lng === 'function' ? pos.lng() : pos.lng;
                                store.markerSetPositions.push({ lat, lng });
                                log('marker_setPosition', { lat, lng });
                            } catch {}
                            return _setPosition.call(this, pos);
                        };
                        try {
                            maps.event.addListener(m, 'position_changed', () => {
                                try {
                                    const pos = m.getPosition?.();
                                    if (pos) {
                                        const lat = pos.lat();
                                        const lng = pos.lng();
                                        store.markerPositionChanged.push({ lat, lng });
                                        log('marker_position_changed', { lat, lng });
                                    }
                                } catch {}
                            });
                        } catch {}
                        return m;
                    }
                    PatchedMarker.prototype = OriginalMarker.prototype;
                    Object.setPrototypeOf(PatchedMarker, OriginalMarker);
                    maps.Marker = PatchedMarker;
                    // Patch Map
                    const OriginalMap = maps.Map;
                    function PatchedMap(el, opts = {}) {
                        try {
                            if (opts.center) {
                                const c = opts.center;
                                const lat = typeof c.lat === 'function' ? c.lat() : c.lat;
                                const lng = typeof c.lng === 'function' ? c.lng() : c.lng;
                                store.mapInitCenter = { lat, lng };
                                log('map_init_center', { lat, lng, zoom: opts.zoom });
                            }
                        } catch {}
                        const map = new OriginalMap(el, opts);
                        try {
                            maps.event.addListenerOnce(map, 'idle', () => {
                                try {
                                    const center = map.getCenter?.();
                                    const b = map.getBounds?.();
                                    if (center) {
                                        store.mapIdleCenter = { lat: center.lat(), lng: center.lng() };
                                        log('map_idle_center', store.mapIdleCenter);
                                    }
                                    if (b) {
                                        const sw = b.getSouthWest?.();
                                        const ne = b.getNorthEast?.();
                                        if (sw && ne) {
                                            store.mapIdleBounds = {
                                                sw: { lat: sw.lat(), lng: sw.lng() },
                                                ne: { lat: ne.lat(), lng: ne.lng() }
                                            };
                                            log('map_idle_bounds', store.mapIdleBounds);
                                        }
                                    }
                                } catch {}
                            });
                        } catch {}
                        try {
                            const _setCenter = map.setCenter;
                            map.setCenter = function(pos) {
                                try {
                                    const lat = typeof pos.lat === 'function' ? pos.lat() : pos.lat;
                                    const lng = typeof pos.lng === 'function' ? pos.lng() : pos.lng;
                                    log('map_setCenter', { lat, lng });
                                } catch {}
                                return _setCenter.call(this, pos);
                            };
                        } catch {}
                        try {
                            const _fitBounds = map.fitBounds;
                            map.fitBounds = function(bounds, ...rest) {
                                try {
                                    const sw = bounds.getSouthWest?.();
                                    const ne = bounds.getNorthEast?.();
                                    if (sw && ne) {
                                        const center = { lat: (sw.lat() + ne.lat()) / 2, lng: (sw.lng() + ne.lng()) / 2 };
                                        store.mapFitBounds.push({
                                            sw: { lat: sw.lat(), lng: sw.lng() },
                                            ne: { lat: ne.lat(), lng: ne.lng() },
                                            center
                                        });
                                        log('map_fitBounds', store.mapFitBounds[store.mapFitBounds.length - 1]);
                                    }
                                } catch {}
                                return _fitBounds.call(this, bounds, ...rest);
                            };
                        } catch {}
                        return map;
                    }
                    PatchedMap.prototype = OriginalMap.prototype;
                    Object.setPrototypeOf(PatchedMap, OriginalMap);
                    maps.Map = PatchedMap;
                    patched = true;
                    log('patch_active', {});
                    return true;
                }
                if (patchOnce()) return;
                const pollStart = Date.now();
                const pollId = setInterval(() => {
                    if (patchOnce()) clearInterval(pollId);
                    if (Date.now() - pollStart > 25000) clearInterval(pollId);
                }, 50);
                const origCreateElement = document.createElement;
                document.createElement = function(tagName, opts) {
                    const el = origCreateElement.call(document, tagName, opts);
                    if (String(tagName).toLowerCase() === 'script') {
                        el.addEventListener('load', () => {
                            try {
                                if (el.src && /maps(\.googleapis)?\.com\/maps-api-v3|googleapis\.com\/maps/.test(el.src)) {
                                    patchOnce();
                                }
                            } catch {}
                        }, { once: true });
                    }
                    return el;
                };
                const mo = new MutationObserver(() => patchOnce());
                mo.observe(document.documentElement || document, { childList: true, subtree: true });
                setTimeout(() => mo.disconnect(), 30000);
            })();
            """
            driver.execute_script(hook_script)
        except Exception as _e:
            print(f"Failed to inject Google Maps hook script: {_e}")

        def get_rating(selector: str, by: str = By.CSS_SELECTOR) -> Optional[float]:
            try:
                element = driver.find_element(by, selector)
                text = element.text.strip()

                if "Rated" in text:
                    # Use regex to extract the rating after "Rated"
                    match = re.search(r'Rated\s+([0-5](?:\.\d)?)\s+out of 5', text)
                    if match:
                        return float(match.group(1))
                    return None
                else:
                    # Fallback to original logic: try converting full text to float
                    return float(text) if text else None

            except Exception:
                return None

        # Defaults when listing has no reviews
        rating_overall = rating_cleanliness = rating_accuracy = rating_checkin = None
        rating_communication = rating_location = rating_value = None
        reviews = []

        try:
            # Wait for the <a> element whose href contains both 'rooms' and 'review'
            link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'rooms') and contains(@href, 'review')]"))
            )

            # Click the element
            link.click()

            time.sleep(2)  # Allow time for modal to open
            rating_overall = get_rating("(//*[contains(text(), 'out of 5 from ')])[last()]", By.XPATH)
            rating_cleanliness = get_rating(
                "//*[contains(., 'out of 5 stars for cleanliness')]",
                By.XPATH
            )
            rating_accuracy = get_rating(
                "//*[contains(., 'out of 5 stars for accuracy')]",
                By.XPATH
            )
            rating_checkin = get_rating(
                "//*[contains(., 'out of 5 stars for check-in')]",
                By.XPATH
            )
            rating_communication = get_rating(
                "//*[contains(., 'out of 5 stars for communication')]",
                By.XPATH
            )
            rating_location = get_rating(
                "//*[contains(., 'out of 5 stars for location')]",
                By.XPATH
            )
            rating_value = get_rating(
                "//*[contains(., 'out of 5 stars for value')]",
                By.XPATH
            )

            def scroll_until_all_reviews_loaded(wait_time: float = 5.0, timeout: int = 30):
                try:
                    # Locate the scrollable review panel
                    panel = WebDriverWait(driver, timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="pdp-reviews-modal-scrollable-panel"]'))
                    )

                    prev_count = -1

                    while True:
                        # Get current children (reviews)
                        children = panel.find_elements(By.XPATH, "./*")
                        current_count = len(children)

                        # If count didn't change from last iteration, assume we're done
                        if current_count == prev_count:
                            print(f"Loaded {current_count} reviews.")
                            break

                        # Scroll the last child into view
                        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'end'});", children[-1])

                        # Wait for lazy loading to fetch more reviews
                        time.sleep(wait_time)

                        # Update count
                        prev_count = current_count

                except Exception as e:
                    print(f"Error during review loading: {e}")

            def extract_reviews() -> List[Review]:
                reviews_inner = []

                # Find all review divs
                review_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-review-id]')

                for element in review_elements:
                    try:
                        review_id = element.get_attribute('data-review-id')
                        children = element.find_elements(By.XPATH, "./div")

                        if len(children) >= 2:
                            metadata = children[0].text.strip()
                            text = children[1].text.strip()
                            reviews_inner.append(Review(review_id, metadata, text))
                    except Exception as e:
                        print(f"Error processing review: {e}")

                return reviews_inner
            scroll_until_all_reviews_loaded()
            reviews = extract_reviews()

            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Close"]'))
            )
            close_button.click()
        except Exception:
            print("No reviews link (or modal failed) — keep defaults: ratings None, reviews []")
            pass

        # Extract basic info (capacity, bedrooms, beds, baths)
        # Wait for the info items to be present before extracting them
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-section-id='OVERVIEW_DEFAULT_V2'] div[data-pageslot='true'] ol li"))
        )
        time.sleep(1)
        info_items = driver.find_elements(By.CSS_SELECTOR, "div[data-section-id='OVERVIEW_DEFAULT_V2'] div[data-pageslot='true'] ol li")
        max_guests = bedrooms = beds = baths = None
        
        def extract_first_number(text):
            """Extract the first number found in the text"""
            import re
            if 'dedicated' in text.lower():
                return 1
            numbers = re.findall(r'\d+(?:\.\d+)?', text)
            if numbers:
                try:
                    return float(numbers[0])
                except ValueError:
                    pass
            return None
        
        for item in info_items:
            text = item.text.lower()
            if "guest" in text:
                max_guests = extract_first_number(text)
            elif "bedroom" in text:
                bedrooms = extract_first_number(text)
            elif "bed" in text:
                beds = extract_first_number(text)
            elif "bath" in text:
                baths = extract_first_number(text)
        if not max_guests:
            max_guests_text_container = driver.find_elements(By.XPATH, "//div[contains(., 'guests maximum')]")[-1]
            if "guest" in max_guests_text_container.text.lower().split("\n")[-1] and max_guests_text_container.text.lower().endswith("maximum"):
                max_guests = extract_first_number(max_guests_text_container.text.lower().split("\n")[-1])
    
        # Find all "Show price breakdown" elements and click the last one
        break_down_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(., 'Show price breakdown')]"))
        )
        time.sleep(2)
        try:    
            # Click the last element in the list
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", break_down_elements[-1])
            driver.execute_script("arguments[0].click();", break_down_elements[-1])
        except Exception:
            try:
                # If the last element is not clickable, try the first one
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", break_down_elements[0])
                driver.execute_script("arguments[0].click();", break_down_elements[0])
            except Exception:
                print("No price breakdown button found or clickable. [0]")
                return None
        except Exception:
            print("No price breakdown button found or clickable. [-1]")
            return None
        
        time.sleep(2)  # Allow time for modal to open
        try:
            # Wait for the parent div to be present
            price_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Price details"]'))
            )
            
            # Get the third direct child of the element
            children = price_container.find_elements(By.XPATH, "./*")
            
            if len(children) >= 3:
                third_child = children[2]  # Index 2 for the 3rd child
                price = third_child.text.strip()
            else:
                price = ""
        except Exception as e:
            price = ""

        if not price:
            # New fallback logic: extract individual line prices and combine.
            try:
                wait = WebDriverWait(driver, 10)

                # Night(s) line (e.g., "2 nights x $79.00" price at right)
                nights_price_el = wait.until(EC.visibility_of_element_located((
                    By.XPATH,
                    "(//div[.//button[.//div[contains(., 'nights')]]]//span[starts-with(normalize-space(.), '$')])[1]"
                )))
                nights_price = nights_price_el.text.strip()

                # Airbnb service fee line (price at the right)
                service_fee_el = wait.until(EC.visibility_of_element_located((
                    By.XPATH,
                    "(//div[.//button[.//div[normalize-space()='Airbnb service fee']]]//span[starts-with(normalize-space(.), '$')])[1]"
                )))
                service_fee = service_fee_el.text.strip()

                # Total line
                total_price_el = wait.until(EC.visibility_of_element_located((
                    By.XPATH,
                    "//div[normalize-space()='Total']/following-sibling::span//span[starts-with(normalize-space(.), '$')]"
                )))
                total_price = total_price_el.text.strip()

                combined = f"{nights_price} | {service_fee} | {total_price}"
                if combined.count('$') >= 1:  # basic sanity check
                    price = combined
                    print(f"Fallback price (composed): {price}")
                else:
                    print("Fallback composed price missing expected currency symbol(s).")
            except Exception as e:
                print(f"Fallback price extraction (composed lines) failed: {e}")

        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Close"]'))
            ).click()
        except Exception as e:
            print(f"No price breakdown close button available or close button not found. Error: {e}")

        time.sleep(1)  # Allow time for modal to close
        # Listing and room type: may appear near the booking summary as "Entire home",
        # "Private room", etc.  We'll read the first list item in that section.
        try:
            # Wait for the room summary element to be present before extracting it
            room_summary_el = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h2[elementtiming='LCP-target']"))
            )
            room_summary = room_summary_el.text
            # Example: "Entire home · 4 guests · 2 bedrooms · 2 beds · 2 baths"
            parts = [p.strip() for p in room_summary.split(" in ")]
            listing_type = parts[0] if parts else ""
            room_type = listing_type  # For Airbnb, listing_type and room_type are often the same description.
        except Exception:
            listing_type = ""
            room_type = ""

        # Collect a handful of visible amenities from the highlights section.  The
        # full amenities list is loaded in a modal that would require extra
        # navigation.  Here we gather whatever is immediately visible.
        def click_show_all_amenities_button(driver, timeout=10):
            try:
                # XPath: find button containing both 'show all' and 'amenities' (case-insensitive)
                xpath = (
                    "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'show all') "
                    "and contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'amenities')]"
                )
                button = WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                driver.execute_script("arguments[0].click();", button)
                print("Clicked 'Show all amenities' button.")
            except Exception as e:
                print(f"Failed to click button: {e}")

        # Open amenities and extract structured data
        click_show_all_amenities_button(driver)
        time.sleep(2)  # Allow time for modal to open if it did
        amenities = None
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="What this place offers"]'))
            )
            time.sleep(2)  # Allow time for modal to open if it did
            amenities = driver.execute_script("""
                try {
                const result = {};
                const sections = document.querySelectorAll(
                    'div[aria-label="What this place offers"] section section > div'
                );

                sections.forEach(sec => {
                    // first child DIV inside the section
                    const firstDiv = Array.from(sec.children).find(el => el && el.tagName === 'DIV');
                    // any UL inside the section
                    const listUl = sec.querySelector('ul');

                    if (firstDiv && listUl) {
                    const key = (firstDiv.textContent || '').trim();
                    const values = Array.from(listUl.querySelectorAll('li'))
                        .map(li => (li.textContent || '').trim())
                        .filter(Boolean);

                    if (key) result[key] = values;
                    }
                });

                return result;
                } catch (e) {
                return { __error: String(e && e.message ? e.message : e) };
                }
            """)
            # Ensure we have a plain dict or set to None
            if amenities is not None and not isinstance(amenities, dict):
                amenities = None
        except Exception as e:
            print(f"Error extracting structured amenities: {e}")

        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(0.5)
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(0.5)
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(0.5)

        # Scroll to map section ('Where you\u2019ll be' / 'Where you\'ll be') using XPath variants to trigger map load
        try:
            map_section = None
            xpath_candidates = [
                # Handle curly apostrophe ’ (U+2019)
                "(//h2[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'where you’') and contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'll be')])[1]",
                # Straight apostrophe version
                "(//h2[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'where you\\'ll be')])[1]",
                # Fallback broader contains logic (mixed apostrophes)
                # Mixed apostrophes fallback (use concat to include single quote inside single-quoted XPath literal)
                "(//h2[contains(., 'Where you') and (contains(., '’ll be') or contains(., concat(\"'\", 'll be')))])",
            ]
            for xp in xpath_candidates:
                try:
                    el = driver.find_element(By.XPATH, xp)
                    if el:
                        map_section = el
                        break
                except Exception:
                    continue
            if map_section:
                driver.execute_script("""
                    arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});
                    // window.scrollBy(0, 800);  // scroll 200px more down
                """, map_section)
                time.sleep(5)  # Allow map & idle event to fire
            else:
                print("Map section element not found via provided XPaths.")
        except Exception as e:
            print(f"Scroll to map section failed: {e}")

        # Retrieve captured Google Maps data
        map_init_center = map_idle_center = map_idle_bounds = None
        try:
            data = driver.execute_script("return window._gmapsHookData || {};")
            map_init_center = data.get('mapInitCenter')
            map_idle_center = data.get('mapIdleCenter')
            map_idle_bounds = data.get('mapIdleBounds')
        except Exception as e:
            print(f"Failed to retrieve Google Maps hook data: {e}")
        
        # Get current date for search_date
        search_date = datetime.now().strftime("%Y-%m-%d")
        
        return Listing(
            id=listing_id,
            title=title,
            listing_type=listing_type,
            room_type=room_type,
            price=price,
            max_guests=max_guests,
            bedrooms=bedrooms,
            beds=beds,
            baths=baths,
            rating_overall=rating_overall,
            rating_cleanliness=rating_cleanliness,
            rating_accuracy=rating_accuracy,
            rating_checkin=rating_checkin,
            rating_communication=rating_communication,
            rating_location=rating_location,
            rating_value=rating_value,
            amenities=amenities,
            reviews=reviews,
            url=url,
            checkin_date=checkin,
            checkout_date=checkout,
            search_date=search_date,
            search_coords=search_coords,
            map_init_center=map_init_center,
            map_idle_center=map_idle_center,
            map_idle_bounds=map_idle_bounds,
        )
    except Exception as e:
        print(f"Error parsing listing details for {driver.current_url}.  This may be due to a change in the page structure or missing elements. {e}")
        _append_failed_listing_url(driver.current_url)
        return None


def load_existing_listing_index(directory: str = "listings") -> dict:
    """Read listing filenames only to build an index of (id -> set of scrape_dates).

    Filenames are expected in the form <listing_id>_<scrape_date>.json
    where scrape_date = YYYY-MM-DD.
    """
    index: dict[str, set[str]] = {}
    path = Path(directory)
    if not path.exists():
        return index
    for file in path.glob("*.json"):
        name = file.stem  # remove .json
        # Split from right only once to allow underscores in ID if ever
        if "_" not in name:
            continue
        listing_id, scrape_date = name.rsplit("_", 1)
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", scrape_date):
            index.setdefault(listing_id, set()).add(scrape_date)
    return index


def scrape_islamabad_listings(
    checkin: str,
    checkout: str,
    max_pages: int = 3,
    start_page: int = 1,
    skip_pages: Optional[List[int]] = None,
    coords: str = "",
    coords_index: Optional[int] = None,
    on_page_done: Optional[Callable[[int, str, int], None]] = None,
    city: str = "islamabad",
) -> List[Listing]:
    """
    Navigate through Airbnb search results for Islamabad and collect data
    for listings appearing in the specified number of result pages.  The
    check-in/check-out dates should be provided in YYYY-MM-DD format.
    """
    # Derive the city-specific listings directory (e.g. "listings-lahore")
    listings_dir = f"listings-{city.lower()}"
    # Populate the global skip-set from existing files in this city's dir
    _init_existing_ids(listings_dir)
    # Build lightweight index from filenames only (no JSON load)
    listing_index = load_existing_listing_index(listings_dir)
    print(f"Found {sum(len(v) for v in listing_index.values())} existing listing files in '{listings_dir}'")
    
    # Build search URL (1 guest by default to keep results broad)
    city_slug = CITY_SEARCH_NAMES.get(city.lower(), "Islamabad--Pakistan")
    search_url = (
        f"https://www.airbnb.com/s/{city_slug}/homes?checkin={checkin}"
        f"&checkout={checkout}&adults=1&zoom=15.5327873717292&search_by_map=true"
        f"&{coords}"
    )

    # Initialize WebDriver (Chrome is used here; adjust if using another browser)
    print("Initializing Chrome WebDriver...")
    
    # Set up Chrome options for better reliability
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--headless=new') 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")  # IMPORTANT
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-position=-2000,0")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    )
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.minimize_window()
    
    # Execute script to hide automation indicators
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    print("WebDriver initialized successfully")
    
    # Set viewport to XL screen size (1920x1080)
    print("Setting window size...")
    driver.set_window_size(1920, 1080)
    print("Window size set")
    
    collected: List[Listing] = []  # New listings scraped this run

    try:
        print(f"Navigating to search URL: {search_url}")
        driver.get(search_url)
        print("Successfully loaded search page")

        # Allow time for listings to load
        print("Waiting for page to load...")
        time.sleep(5)
        print("Page load wait completed")

        # Try to find and click 'Got it' button, but continue if not found
        print("Looking for 'Got it' button...")
        try:
            element = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//*[text()='Got it']"))
            )
            element.click()
            print("Clicked 'Got it' button")
        except Exception:
            print("'Got it' button not found or not clickable within 15 seconds, continuing...")

        # Start from the requested page (default 1).  If start_page > 1,
        # advance the pagination by clicking "Next" until we reach it
        current_page = 1
        if start_page and start_page > 1:
            print(f"Advancing to start page {start_page}...")
            for _ in range(start_page - 1):
                try:
                    print("Looking for 'Got it' button...")
                    try:
                        element = WebDriverWait(driver, 15).until(
                            EC.element_to_be_clickable((By.XPATH, "//*[text()='Got it']"))
                        )
                        element.click()
                        print("Clicked 'Got it' button")
                    except Exception:
                        print("'Got it' button not found or not clickable within 15 seconds, continuing...")
                    next_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Next']"))
                    )
                    next_btn.click()
                    current_page += 1
                    if on_page_done is not None and coords_index is not None:
                        on_page_done(coords_index, coords, current_page)
                    time.sleep(5)
                except Exception:
                    print(f"Unable to advance to page {_ + 2}; stopping advance loop.")
                    break

        # Normalize skip_pages to a set for fast membership tests
        skip_pages_set = set(skip_pages or [])

        while current_page <= max_pages:
            deadline = time.monotonic() + RETRY_WINDOW_SECONDS
            page_finished = False
            no_more_pages = False
            while not page_finished and not no_more_pages and time.monotonic() < deadline:
                try:
                    # If this page is requested to be skipped, jump to the next page
                    if current_page in skip_pages_set:
                        print(f"Skipping page {current_page} per skip_pages parameter")
                        print("Looking for 'Got it' button...")
                        try:
                            element = WebDriverWait(driver, 15).until(
                                EC.element_to_be_clickable((By.XPATH, "//*[text()='Got it']"))
                            )
                            element.click()
                            print("Clicked 'Got it' button")
                        except Exception:
                            print("'Got it' button not found or not clickable within 15 seconds, continuing...")
                        next_btn = WebDriverWait(driver, 15).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Next']"))
                        )
                        next_btn.click()
                        current_page += 1
                        if on_page_done is not None and coords_index is not None:
                            on_page_done(coords_index, coords, current_page)
                        time.sleep(5)
                        page_finished = True
                        break
                    # Find all listing cards on the page
                    # cards = driver.find_elements(By.XPATH, "//a[starts-with(@href, '/rooms/')]")
                    cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='listing-card-title']")

                    # Store the current window handle (search results page)
                    main_window = driver.current_window_handle

                    for i, card in enumerate(cards):
                        try:
                            # Re-find the card element to avoid stale element reference
                            try:
                                current_cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='listing-card-title']")
                                if i < len(current_cards):
                                    current_card = current_cards[i]
                                else:
                                    continue
                            except Exception:
                                continue

                            # Click the card to open it in a new tab
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", current_card)
                            size = current_card.size
                            center_x = size['width'] // 2
                            center_y = size['height'] // 2
                            ActionChains(driver).move_to_element_with_offset(current_card, center_x, center_y).click().perform()
                            ActionChains(driver).move_by_offset(-center_x, -center_y).perform()
                            time.sleep(2)
                            all_windows = driver.window_handles
                            new_window = None
                            for window in all_windows:
                                if window != main_window:
                                    new_window = window
                                    break
                            if new_window:
                                driver.switch_to.window(new_window)
                                listing_data = parse_listing_details(
                                    driver, checkin, checkout, search_coords=coords
                                )
                                if listing_data:
                                    scrape_date = listing_data.search_date
                                    existing_dates = listing_index.get(listing_data.id, set())
                                    if scrape_date in existing_dates:
                                        print(f"Already have {listing_data.id} for {scrape_date}, skipping save.")
                                    else:
                                        collected.append(listing_data)
                                        listing_index.setdefault(listing_data.id, set()).add(scrape_date)
                                        out_dir = Path(listings_dir)
                                        out_dir.mkdir(parents=True, exist_ok=True)
                                        filename = out_dir / f"{listing_data.id}_{scrape_date}.json"
                                        try:
                                            with open(filename, "w", encoding="utf-8") as f:
                                                json.dump(asdict(listing_data), f, ensure_ascii=False, indent=2)
                                            saved_count = len(list(out_dir.glob("*.json")))
                                            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                            print(f"Saved listing to {filename} (total saved: {saved_count}) [{now}]")
                                            EXISTING_LISTING_IDS.add(listing_data.id)
                                        except Exception as e:
                                            print(f"Failed to save listing {listing_data.id}: {e}")
                                driver.close()
                                driver.switch_to.window(main_window)
                                time.sleep(1)
                        except Exception as e:
                            print(f"Error processing listing {driver.current_url}, {card.text}: {e}")
                            try:
                                driver.switch_to.window(main_window)
                            except Exception:
                                pass
                            continue

                    # Try to navigate to the next page by clicking the Next button.
                    try:
                        next_btn = driver.find_element(By.CSS_SELECTOR, "a[aria-label='Next']")
                        next_btn.click()
                        current_page += 1
                        if on_page_done is not None and coords_index is not None:
                            on_page_done(coords_index, coords, current_page)
                        time.sleep(5)
                        page_finished = True
                    except NoSuchElementException:
                        no_more_pages = True
                        page_finished = True
                except Exception as e:
                    if isinstance(e, NoSuchElementException):
                        no_more_pages = True
                        page_finished = True
                    else:
                        print(f"Page/coords error: {e}. Retrying for up to 5 mins...")
                        time.sleep(30)
            if no_more_pages:
                break
            if not page_finished:
                print("Giving up current page/coords after 5 mins of failures, moving on.")
                break

    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        print(f"Collected {len(collected)} listings before error occurred")
    finally:
        driver.quit()

    # Return only newly collected listings (existing ones were not loaded to memory)
    return collected


PROGRESS_FILENAME = "scrape_progress.json"
FAILED_LISTINGS_FILENAME = "failed_listings.json"


def _append_failed_listing_url(url: str, filepath: Optional[Path] = None) -> None:
    """Append a failed listing URL to failed_listings.json for later retry."""
    path = filepath or Path(FAILED_LISTINGS_FILENAME)
    try:
        data: Dict[str, list] = {"urls": []}
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data.get("urls"), list):
                data["urls"] = []
        if url not in data["urls"]:
            data["urls"].append(url)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to save failed listing URL to {path}: {e}")


def _load_progress(progress_path: Path, no_resume: bool, areas: list) -> tuple[int, str, int]:
    """Return (coords_index, coords_string, page) for FORWARD runner. If no_resume or no file, (0, first_coords, 1)."""
    if no_resume or not progress_path.exists():
        coords = areas[0] if areas else ""
        return (0, coords, 1)
    try:
        with open(progress_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        idx = int(data.get("forward_coords_index", data.get("coords_index", 0)))
        cs = data.get("forward_coords_string", data.get("coords_string", areas[0] if areas else ""))
        page = int(data.get("forward_page", data.get("page", 1)))
        return (max(0, idx), cs, max(1, page))
    except Exception:
        coords = areas[0] if areas else ""
        return (0, coords, 1)


def _load_reverse_progress(progress_path: Path, no_resume: bool, areas: list) -> tuple[int, str, int]:
    """Return (coords_index, coords_string, page) for REVERSE runner (end→first). If no resume, (len-1, last_coords, 1)."""
    n = len(areas)
    if n == 0:
        return (0, "", 1)
    last_coords = areas[n - 1]
    if no_resume or not progress_path.exists():
        return (n - 1, last_coords, 1)
    try:
        with open(progress_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        idx = data.get("reverse_coords_index")
        if idx is None:
            return (n - 1, last_coords, 1)
        idx = int(idx)
        cs = data.get("reverse_coords_string", areas[idx] if 0 <= idx < n else last_coords)
        page = int(data.get("reverse_page", 1))
        return (max(0, min(n - 1, idx)), cs, max(1, page))
    except Exception:
        return (n - 1, last_coords, 1)


def _save_progress_runner(
    progress_path: Path,
    runner: str,
    coords_index: int,
    coords_string: str,
    page: int,
    lock: Optional[Any] = None,
) -> None:
    """Save one runner's progress; merge with existing JSON so the other runner's data is kept. Optional lock for multiprocessing."""
    if lock is not None:
        lock.acquire()
    try:
        data: Dict = {}
        if progress_path.exists():
            try:
                with open(progress_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                pass
        prefix = "forward" if runner == "forward" else "reverse"
        data[f"{prefix}_coords_index"] = coords_index
        data[f"{prefix}_coords_string"] = coords_string
        data[f"{prefix}_page"] = page
        if runner == "forward":
            data["coords_index"] = coords_index
            data["coords_string"] = coords_string
            data["page"] = page
        with open(progress_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to save progress: {e}")
    finally:
        if lock is not None:
            lock.release()


def _save_progress(progress_path: Path, coords_index: int, coords_string: str, page: int, lock: Optional[Any] = None) -> None:
    """Save FORWARD runner progress. Merges with existing file so reverse progress is preserved."""
    _save_progress_runner(progress_path, "forward", coords_index, coords_string, page, lock)


def _save_reverse_progress(progress_path: Path, coords_index: int, coords_string: str, page: int, lock: Optional[Any] = None) -> None:
    """Save REVERSE runner progress. Merges with existing file so forward progress is preserved."""
    _save_progress_runner(progress_path, "reverse", coords_index, coords_string, page, lock)


def _run_runner_worker(
    runner: str,
    indices: List[int],
    first_start_page: int,
    checkin: str,
    checkout: str,
    max_pages: int,
    skip_pages_list: List[int],
    progress_path_str: str,
    lock: Any,
    city: str,
) -> None:
    """Worker run in a separate process: scrapes the given coords indices for one runner. Writes listings to disk and progress with lock."""
    # Prefix all print output in this process with the runner name
    import builtins
    _original_print = builtins.print
    _prefix = f"[{runner.upper()}]"

    def _prefixed_print(*args, **kwargs):
        if args:
            _original_print(_prefix, *args, **kwargs)
        else:
            _original_print(_prefix, **kwargs)

    builtins.print = _prefixed_print

    progress_path = Path(progress_path_str)
    areas = get_areas(city)
    n_sectors = len(areas)

    def make_on_page_done(runner_name: str) -> Callable[[int, str, int], None]:
        def on_page_done(ci: int, cs: str, p: int) -> None:
            if runner_name == "forward":
                _save_progress(progress_path, ci, cs, p, lock)
            else:
                _save_reverse_progress(progress_path, ci, cs, p, lock)
        return on_page_done

    for i, idx in enumerate(indices):
        coords = areas[idx]
        start_page = first_start_page if i == 0 else 1
        print(f"Scraping coords index {idx + 1}/{n_sectors} (start_page={start_page}): {coords[:60]}...")
        deadline = time.monotonic() + RETRY_WINDOW_SECONDS
        retry_start_page = start_page
        while time.monotonic() < deadline:
            try:
                scrape_islamabad_listings(
                    checkin,
                    checkout,
                    max_pages=max_pages,
                    start_page=retry_start_page,
                    skip_pages=skip_pages_list,
                    coords=coords,
                    coords_index=idx,
                    on_page_done=make_on_page_done(runner),
                    city=city,
                )
                break
            except Exception as e:
                print(f"Coords idx={idx} failed: {e}. Retrying...", file=sys.stderr)
                if runner == "forward":
                    saved_idx, _, saved_page = _load_progress(progress_path, no_resume=False, areas=areas)
                else:
                    saved_idx, _, saved_page = _load_reverse_progress(progress_path, no_resume=False, areas=areas)
                if saved_idx == idx:
                    retry_start_page = saved_page
                if time.monotonic() + 30 >= deadline:
                    break
                time.sleep(30)
        # Advance progress: forward goes +1, reverse goes -1
        if runner == "forward":
            next_idx = idx + 1
            next_cs = areas[next_idx] if next_idx < n_sectors else coords
            _save_progress(progress_path, next_idx, next_cs, 1, lock)
        else:
            next_idx = idx - 1
            next_cs = areas[next_idx] if next_idx >= 0 else coords
            _save_reverse_progress(progress_path, next_idx, next_cs, 1, lock)


if __name__ == "__main__":
    import argparse
    import multiprocessing

    parser = argparse.ArgumentParser(description="Scrape Airbnb listings for a Pakistan city")
    parser.add_argument(
        "--city",
        default="islamabad",
        choices=list(CITY_SEARCH_NAMES.keys()),
        help="City to scrape: islamabad, lahore, or karachi (default: islamabad)",
    )
    parser.add_argument("--checkin", default="2026-10-3", help="Check-in date YYYY-MM-DD")
    parser.add_argument("--checkout", default="2026-10-5", help="Check-out date YYYY-MM-DD")
    parser.add_argument("--max-pages", type=int, default=20, help="Maximum number of pages to traverse")
    parser.add_argument("--start-page", type=int, default=1, help="Page number to start from when not resuming (1-based)")
    parser.add_argument(
        "--skip-pages",
        type=str,
        help="Comma-separated list of page numbers to skip, e.g. '2,5,7' or ranges '4-6'",
    )
    parser.add_argument(
        "--progress-file",
        default=None,
        help="Path to progress file for resume (default: scrape_progress-{city}.json)",
    )
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Ignore saved progress and start from first coords, page 1",
    )

    args = parser.parse_args()

    # Resolve the bounding-box list for the chosen city
    areas = get_areas(args.city)

    # Parse skip_pages string into a list of ints (support ranges like 4-6)
    skip_pages_list: List[int] = []
    if args.skip_pages:
        for part in args.skip_pages.split(","):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                try:
                    a, b = part.split("-", 1)
                    a_i = int(a.strip())
                    b_i = int(b.strip())
                    if a_i <= b_i:
                        skip_pages_list.extend(list(range(a_i, b_i + 1)))
                except Exception:
                    continue
            else:
                try:
                    skip_pages_list.append(int(part))
                except Exception:
                    continue

    # Default progress file is city-scoped; can be overridden with --progress-file
    progress_file = args.progress_file or f"scrape_progress-{args.city}.json"
    progress_path = Path(progress_file)
    n_sectors = len(areas)
    if n_sectors == 0:
        print(f"No coords for city '{args.city}'.")
        sys.exit(0)

    print(f"City: {args.city} ({n_sectors} bounding-box entries)")

    # Load both runners: forward (first→end), reverse (end→first)
    forward_idx, _, forward_page = _load_progress(progress_path, args.no_resume, areas)
    reverse_idx, _, reverse_page = _load_reverse_progress(progress_path, args.no_resume, areas)
    if args.no_resume:
        forward_page = max(1, args.start_page)
        reverse_page = 1

    # Stop when they would surpass each other
    if forward_idx > reverse_idx:
        print("Runners already met (forward_idx > reverse_idx). Nothing to do.")
        sys.exit(0)

    # Partition work so they never double-scrape: when they meet at one coords, only forward does it.
    # Forward: indices [forward_idx .. reverse_idx] inclusive.
    # Reverse: indices [reverse_idx-1 .. forward_idx] descending (so reverse does not do reverse_idx).
    forward_indices: List[int] = list(range(forward_idx, reverse_idx + 1))
    reverse_indices: List[int] = list(range(reverse_idx - 1, forward_idx - 1, -1))  # reverse_idx-1 down to forward_idx

    if not forward_indices and not reverse_indices:
        print("No indices to scrape.")
        sys.exit(0)

    print(f"FORWARD runner: {len(forward_indices)} coords (indices {forward_idx}..{reverse_idx})")
    print(f"REVERSE runner: {len(reverse_indices)} coords (indices {reverse_idx-1}..{forward_idx})")
    print("Starting both runners simultaneously...")

    lock = multiprocessing.Lock()
    progress_path_str = str(progress_path.resolve())

    forward_process = multiprocessing.Process(
        target=_run_runner_worker,
        args=(
            "forward",
            forward_indices,
            forward_page,
            args.checkin,
            args.checkout,
            args.max_pages,
            skip_pages_list,
            progress_path_str,
            lock,
            args.city,
        ),
    )
    reverse_process = multiprocessing.Process(
        target=_run_runner_worker,
        args=(
            "reverse",
            reverse_indices,
            1,  # reverse first coords is reverse_idx-1; no per-coords resume for that
            args.checkin,
            args.checkout,
            args.max_pages,
            skip_pages_list,
            progress_path_str,
            lock,
            args.city,
        ),
    )

    forward_process.start()
    reverse_process.start()
    forward_process.join()
    reverse_process.join()

    if forward_process.exitcode != 0:
        print(f"FORWARD process exited with code {forward_process.exitcode}", file=sys.stderr)
    if reverse_process.exitcode != 0:
        print(f"REVERSE process exited with code {reverse_process.exitcode}", file=sys.stderr)
    print("Both runners finished.")