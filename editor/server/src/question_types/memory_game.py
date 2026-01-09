import random
from typing import List, Any


def create_memory_game(elements: List[Any], width: int = 8, height: int = 8) -> List[List[Any]]:
    """
    Build a memory-game grid where each chosen element appears exactly twice.
    width/height act as maximum bounds. If there are too many elements, extras
    are skipped. If there are too few to fill the requested grid, we shrink
    width/height and may drop additional elements so that the grid is perfectly
    filled (no padding).
    """
    if not elements:
        raise ValueError("elements must not be empty")

    total_cells = width * height
    if total_cells < 2:
        raise ValueError("Grid must have space for at least one pair")

    max_pairs = total_cells // 2
    target_pairs = min(len(elements), max_pairs)

    def find_dims(pairs: int) -> tuple[int, int] | None:
        cells = pairs * 2
        max_w = min(width, cells)
        for w in range(max_w, 0, -1):
            if cells % w != 0:
                continue
            h = cells // w
            if h <= height:
                return w, h
        return None

    dims = None
    while target_pairs > 0 and dims is None:
        dims = find_dims(target_pairs)
        if dims is None:
            target_pairs -= 1  # drop one pair (i.e., exclude an element)

    if dims is None:
        raise ValueError("Could not fit any pairs within the given bounds")

    chosen_width, chosen_height = dims

    chosen_elements = (
        random.sample(elements, target_pairs)
        if target_pairs < len(elements)
        else list(elements)
    )

    pool: List[Any] = []
    for el in chosen_elements:
        pool.extend([el, el])  # two of each element

    random.shuffle(pool)

    grid: List[List[Any]] = []
    idx = 0
    for _ in range(chosen_height):
        row = pool[idx : idx + chosen_width]
        grid.append(row)
        idx += chosen_width

    return grid


if __name__ == "__main__":
    sample = ["A", "B", "C", "D", "E", "F", "G", "H", "I",'bb','cc','dd','ee','ff','gg','hh','ii']
    # sample = ["A", "B", "C", "D", "E", "F"]
    g = create_memory_game(sample, width=6, height=6)
    for row in g:
        print(row)
