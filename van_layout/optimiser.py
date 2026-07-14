'''
Simulated annealing based optimser for the van layout.

Unlike v0.2, where the first available location found is the final location of an item,
simulated annealing iterates through multiple potential layouts, accepting invalid layouts (with a low score) in order to find new valid solutions.
'''

import math
import random

from van_layout.geometry import Item, Van, space_utilisation, total_overlap_area, count_out_of_bounds
from van_layout.mass_balance import balance_score

overlap_penalty = 5.0
out_of_bounds_penalty = 0.5


def objective(items: list[Item], van: Van) -> float:
    # Calculate the score for a single layout, where a higher score indicates a better layout

    # Positive: Area Utilised.
    score = space_utilisation(items, van) + balance_score(items, van)

    # Negative: Area overlap between items.
    score -= overlap_penalty * (total_overlap_area(items) / van.area)

    # Negative: Items out of bounds.
    score -= out_of_bounds_penalty * count_out_of_bounds(items, van)

    return score


def random_move(items: list[Item], van: Van, bump_size: float = 150) -> tuple[Item, float, float]:
    # Picks a random item then moves it at random, either a teleport to a completely new location, or a small step away from the current.

    # Pick a random item.
    item = random.choice(items)
    old_x, old_y = item.x, item.y
    
    max_x = van.length - item.length
    max_y = van.width - item.width

    if random.random() < 0.5:
        # Teleport to a random position in the van.
        # Useful for escaping local optima
        item.x = random.uniform(0, max_x)
        item.y = random.uniform(0, max_y)
    else:
        # Bump the item a small step from the current position.
        item.x = min(max(0, old_x + random.uniform(-bump_size, bump_size)), max_x)
        item.y = min(max(0, old_y + random.uniform(-bump_size, bump_size)), max_y)

    return item, old_x, old_y


def should_accept(old_score: float, new_score: float, temperature: float) -> bool:
    # Logic to determine whether a move should be accepted.
    # An improved move is always accepted, a worse move is accepted with a probability.
    # This probability is based on the temperature during simulated annealing, where a higher temperature means a worse move is more likely to be accepted.

    if new_score >= old_score:
        # Better move, always accepted
        return True

    if temperature <= 0:
        # Temperature is too small to accept a better move.
        return False

    # Calculate the criterion for a worse move to be accepted
    delta = old_score - new_score # +ive means worse
    probability = math.exp(-delta / temperature)

    return random.random() < probability