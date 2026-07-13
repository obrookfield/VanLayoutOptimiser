'''
First fit decreasing algorithm for placing items in a van layout.

Sort items largest-first, then place each item in the first available position that fits.
'''

from van_layout import Item, Van, overlaps, in_bounds

def sort_by_area_descending(items: list[Item]) -> list[Item]:
    # Returns a new list of items sorted by largest area, descending.
    return sorted(items, key=lambda item: item.area, reverse=True)

def fits_at(item: Item, x: float, y: float, van: Van, placed_items: list[Item]) -> bool:
    # Check if the item can be placed at (x, y) without overlapping or going out of bounds.
    # Temporarily place the item, rather than mutating the original item coordinates.
    original_x, original_y = item.x, item.y
    item.x, item.y = x, y

    # Returns True if both in bounds and does not overlap
    fits = in_bounds(item, van) and not any(overlaps(item, placed_item) for placed_item in placed_items)

    item.x, item.y = original_x, original_y  # Restore original coordinates

    return fits



def place_items(items: list[Item], van: Van, step: float = 50) -> None:
    # Place items in the van using a simple greedy algorithm.
    # Items are placed in order of largest area first, starting from the bottom left corner, moving right and then up
    placed: list[Item] = []
    unplaced: list[Item] = []

    for item in sort_by_area_descending(items):
        placed_successfully = False
        y = 0.0

        while y + item.width <= van.width and not placed_successfully:
            x = 0.0
            while x + item.length <= van.length and not placed_successfully:
                if fits_at(item, x, y, van, placed):
                    item.x, item.y = x, y
                    placed.append(item)
                    placed_successfully = True
                x += step
            y += step

        if not placed_successfully:
            unplaced.append(item)

    return placed, unplaced