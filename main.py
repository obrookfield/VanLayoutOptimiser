'''
v0.1
Hand-placed layout of items in a van.

There is no optimisation at this stage.

Defines a van, places items in it at predetermined locations, 
checks the layout is valid, and plots it.

Dimensions are in millimetres.
'''

import random
random.seed(1)

from van_layout import Item, Van, Obstacle
from van_layout.geometry import space_utilisation, validate_layout
from van_layout.mass_balance import balance_offset, balance_score
from van_layout.optimiser import objective, simulated_annealing
from van_layout.placement import place_items
from van_layout.visualiser import plot_layout

# Dimensions - VW Transporter SWB (2014-)
van = Van(length=2572, width=1700)

# Obstructions, defined by: (name, length, width, x, y)
obstacles = [
    Obstacle(name="Wheel Arch (L)", length=300, width=180, x=2100, y=0),
    Obstacle(name="Wheel Arch (R)", length=300, width=180, x=2100, y=1520),
    Obstacle(name="Sliding Door Clearance", length=700, width=150, x=700, y=0)
    ]

# Item defined by: (name, length, width)
items = [
    Item(name="Twin Bed", length=1910, width=970, mass=36), # More accurate bed size, standard twin.
    Item(name="Kitchen Unit", length=1000, width=500, mass=40),
    Item(name="Wardrobe", length=600, width=500, mass=35),
    Item(name="Fire Extinguisher", length=114, width=114, mass=2), # 2kg 3L 250 bar fire extinguisher.
    Item(name="Foldable Table", length=800, width=600, mass=10),
    Item(name="Storage Box A", length=600, width=400, mass=20),
    Item(name="Storage Box B", length=600, width=400, mass=20)

    #Item(name="Mini Fridge", length=450, width=480, mass=15),
    #Item(name="Kitchen Cabinet", length=1000, width=500, mass=40),
    #Item(name="Fresh Water Tank (50L)", length=600, width=400, mass=50),
    #Item(name="Grey Water Tank (Empty)", length=600, width=400, mass=5),
    #Item(name="Shower Tray", length=700, width=700, mass=10),
    #Item(name="Propane Gas Bottle", length=300, width=300, mass=15),
    
    ]


def report(label: str, layout: list[Item], obstructions= list[Obstacle]) -> None:
    # Check the layout is valid.
    problems = validate_layout(layout, van, obstructions)
    print(f"--- {label} ---")
    if problems:
        print("Layout is invalid:")
        for p in problems:
            print(f"  - {p}")
        return
    
    print("Layout is valid.")
    x_offset, y_offset = balance_offset(layout, van)
    print(f"Space Utilisation: {space_utilisation(layout, van):.1%}")
    print(f"Mass balance offset: front/back={x_offset:+.2f}, side/side={y_offset:+.2f}")
    print(f"Mass balance score: {balance_score(layout, van):.2f} (0.0 = perfectly balanced)")


if __name__ == "__main__":
    # First Fit Placement
    # Place items in the van.
    placed, unplaced = place_items(items, van, obstacles)
    if unplaced:
        print("Could not place:")
        for u in unplaced:
            print(f"  - {u.name} ({u.length} x {u.width})")

    report("v0.2: First Fit Placement", placed, obstacles)
    plot_layout(items, van, title="v0.2: First Fit Placement")

    print()

    # Simulated Annealing Placement
    optimised, best_score, history = simulated_annealing(placed, van, obstacles)

    report("v0.4: Simulated Annealing", optimised, obstacles)
    plot_layout(optimised, van, title="v0.5: Simulated Annealing w/ Obstructions")