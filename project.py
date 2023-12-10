import cv2
import mediapipe as mp
import random
import time
from collections import Counter
import threading     


mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
user_score = 0
computer_score = 0
last_winner_time = 0
user_gesture_history = []

def classify_gesture(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    # Calculate distances between finger tips
    dist_thumb_index = ((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)**0.5
    dist_index_middle = ((index_tip.x - middle_tip.x)**2 + (index_tip.y - middle_tip.y)**2)**0.5
    # Define thresholds to classify gestures
    threshold_rock = 0.08  
    threshold_paper = 0.12  
    threshold_scissors = 0.12  
    # Classify gestures based on distances
    if dist_thumb_index < threshold_rock:
        return "Rock"
    elif dist_thumb_index > threshold_paper and dist_index_middle > threshold_scissors:
        return "Paper"
    else:
        return "Scissors"
    
def get_computer_gesture():
    global user_gesture_history
    gestures = ["Rock", "Paper", "Scissors"]

    if user_gesture_history:
        most_common_user_gesture = Counter(user_gesture_history).most_common(1)[0][0]

        if most_common_user_gesture == "Rock":
            return "Paper"
        elif most_common_user_gesture == "Paper":
            return "Scissors"
        elif most_common_user_gesture == "Scissors":
            return "Rock"
    return random.choice(gestures)

def determine_winner(user_choice, computer_choice):
    global last_winner_time
    current_time = time.time()


    if user_choice == computer_choice:
        last_winner_time = current_time
        return "Tie"
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
            (user_choice == "Paper" and computer_choice == "Rock") or \
            (user_choice == "Scissors" and computer_choice == "Paper"):
        last_winner_time = current_time
        return "User"
    else:
        return "Computer"
    
def update_score(winner, user_gesture):
    global user_score, computer_score
    if winner == "User" and user_gesture != "Undetected":
        user_score += 1
    elif winner == "Computer" and user_gesture != "Undetected":
        computer_score += 1
    elif winner == "Tie":
        print("Tie")

def display_countdown(countdown_time):
    for i in range(countdown_time, 0, -1):
        print(f"Countdown: {i}")
        time.sleep(1)

def overlay_countdown(frame, countdown):
    cv2.putText(frame, countdown, (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    return frame

def detect_hands(frame, winner_text="", winner_info="", end_message=""):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                height, width, _ = frame.shape
                cx, cy = int(landmark.x * width), int(landmark.y * height)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
        connections = mp_hands.HAND_CONNECTIONS
        for connection in connections:
            x0, y0 = int(hand_landmarks.landmark[connection[0]].x * width), int(hand_landmarks.landmark[connection[0]].y * height)
            x1, y1 = int(hand_landmarks.landmark[connection[1]].x * width), int(hand_landmarks.landmark[connection[1]].y * height)
            cv2.line(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)

        cv2.putText(frame, winner_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
            
    return frame

def play_game():
    global user_score, computer_score, last_winner_time, user_gesture_history
    
    cap = cv2.VideoCapture(0)

    while True:
        user_score = 0
        computer_score = 0
        last_winner_time = 0
        in_delay = False
        user_gesture = ""
        computer_gesture = get_computer_gesture()

        while True:
            winner = determine_winner(user_gesture, computer_gesture)
            update_score(winner, user_gesture)
            print(f"User gesture: {user_gesture}, Computer gesture: {computer_gesture}, Winner: {winner}")
            key = cv2.waitKey(1) & 0xFF
            if winner == "Computer" or winner == "User":
                in_delay = True
            if in_delay:
                delay_start_time = time.time()
                in_delay = False  
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Failed to capture frame.")
                    break
                results = hands.process(frame)
                if results.multi_hand_landmarks and len(results.multi_hand_landmarks) > 0:
                    user_gesture = classify_gesture(results.multi_hand_landmarks[0])
                    user_gesture_history.append(user_gesture)
                else:
                    user_gesture = "Undetected"
                    
                # Only update the computer gesture if the user's gesture is detected
                if user_gesture != "Undetected":
                    computer_gesture = get_computer_gesture()
                    
                winner_text = f"Your Score: {user_score} Computer Score: {computer_score}"
                # Draw user and computer gestures directly on the camera feed
                if winner == "User":
                    winner_info = f"You won with Gesture: {user_gesture} (Computer's Gesture: {computer_gesture})"
                elif winner == "Computer":
                    if user_gesture == "Undetected":
                        winner_info = f"Computer won as your gesture is Undetected. Computer Gesture: {computer_gesture}"
                    else:
                        winner_info = f"Computer won with Computer Gesture: {computer_gesture}  Your Gesture is :{user_gesture}"
                        cv2.putText(frame, winner_info, (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        cv2.imshow("Camera Feed", frame)
                        delay_start_time = time.time()
                        while time.time() - delay_start_time < 5:
                            ret, frame = cap.read()
                            if not ret:
                                print("Error: Failed to capture frame.")
                                break
                            result_frames = detect_hands(frame, winner_text, winner_info)
                            result_frames = overlay_countdown(result_frames, str(5 - int(time.time() - delay_start_time)))
                            cv2.putText(result_frames, f"Your Gesture: {user_gesture}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                            cv2.putText(result_frames, f"Computer Gesture: {computer_gesture}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                            cv2.putText(result_frame, f"Winner is: {winner}",(10, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                            cv2.imshow("Camera Feed", result_frames)
                            key = cv2.waitKey(1) & 0xFF
                            if key == ord('q'):
                                break
                        winner_info = ""
                end_message = "Press 'S' to start a new game or 'Q' to quit"
                result_frame = detect_hands(frame, winner_text, winner_info, end_message)
                cv2.putText(result_frame, f"Your Gesture: {user_gesture}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.putText(result_frame, f"Computer Gesture: {computer_gesture}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.putText(result_frame, f"Winner is: {winner}",(10, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.imshow("Camera Feed", result_frame)
                
                if time.time() - delay_start_time >= 5:
                    break
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
            if key == ord('q'):
                break

        # Release the camera at the end of the game loop
        cap.release()

        end_message = "Press 'S' to start a new game or 'Q' to quit"
        cv2.putText(frame, end_message, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Camera Feed", frame)
        key = cv2.waitKey(0) & 0xFF
        if key == ord('s'):
            cv2.destroyAllWindows()
            cap = cv2.VideoCapture(0)  # No need to reopen the camera here
        elif key == ord('q'):
            cv2.destroyAllWindows()
            return

if __name__ == "__main__":
    play_game()