import heapq

class Warehouse:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0] * width for _ in range(height)]  # Initialize grid with all zeros
        self.pick_locations = []
        self.obstacles = set()
        self.one_way_aisles = {}

    def add_pick_location(self, x, y):
        self.pick_locations.append((x, y))

    def set_obstacle(self, x, y):
        self.obstacles.add((x, y))

    def set_one_way_aisle(self, x, y, direction):
        self.one_way_aisles[(x, y)] = direction

    def heuristic(self, x, y, remaining_pick_locations):
        # A heuristic function estimating remaining distance based on the number of remaining pick locations
        return min(abs(x - px) + abs(y - py) for px, py in remaining_pick_locations)

    def a_star(self, start_x, start_y, remaining_pick_locations):
        pq = [(0, start_x, start_y, [])]  # Priority queue (f-score, x, y, path)
        visited = set()

        while pq:
            f, x, y, path = heapq.heappop(pq)

            if (x, y) in remaining_pick_locations:
                remaining_pick_locations.remove((x, y))
                if not remaining_pick_locations:
                    return path + [(x, y)]

            if (x, y) in visited:
                continue
            visited.add((x, y))

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in self.obstacles:
                        new_path = path + [(x, y)]
                        g = len(new_path)
                        h = self.heuristic(nx, ny, remaining_pick_locations)
                        f = g + h
                        heapq.heappush(pq, (f, nx, ny, new_path))

        return None  # No path found

    def find_path(self, start_x, start_y):
        remaining_pick_locations = set(self.pick_locations)
        path = []
        while remaining_pick_locations:
            next_location = self.a_star(start_x, start_y, remaining_pick_locations)
            if not next_location:
                break
            path += next_location[:-1]
            start_x, start_y = next_location[-1]
        return path

    def visualize_path(self, path):
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.pick_locations:
                    print('P', end=' ')  # Highlight picking locations
                elif (x, y) in self.obstacles:
                    print('#', end=' ')  # Obstacle
                elif (x, y) in path:
                    print('*', end=' ')  # Path
                else:
                    print('.', end=' ')  # Free space
            print()

# Example usage:
warehouse = Warehouse(5, 5)
warehouse.add_pick_location(1, 2)
warehouse.add_pick_location(3, 4)
warehouse.set_obstacle(2, 2)
warehouse.set_one_way_aisle(2, 3, 'down')

start_x, start_y = 0, 0
path = warehouse.find_path(start_x, start_y)
warehouse.visualize_path(path)
