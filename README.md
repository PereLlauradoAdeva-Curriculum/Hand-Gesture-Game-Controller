# 🖐️ Hand Gesture Game Controller

This project lets you control the classic **Snake** game using your **hand gestures**, implemented with two different methods:

- A **MediaPipe-based model** to play the game.
- A **classical computer vision method** to visualize hand direction.

---

## 🎮 Snake Game (MediaPipe)

This version uses **MediaPipe** to detect hand landmarks and control the Snake game in real time.

### ▶️ How to run:

> Simply **press the "Run" or "Compile" button** on `main.py` in your code editor.  
> No terminal commands needed.

- Moves are based on the direction between the **wrist and the index fingertip**.
- Very robust under different lighting and background conditions.

---

## 🔍 Hand Direction Visualizer (Classical CV)

This version detects the **direction your hand is pointing** using skin color segmentation and contour analysis.

> ⚠️ This version **does not control the game**, it only shows the detected direction on screen.

### ▶️ How to run:

> Open `manual.py` and **click "Run"** in your IDE or editor.  
> No terminal input required.

### ⚠️ Detection tips:

- Wear a **dark sleeve** to hide your wrist.
- Use a **plain, light-colored background**.
- Avoid too many objects or strong lighting changes.
