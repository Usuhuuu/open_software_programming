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
```

## How It Works

1. The game captures video frames from the camera using OpenCV.
2. MediaPipe is employed to detect hand landmarks in each frame.
3. Key hand landmarks (thumb tip, index finger tip, middle finger tip) are used to classify the user's gesture (Rock, Paper, or Scissors).
4. The computer adapts its gesture based on the most common historical user gesture.
5. The winner is determined by comparing the user's and computer's gestures.

  
## Hand Detection Visualization

As the game runs, you will see your hand landmarks visualized on the camera feed. Key hand points are marked with green circles, and hand connections are displayed in green lines.

## Game Flow

1. The game starts with both user and computer scores set to zero.
2. The computer makes an initial random gesture.
3. The user's gesture is continuously detected using hand landmarks.
4. The winner is determined based on Rock-Paper-Scissors rules.
5. If the user or computer wins, a delay is introduced, and the winner is displayed.
6. The computer adapts its choice based on the user's historical gestures.
7. The game continues until the user decides to quit.

## Random Choice Improvement

The computer's random choice adapts based on the user's historical gestures, making it more challenging for the user to predict the computer's moves. The get_computer_gesture function uses the most common user gesture to determine the computer's choice, creating a dynamic and strategic gaming experience.

## Difficult Adjustment

1. Adaptive Computer Choice: The computer adapts its strategy based on the user's historical choices.
2. Delayed Display: After a round, there is a delay before displaying the winner, creating suspense and making the game more engaging.

## How to Contribute 

Feel free to contribute by enhancing the game logic, improving gesture recognition accuracy, or adding new features. Issues and pull requests are welcome!



Copy and paste this into your README.md file on GitHub. Adjust it as needed, and make sure to run the `pip install opencv-python` and `pip install mediapipe` commands in your terminal or command prompt to install the required libraries before running the game.





