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


@dataclass
class Obstacle:
    # A fixed rectangular region within the van that must not have anything placed over it.
    # E.g. rear wheel arches, clearance for stepping in through the side door.

    name: str
    x: float
    y: float
    length: float
    width: float

    def bounds(self) -> tuple[float, float, float, float]:
        return (self.x, self.y, self.x + self.length, self.y + self.width)


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


def validate_layout(items: list[Item], van: Van, obstacles: list[Obstacle]) -> list[str]:
    # Check the placed layout for problems.
    # Returns a list of problem descriptions.

    obstacles = obstacles or [] # Include the obstacle regions.
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

    # Check for items overlapping the obstacle regions.
    for item in placed_items:
        for obstacle in obstacles:
            if overlaps(item, obstacle):
                problems.append(f"'{item.name}' overlaps with '{obstacle.name}'")

    # Check for overlapping items.
    for i in range(len(placed_items)):
        for j in range(i+1, len(placed_items)):
            a, b = placed_items[i], placed_items[j]
            if overlaps(a,b):
                problems.append(f"'{a.name}' overlaps with '{b.name}'")

    return problems


def space_utilisation(items: list[Item], van: Van) -> float:
    # Fraction of the van's floor space covered by placed items (0-1).
    used = sum(item.area for item in items if item.placed) / van.area

    return used


def overlap_area(a: Item, b: Item) -> float:
    # Area of overlap between two placed items, returns a value >= 0
    ax_min, ay_min, ax_max, ay_max = a.bounds()
    bx_min, by_min, bx_max, by_max = b.bounds()

    x_overlap = max(0.0, min(ax_max, bx_max) - max(ax_min, bx_min))
    y_overlap = max(0.0, min(ay_max, by_max) - max(ay_min, by_min))

    return x_overlap * y_overlap


def total_overlap_area(items: list[Item]) -> float:
    placed_items = [item for item in items if item.placed]

    total = 0.0
    for i in range(len(placed_items)):
        for j in range(i+1, len(placed_items)):
            total += overlap_area(placed_items[i], placed_items[j])

    return total


def total_obstacle_overlap_area(items: list[Item], obstacles: list[Obstacle]) -> float:
    placed_items = [item for item in items if item.placed]

    total = 0.0
    for item in placed_items:
        for obstacle in obstacles:
            total += overlap_area(item, obstacle)

    return total


def count_overlaps(items: list[Item]) -> int:
    # Number of pairs of placed item that overlap each other.
    placed_items = [item for item in items if item.placed]

    count = 0
    for i in range(len(placed_items)):
        for i in range(len(placed_items)):
            for j in range(i+1, len(placed_items)):
                if overlaps(placed_items[i], placed_items[j]):
                    count += 1

    return count


def count_out_of_bounds(items: list[Item], van: Van) -> int:
    # Number of items that are outside the bounds of the van.
    return sum(1 for item in items if item.placed and not in_bounds(item, van))