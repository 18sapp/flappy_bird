# Flappy Bird Web Game

A web-based Flappy Bird game with custom features: coin collection and a 3-lives system. Built with Python, Pygame, and deployed with Docker.

## Features

- **Classic Flappy Bird gameplay**: Navigate through pipes by jumping
- **Coin Collection**: Collect coins that spawn between pipes for bonus points
- **3 Lives System**: You have 3 lives - lose a life when you hit a pipe or the screen edges
- **Score Tracking**: Track your score and coins collected
- **Web Deployable**: Compile to WebAssembly and run in any modern browser

## Game Controls

- **SPACE** or **Mouse Click**: Make the bird jump
- **SPACE** or **Mouse Click** (on menu/game over): Start/Restart game

## Project Structure

```
flappy_bird/
├── game/
│   ├── __init__.py
│   ├── main.py          # Main game loop
│   ├── bird.py          # Bird class with lives system
│   ├── pipes.py         # Obstacle pipes
│   ├── coins.py         # Coin collection system
│   ├── game_state.py    # Game state management
│   └── constants.py     # Game constants
├── assets/
│   ├── images/          # Sprites and images
│   └── sounds/          # Sound effects (optional)
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration
└── README.md            # This file
```

## Local Development

### Prerequisites

- Python 3.11 or higher
- pip

### Setup

1. Clone or navigate to the project directory:
```bash
cd flappy_bird
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game locally:
```bash
python -m game.main
```

## Docker Deployment

### Build the Docker Image

```bash
docker build -t flappy-bird-game .
```

### Run the Container

```bash
docker run -p 8000:8000 flappy-bird-game
```

### Access the Game

Open your web browser and navigate to:
```
http://localhost:8000
```

The game will be served as a web application and should work in any modern browser that supports WebAssembly.

## Docker Compose (Optional)

You can also use Docker Compose for easier management. Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  flappy-bird:
    build: .
    ports:
      - "8000:8000"
    restart: unless-stopped
```

Then run:
```bash
docker-compose up
```

## How It Works

1. **Game Development**: The game is developed using Pygame, a popular Python game development library.

2. **Web Compilation**: The game is compiled to WebAssembly using `pygbag`, which allows Pygame games to run in web browsers.

3. **Docker Deployment**: The Dockerfile uses a multi-stage build:
   - **Stage 1 (Builder)**: Installs dependencies and compiles the game with pygbag
   - **Stage 2 (Production)**: Serves the compiled web files using a simple HTTP server

4. **Web Server**: The final container runs a Python HTTP server on port 8000, serving the compiled game files.

## Customization

You can customize the game by modifying constants in `game/constants.py`:
- Screen dimensions
- Bird physics (gravity, jump strength)
- Pipe settings (width, gap size, speed)
- Coin settings (size, rotation speed)
- Number of lives
- Score values

## Troubleshooting

### Game doesn't compile with pygbag

If you encounter issues with pygbag compilation, you may need to:
- Ensure all dependencies are installed
- Check that the game runs locally first
- Review pygbag documentation for compatibility issues

### Docker build fails

- Make sure Docker is running
- Check that all files are present in the project directory
- Review Docker logs for specific error messages

### Game doesn't load in browser

- Ensure the container is running and port 8000 is accessible
- Check browser console for errors
- Verify WebAssembly support in your browser

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to fork this project and add your own features! Some ideas:
- Add sound effects
- Implement different difficulty levels
- Add power-ups
- Create a leaderboard system
- Add multiplayer support

