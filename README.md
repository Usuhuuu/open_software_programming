# Rock-Paper-Scissors Hand Gesture Recognition Game

This is a simple hand gesture recognition game implemented using OpenCV, MediaPipe, and Python. The game allows the user to play Rock-Paper-Scissors against a computer that adapts its choices based on the user's historical gestures.

## Table of Contents

- [How to Play](#how-to-play)
- [Dependencies](#dependencies)
- [How It Works](#how-it-works)
- [Hand Detection Visualization](#hand-detection-visualization)
- [Game Flow](#game-flow)
- [Random Choice Improvement](#random-choice-improvement)
- [Difficulty Adjustment](#difficulty-adjustment)
- [How to Contribute](#how-to-contribute)
- [Conclusion](#conclusion)

## How to Play

1. Run the `play_game()` function in the main script.
2. Gesture recognition is performed using the MediaPipe library.
3. The user's gesture is classified based on the position of thumb, index, and middle finger tips.
4. The computer adapts its choice based on the most common historical user gesture.

## Dependencies

To run the game, you need to install the following Python libraries. You can install them using the following commands:

```bash
pip install opencv-python
pip install mediapipe
