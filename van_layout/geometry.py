# 2D geometry for van layout.

from dataclasses import dataclass


@dataclass
class Item:
    # A single rectangular item to be placed in the van.

    name: str
    width: float
    length: float
    mass: float = 0.0
    x: float | None = None
    y: float | None = None


    @property
    def placed(self) -> bool:
        # Return True if the item has been placed in the van.
        return self.x is not None and self.y is not None


    @property
    def area(self) -> float:
        # Calculate the 2D footprint of the item.
        return self.width * self.length


    def bounds(self) -> tuple[float, float, float, float]:
        # Return the bounding box of the item as (x_min, y_min, x_max, y_max).
        if not self.placed:
            raise ValueError(f"'{self.name}' has not been placed.")
        return(self.x, self.y, self.x + self.length, self.y + self.width)


@dataclass
class Van:
    # The useable internal floor space of the van, represented as a rectangle.

    length: float
    width: float

    @property
    def area(self) -> float:
        return self.width * self.length


def in_bounds(item: Item, van: Van) -> bool:
    # Check if the item is within the bounds of the van.
    x_min, y_min, x_max, y_max = item.bounds()
    return x_min >= 0 and y_min >= 0 and x_max <= van.length and y_max <= van.width


def overlaps(a: Item, b: Item) -> bool:
    # Check if any items overlap.
    ax_min, ay_min, ax_max, ay_max = a.bounds()
    bx_min, by_min, bx_max, by_max = b.bounds()

    if ax_max <= bx_min or bx_max <= ax_min:
        return False
    if ay_max <= by_min or by_max <= ay_min:
        return False
    return True


def validate_layout(items: list[Item], van: Van) -> list[str]:
    # Check the placed layout for problems.
    # Returns a list of problem descriptions.

    problems = []

    # Check for items that have not been placed.
    for item in items:
        if not item.placed:
            problems.append(f"'{item.name}' has not been placed.")

    placed_items = [item for item in items if item.placed]

    # Check for items placed out of bounds.
    for item in placed_items:
        if not in_bounds(item, van):
            problems.append(f"'{item.name}' is out of bounds.")

    # Check for overlapping items.
    for i in range(len(placed_items)):
        for j in range(i+1, len(placed_items)):
            a, b = placed_items[i], placed_items[j]
            if overlaps(a,b):
                problems.append(f"'{a.name}' overlaps with '{b.name}'")

    return problems
