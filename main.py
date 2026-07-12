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
from van_layout.visualiser import plot_layout

# Dimensions
van = Van(length=2500, width=1600)

items = [
    Item(name="Bed", length=2000, width=1100, x=0, y=0),
    Item(name="Kitchen Unit", length=500, width=500, x=2000, y=0),
    Item(name="Wardrobe", length=500, width=500, x=2000, y=500)
    ]

if __name__ == "__main__":
    # Check the layout is valid.
    problems = validate_layout(items, van)

    if problems:
        print("Layout is invalid:")
        for p in problems:
            print(f"  - {p}")
    else:
        print("Layout is valid.")

    plot_layout(items, van, title="v0.1: Hand-placed layout")