# CAS141---HIT137---Assignment-3
CDU - HIT 137 - Assignment 3. Semester2, 2024.

# Weather Forecast Application

This is a simple weather forecast application built using Python's `tkinter` library. The app allows users to select an Australian state capital city, input a specific date, and retrieve the weather forecast for that city on the selected date.

## Features

- Users can select from eight Australian state capital cities using a dropdown menu.
- Users can input a date in the `DDMMYYYY` format (e.g., 17102024 for October 17, 2024).
- The app fetches the weather forecast from the OpenWeatherMap API.
- The weather information, including temperature and general conditions, is displayed for the selected city and date.

## Prerequisites

Before running the application, ensure you have the following:

- Python 3.x installed on your machine.
- The `requests` library installed. If you don’t have it, you can install it by running:

    ```bash
    pip install requests
    ```

## API Key

This application uses the OpenWeatherMap API. You must have a valid API key to use the application. If you don’t have one, you can register for free on [OpenWeatherMap](https://openweathermap.org/api) and generate your API key.

Once you have the API key, replace the placeholder in the script with your actual key:

```python
api_key = "YOUR_API_KEY"



# Pygame Platformer Game

This is a 2D platformer game built using Python and Pygame. The player can move left, right, jump, and shoot, while avoiding enemies and collecting items such as health and points. The game features scrolling backgrounds and randomly generated enemies and items.

## Features
- 2D side-scrolling gameplay with smooth camera movements.
- Player controls: move left, right, jump, and shoot.
- Health and point collectables.
- Randomly generated enemies that move unpredictably.
- Health bar for player status.
- Game over and restart functionality.

## Screenshots
*(Add your game screenshots here)*

## Requirements
- Python 3.x
- Pygame library

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    ```
2. Navigate to the project directory:
    ```bash
    cd your-repo-name
    ```
3. Install the required dependencies:
    ```bash
    pip install pygame
    ```
4. Run the game:
    ```bash
    python game.py
    ```

## How to Play
- **A**: Move left
- **D**: Move right
- **W**: Jump
- **Space**: Shoot
- **R**: Restart after game over
- Avoid enemies and collect health and points to survive and score higher!

## File Structure
```plaintext
game.py             # Main game file
bullet.PNG          # Bullet image
coin.PNG            # Points coin image
health.PNG          # Health coin image
backround.png       # Background image
font.ttf            # Game font
