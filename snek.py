from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random
import json

# Initialize the Flask app and WebSocket
app = Flask(__name__)
socketio = SocketIO(app)

# Initial game state
game_state = {
    "snake1": [(10, 32), (9, 32), (8, 32)],  # Snake 1's body (x, y)
    "snake2": [(100, 32), (101, 32), (102, 32)],  # Snake 2's body (x, y)
    "food": (50, 30)  # Food position (x, y)
}


@app.route('/')
def index_snek():
    # Serve the index page (this could be expanded to show a web version of the game)
    return render_template('index_snek.html')


@socketio.on('connect')
def handle_connect():
    print("Client connected")
    # Send the initial game state when a new client connects
    emit('game_state', json.dumps(game_state))


@socketio.on('update_direction')
def handle_update_direction(data):
    """
    Update the direction of a snake based on the received input.
    The 'data' should include which snake (snake1 or snake2) and the direction.
    """
    snake_id = data['snake']
    direction = data['direction']

    if snake_id == 'snake1':
        game_state['snake1_direction'] = direction
    elif snake_id == 'snake2':
        game_state['snake2_direction'] = direction

    # Broadcast the updated game state to all clients
    emit('game_state', json.dumps(game_state), broadcast=True)


@socketio.on('update_game')
def handle_update_game(data):
    """
    Update the game state (move the snakes, check for food collisions, etc.)
    """
    global game_state

    # Move the snakes based on their current direction
    for snake_id, snake in game_state.items():
        if snake_id.startswith("snake"):
            direction = game_state.get(f"{snake_id}_direction", (0, 0))
            # Move the snake in the current direction
            new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            snake.insert(0, new_head)
            snake.pop()  # Remove the last segment of the snake (unless food is eaten)

            # Check for food collision
            if new_head == game_state["food"]:
                # Snake eats food, grow the snake
                snake.append(snake[-1])  # Add a new segment at the tail

                # Generate new food position
                game_state["food"] = (random.randint(0, 127), random.randint(0, 63))

    # Broadcast the updated game state to all clients
    emit('game_state', json.dumps(game_state), broadcast=True)


if __name__ == '__main__':
    # Run the Flask app with WebSocket support
    socketio.run(app, host='0.0.0.0', port=5000)
