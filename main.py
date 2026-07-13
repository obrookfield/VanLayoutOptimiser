'''
v0.1
Hand-placed layout of items in a van.

There is no optimisation at this stage.

Defines a van, places items in it at predetermined locations, 
checks the layout is valid, and plots it.

Dimensions are in millimetres.
'''

from van_layout import Item, Van
from van_layout.geometry import validate_layout
from van_layout.placement import place_items
from van_layout.visualiser import plot_layout
from van_layout.mass_balance import balance_offset, balance_score

# Dimensions - VW Transporter SWB (2014-)
van = Van(length=2572, width=1700)

# Item defined by: (name, length, width)
items = [
    Item(name="Bed", length=2000, width=1100, mass=40),
    #Item(name="Twin Bed", length=1910, width=970, mass=36), # More accurate bed size, standard twin.
    Item(name="Kitchen Unit", length=500, width=500, mass=35),
    Item(name="Wardrobe", length=500, width=500, mass=20),
    Item(name="Fire Extinguisher", length=114, width=114, mass=2) # 2kg 3L 250 bar fire extinguisher.
    ]

if __name__ == "__main__":
    # Place items in the van.
    placed, unplaced = place_items(items, van)
    if unplaced:
        print("Could not place:")
        for u in unplaced:
            print(f"  - {u.name} ({u.length} x {u.width})")

    # Check the layout is valid.
    problems = validate_layout(items, van)
    if problems:
        print("Layout is invalid:")
        for p in problems:
            print(f"  - {p}")
    else:
        print("Layout is valid.")

        x_offset, y_offset = balance_offset(placed, van)
        print(f"Mass balance offset: front/back={x_offset:+.2f}, side/side={y_offset:+.2f}")
        print(f"Mass balance score: {balance_score(placed, van):.2f} (1.0 = perfectly balanced)")

    plot_layout(items, van, title="v0.2: Naive algorithm layout")