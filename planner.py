import sys
import heapq

DIRECTIONS = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}

def parse_file(filepath):
    with open(filepath, 'r') as f:
        cols = int(f.readline())
        rows = int(f.readline())
        grid = [list(f.readline().strip()) for _ in range(rows)]

    start_loc = None
    dirty_cells = set()

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                start_loc = (r, c)
            elif grid[r][c] == '*':
                dirty_cells.add((r, c))

    return grid, start_loc, dirty_cells

def dfs(grid, start_loc, dirty_cells):
    rows, cols = len(grid), len(grid[0])
    stack = [{
        "loc": start_loc,
        "dirt": set(dirty_cells),
        "path": []
    }]
    visited = set()
    nodes_generated = 1
    nodes_expanded = 0

    while stack:
        state = stack.pop()
        loc, dirt_left, path = state["loc"], state["dirt"], state["path"]
        nodes_expanded += 1

        if not dirt_left:
            return path, nodes_generated, nodes_expanded

        if loc in dirt_left:
            new_dirt = set(dirt_left)
            new_dirt.remove(loc)
            stack.append({
                "loc": loc,
                "dirt": new_dirt,
                "path": path + ["V"]
            })
            nodes_generated += 1
            continue

        r, c = loc
        for action, (dr, dc) in DIRECTIONS.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                state_id = ((nr, nc), frozenset(dirt_left))
                if state_id not in visited:
                    visited.add(state_id)
                    stack.append({
                        "loc": (nr, nc),
                        "dirt": dirt_left,
                        "path": path + [action]
                    })
                    nodes_generated += 1

    return [], nodes_generated, nodes_expanded

def ucs(grid, start_loc, dirty_cells):
    rows, cols = len(grid), len(grid[0])
    initial_state = (0, [], start_loc, frozenset(dirty_cells))
    priority_queue = [initial_state]
    visited = set()
    nodes_generated = 1
    nodes_expanded = 0

    while priority_queue:
        cost, path, loc, dirt_left = heapq.heappop(priority_queue)
        state_id = (loc, dirt_left)

        if state_id in visited:
            continue
        visited.add(state_id)
        nodes_expanded += 1

        if not dirt_left:
            return path, nodes_generated, nodes_expanded

        if loc in dirt_left:
            new_dirt = set(dirt_left)
            new_dirt.remove(loc)
            heapq.heappush(priority_queue, (cost + 1, path + ["V"], loc, frozenset(new_dirt)))
            nodes_generated += 1
            continue

        r, c = loc
        for action, (dr, dc) in DIRECTIONS.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                heapq.heappush(priority_queue, (cost + 1, path + [action], (nr, nc), dirt_left))
                nodes_generated += 1

    return [], nodes_generated, nodes_expanded

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 planner.py [uniform-cost|depth-first] [world-file]")
        return

    algorithm = sys.argv[1]
    file_path = sys.argv[2]

    cols, rows, grid, start, dirty = parse_file(file_path)
    initial_state = (start, frozenset(dirty))

    if algorithm == "depth-first":
        actions, nodes_generated, nodes_expanded = dfs(initial_state, grid, cols, rows)
    elif algorithm == "uniform-cost":
        actions, nodes_generated, nodes_expanded = ucs(initial_state, grid, cols, rows)
    else:
        print("Unknown algorithm. Use 'depth-first' or 'uniform-cost'.")
        return

    for action in actions:
        print(action)
    print(f"{nodes_generated} nodes generated")
    print(f"{nodes_expanded} nodes expanded")

if __name__ == "__main__":
    main()