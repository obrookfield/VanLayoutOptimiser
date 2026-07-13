'''
Mass distribution and balance scoring for a van layout.

A poorly balanced layout, i.e. heavily lopsided load, can make the van difficult to drive, and can be dangerous.

Likewise, it can also increase tyre wear, reduce fuel efficiency, and in some jurisdictions, be illegal due to axle weight limits

This module scores how far a layout's centre of mass is from the van's geometric centre.

At this stage (v0.3), nothing is moved or optimised, only scored.
'''

from van_layout import Item, Van


def centre_of_mass(items: list[Item]) -> tuple[float, float]:
    # Average centre point of all placed items, weighted by mass.
    # Items with 0 mass contribute only their position in the van, and do not affect the centre of mass.

    placed_items = [item for item in items if item.placed]

    total_mass = sum(item.mass for item in placed_items)

    if total_mass == 0:
        raise ValueError("Total mass of placed items is zero, cannot compute centre of mass.")

    x_centre = sum(
        (item.x + item.length / 2) * item.mass for item in placed_items
    ) / total_mass

    y_centre = sum(
        (item.y + item.width / 2) * item.mass for item in placed_items
    ) / total_mass

    return x_centre, y_centre


def balance_offset(items: list[Item], van: Van) -> tuple[float, float]:
    # Calculate the offset of the centre of mass from the geometric centre of the van.
    
    x_com, y_com = centre_of_mass(items)

    van_x_centre = van.length / 2
    van_y_centre = van.width / 2

    # Normalised offsets from the centre, where 0 is perfectly balanced, and 1 is at the edge of the van.
    x_offset = (x_com - van_x_centre) / van_x_centre 
    y_offset = (y_com - van_y_centre) / van_y_centre

    return x_offset, y_offset