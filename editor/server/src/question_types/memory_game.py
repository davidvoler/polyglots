import random
from typing import List, Any


def create_memory_game(elements: List[Any], width: int = 8, height: int = 8) -> List[List[Any]]:
    """
    Build a memory-game grid where each element appears exactly twice.
    Raises ValueError if the grid size cannot fit the pairs.
    """
    if not elements:
        raise ValueError("elements must not be empty")

    total_cells = width * height
    required = len(elements) * 2
    if total_cells != required:
        raise ValueError(
            f"Grid {width}x{height} has {total_cells} cells, but {required} needed for pairs"
        )

    pool = list(elements) * 2  # two of each element
    random.shuffle(pool)

    grid = []
    idx = 0
    for _ in range(height):
        row = pool[idx : idx + width]
        grid.append(row)
        idx += width

    return grid


if __name__ == "__main__":
    sample = ["A", "B", "C", "D","E","F","G","H"]
    g = create_memory_game(sample, width=4, height=4)
    for row in g:
        print(row)
