'''
Simulated annealing based optimser for the van layout.

Unlike v0.2, where the first available location found is the final location of an item,
simulated annealing iterates through multiple potential layouts, accepting invalid layouts (with a low score) in order to find new valid solutions.
'''

import math
import random

from van_layout.geometry import Item, Van, space_utilisation
from van_layout.mass_balance import balance_score


def objective(items: list[Item], van: Van) -> float:
    # Calculate the score for a single layout, where a higher score indicates a better layout

    # Positive: Area Utilised.
    score = space_utilisation(items, van) + balance_score(items, van)

    # Negative: Area overlap between items.
    score -= overlap_penalty * (total_overlap_area(items) / van.area)

    # Negative: Items out of bounds.
    score -= out_of_bounds_penalty * count_out_of_bounds(items, van)

    return score