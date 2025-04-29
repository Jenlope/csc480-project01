import sys
import heapq

# Directions: N, S, E, W
DIRS = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}

def parse_file(path):
    with open(path) as f:
        cols, rows = int(f.readline()), int(f.readline())
        grid = [list(f.readline().strip()) for _ in range(rows)]

    start = None
    dirty = set()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                start = (r, c)
            elif grid[r][c] == '*':
                dirty.add((r, c))

    return grid, start, dirty

def dfs(grid, start, dirty):
    stack = [(start, set(dirty), [])]
    visited = set()
    gen, exp = 1, 0

    while stack:
        loc, dirt_left, path = stack.pop()
        exp += 1
        if not dirt_left:
            return path, gen, exp

        if loc in dirt_left:
            new_dirt = dirt_left - {loc}
            stack.append((loc, new_dirt, path + ['V']))
            gen += 1
            continue

        for move, (dr, dc) in DIRS.items():
            nr, nc = loc[0] + dr, loc[1] + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '#':
                state = ((nr, nc), frozenset(dirt_left))
                if state not in visited:
                    visited.add(state)
                    stack.append(((nr, nc), dirt_left, path + [move]))
                    gen += 1

    return [], gen, exp

def ucs(grid, start, dirty):
    pq = [(0, [], start, frozenset(dirty))]
    visited = set()
    gen, exp = 1, 0

    while pq:
        cost, path, loc, dirt_left = heapq.heappop(pq)
        if (loc, dirt_left) in visited:
            continue
        visited.add((loc, dirt_left))
        exp += 1

        if not dirt_left:
            return path, gen, exp

        if loc in dirt_left:
            new_dirt = dirt_left - {loc}
            heapq.heappush(pq, (cost + 1, path + ['V'], loc, frozenset(new_dirt)))
            gen += 1
            continue

        for move, (dr, dc) in DIRS.items():
            nr, nc = loc[0] + dr, loc[1] + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '#':
                heapq.heappush(pq, (cost + 1, path + [move], (nr, nc), dirt_left))
                gen += 1

    return [], gen, exp

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 planner.py [uniform-cost|depth-first] [world-file]")
        return

    algo, file = sys.argv[1], sys.argv[2]
    grid, start, dirty = parse_file(file)

    if algo == "depth-first":
        actions, gen, exp = dfs(grid, start, dirty)
    elif algo == "uniform-cost":
        actions, gen, exp = ucs(grid, start, dirty)
    else:
        print("Unknown algorithm.")
        return

    print("\n".join(actions))
    print(f"{gen} nodes generated")
    print(f"{exp} nodes expanded")

if __name__ == "__main__":
    main()