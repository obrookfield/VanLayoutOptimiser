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
    item.x = x
    item.y = y
    if not in_bounds(item, van):
        return False
    for placed_item in placed_items:
        if overlaps(item, placed_item):
            return False
    return True

