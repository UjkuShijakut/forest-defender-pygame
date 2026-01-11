# Forest Defender – Pygame Project

## Game Concept
Forest Defender is a 2D top-down survival shooter developed using **Python** and **Pygame**.  
The player controls a hero who must defend a magical tree located at the center of the screen from continuously spawning enemies. Enemies approach from all sides and become stronger over time. The game ends when the tree’s health reaches zero.

The game focuses on real-time combat, increasing difficulty, and basic resource management (positioning, aiming, and reaction time).

---

## How to Run the Game

### Requirements
- Python 3.10 or newer
- Pygame library

### Installation & Run
pip install pygame
python main.py
The game launches in fullscreen mode.
Press ESC to exit.

Controls
W / A / S / D – Move player

Left Mouse Button – Shoot

R – Restart game after Game Over

ESC – Quit game

Project Structure

forest-defender-pygame/
│
├── main.py          # Entry point
├── game.py          # Main game loop and logic
├── settings.py      # Game constants and configuration
├── audio.py         # Audio manager (music & sound effects)
├── utils.py         # Helper math and image-loading utilities
│
├── entities/
│   ├── player.py
│   ├── enemy.py
│   └── tree.py
│
├── assets/
│   ├── bg.png
│   ├── player.png
│   ├── enemy.png
│   ├── tree.png
│   ├── projectile.png
│   ├── music_game.mp3
│   ├── sfx_shoot.mp3
│   └── sfx_lose.wav
Implemented Classes & Functionality
Core Custom Classes
Game
Manages the main loop, rendering, collision detection, scoring, game states, and restart logic.

Player
Handles player movement, aiming, and projectile shooting.

Enemy
Enemies spawn from screen edges and move toward the tree. Each enemy has health, speed, and damage values.

TreeBase
Represents the central object being defended. Tracks health and triggers game over when destroyed.

Spawner
Dynamically spawns enemies and increases difficulty over time by:

Reducing spawn intervals

Increasing enemy speed

Increasing enemy health

AudioManager
Controls background music and sound effects with a separate volume control for music and SFX.

Gameplay Features
Real-time shooting mechanics

Progressive difficulty scaling

Collision-based damage system

Score tracking

Game Over screen with a restart option

Background music and sound effects

Sprite-based visuals

Fullscreen rendering

Assignment Notes
This project was developed individually with the help of online tutorials and other tools.

Uses Python + Pygame

Demonstrates object-oriented design, game loops, event handling, and audio integration

Author
Gerald
