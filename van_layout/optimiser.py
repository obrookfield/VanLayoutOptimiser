'''
Simulated annealing based optimser for the van layout.

Unlike v0.2, where the first available location found is the final location of an item,
simulated annealing iterates through multiple potential layouts, accepting invalid layouts (with a low score) in order to find new valid solutions.
'''

import math
import random

from van_layout.geometry import Item, Van, space_utilisation, total_overlap_area, count_out_of_bounds
from van_layout.mass_balance import balance_score

overlap_penalty = 8.0
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


def random_move(items: list[Item], van: Van, progress: float, max_bump_size: float = 300) -> tuple[Item, float, float]:
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
        bump_size = max_bump_size * (1 - progress)
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


def simulated_annealing(
    items: list[Item],
    van: Van,
    iterations: int = 10000,
    start_temp: float = 1.0,
    end_temp: float = 0.001
    ) -> tuple[list[Item], float, list[float]]:
    
    # Search for an optimal layout by repeatedly proposing random moves of items.
    # Accept or reject moves based on a decreasing temperature.

    # Returns (items, best_score, score_history), positioned at the best found layout.

    current_score = objective(items, van)
    best_score = current_score
    best_positions = [(item.x, item.y) for item in items]
    score_history = [current_score]

    for i in range(iterations):
        # Exponential cooling, dropping from start temperature to end temperature.
        progress = i / (iterations - 1)
        temperature = start_temp * (end_temp / start_temp) ** progress

        # Generate a random move and calculate score.
        item, old_x, old_y = random_move(items, van, progress)
        new_score = objective(items, van)

        if should_accept(current_score, new_score, temperature):
            # Accept the new score if better than current score.
            current_score = new_score

            if new_score > best_score:
                best_score = new_score
                best_positions = [(item.x, item.y) for item in items]
        else:
            # Revert the move
            item.x, item.y = old_x, old_y

        score_history.append(current_score)

    # Finally put items in the positions in the best layout found.
    for item, (x, y) in zip(items, best_positions):
        item.x, item.y = x, y

    return items, best_score, score_history