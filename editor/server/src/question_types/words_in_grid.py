import random
from typing import List, Tuple

def generate_grid(
    words: List[str],
    filler_chars: str,
    width: int = 8,
    height: int = 8,
    overlap: bool = False,
) -> Tuple[List[List[str]], List[dict]]:
    """
    Place words into a height x width grid in 8 directions.
    overlap=False prevents sharing cells; overlap=True lets same-letter overlaps.

    Returns (grid, placements) where placements is a list of dicts:
    {
        "word": str,
        "start": (row, col),
        "direction": (dr, dc),
        "coordinates": [(r, c), ...],
    }
    """
    words = [w.strip() for w in words if w.strip()]
    if not words:
        raise ValueError("No words to place")
    longest = max(len(w) for w in words)
    if longest > max(width, height):
        raise ValueError(f"Longest word ({longest}) does not fit in grid {width}x{height}")

    grid = [["" for _ in range(width)] for _ in range(height)]
    directions: List[Tuple[int, int]] = [
        (1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (1, -1), (-1, 1), (-1, -1),
    ]

    def can_place(word: str, r: int, c: int, dr: int, dc: int) -> bool:
        for i, ch in enumerate(word):
            rr, cc = r + dr * i, c + dc * i
            if not (0 <= rr < height and 0 <= cc < width):
                return False
            cell = grid[rr][cc]
            if cell:
                if not overlap:
                    return False
                if cell != ch:  # overlap only if same letter allowed
                    return False
        return True

    placements: List[dict] = []

    def place(word: str) -> bool:
        for _ in range(400):  # attempts
            dr, dc = random.choice(directions)
            r = random.randrange(height)
            c = random.randrange(width)
            if can_place(word, r, c, dr, dc):
                coords = []
                for i, ch in enumerate(word):
                    rr, cc = r + dr * i, c + dc * i
                    grid[rr][cc] = ch
                    coords.append((rr, cc))
                placements.append(
                    {
                        "word": word,
                        "start": (r, c),
                        "direction": (dr, dc),
                        "coordinates": coords,
                    }
                )
                return True
        return False

    for w in words:
        if not place(w):
            raise RuntimeError(f"Could not place word: {w}")

    for r in range(height):
        for c in range(width):
            if grid[r][c] == "":
                grid[r][c] = random.choice(filler_chars)

    return grid, placements

# Example
if __name__ == "__main__":
    words = ["cat", "car", "snow"]
    chars = "ertyuifdcx"
    g, placements = generate_grid(words, chars, width=8, height=8, overlap=False)
    for row in g:
        print(" ".join(row))
    print("\nplacements:")
    for p in placements:
        print(p)