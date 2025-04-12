# Flappy Bird Clone using Python & Pygame

Welcome to my custom-made **Flappy Bird Clone** built with **Python** and the **Pygame** library. Fly the bird through the pipes, avoid collisions, and try to get the highest score possible!

---

## 🎮 Game Overview

- Classic Flappy Bird mechanics
- Simple and smooth controls
- Real-time score tracking
- Sound effects for immersive experience
- Custom welcome and game over screens

---

## 📁 Project Structure

```
FlappyBird/
│
├── GameSprites/             # All game images
│   ├── bird.png
│   ├── background.png
│   ├── base.png
│   ├── pipe.png
│   ├── gameover.png
│   ├── logo.png
│   ├── logo2.png
│   ├── ready.png
│   ├── score.png
│   ├── pranitlogo.png
│   ├── 0.png to 9.png        # Score digit images
│
├── GameSounds/              # Game audio files
│   ├── die.mp3
│   ├── hit.mp3
│   ├── point.mp3
│   ├── swoosh.mp3
│   ├── wing.mp3
│
├── Game.py            # Main game file
├── README.md                # Project README
```

---

## ✅ Requirements

- Python 3.x
- Pygame

Install Pygame using pip:
```bash
pip install pygame
```

---

## 🚀 How to Run the Game

1. Clone or download this repository.
2. Make sure `GameSprites` and `GameSounds` folders are in the same directory as `Game.py`.
3. Run the game:

```bash
python Game.py
```

---
## 🎮 Controls
space bar ---> jump/flap
---

## 🧠 How It Works

- The bird moves forward while gravity pulls it down.
- Pressing space/arrow key makes it flap and go up.
- Avoid hitting pipes or the ground.
- You gain a point each time you pass a pipe.

---

## Future improvements

1. Add Different Game Modes
2. Implement Power-ups
3. High Score Saving
4. Improved Sound Effects
5. Mobile Support
---

## Acknowledgements
- Thanks to the original creators of Flappy Bird.
- Pygame for providing the tools to build this game.
---

## 👤 Author

**Pranit Bijave**  
A passionate Python developer !

---