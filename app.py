from flask import Flask, render_template
from src.main import Warehouse



app = Flask(__name__, template_folder='src/templates')

@app.route('/')
def index():
    # Initialize the warehouse
    warehouse = Warehouse(5, 5)
    warehouse.add_pick_location(1, 2)
    warehouse.add_pick_location(3, 4)
    warehouse.set_obstacle(2, 2)
    warehouse.set_one_way_aisle(2, 3, 'down')

    # Find the shortest path
    start_x, start_y = 0, 0
    path = warehouse.find_path(start_x, start_y)

    # Visualize the path
    grid = []
    for y in range(warehouse.height):
        row = []
        for x in range(warehouse.width):
            if (x, y) in warehouse.pick_locations:
                row.append('P')  # Highlight picking locations
            elif (x, y) in warehouse.obstacles:
                row.append('#')  # Obstacle
            elif (x, y) in path:
                row.append('*')  # Path
            else:
                row.append('.')  # Free space
        grid.append(row)

    return render_template('index.html', grid=grid)

if __name__ == '__main__':
    app.run(debug=True)
