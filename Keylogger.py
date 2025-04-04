import time
import csv
import os
from pynput import keyboard

# Define the word to be typed
TARGET_WORD = "pneumonoultramicroscopicsilicovolcanoconiosis"
typed_keys = []
key_press_times = {}
data = []
held_keys = set()  # Track currently held keys
error_count = 0  # Track errors
backspace_count = 0  # Track backspaces
start_time = None  # To track word completion time

# Ask for participant details
participant_id = input("Enter Participant ID: ")
condition = input("Enter Condition (Relaxed/Stressed): ")

# Get the script directory and define the CSV file path
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script location
csv_filename = os.path.join(script_dir, "keystroke_data.csv")  # Save in the same folder
csv_headers = ["Participant ID", "Condition", "Key Pressed", "Press Time (s)", 
               "Release Time (s)", "Hold Time (s)", "Flight Time (s)",
               "Word Completion Time (s)", "Typing Speed (Keys/sec)", "Error Rate (%)"]

# Ensure the CSV file exists by creating it if necessary
if not os.path.exists(csv_filename):
    with open(csv_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)  # Write headers only once

# Function to handle key press events
def on_press(key):
    global start_time, error_count, backspace_count

    try:
        if hasattr(key, 'char') and key.char is not None:  # Only log printable characters
            key_char = key.char.lower()
            
            if start_time is None:  
                start_time = time.time()  # Start the timer on first keypress
            
            # Check if the typed letter matches the expected letter
            expected_char = TARGET_WORD[len(typed_keys)] if len(typed_keys) < len(TARGET_WORD) else None
            if key_char != expected_char:
                error_count += 1  # Count errors

            if key_char not in held_keys and len(typed_keys) < len(TARGET_WORD):  
                held_keys.add(key_char)
                typed_keys.append((key_char, time.time()))
                key_press_times[key_char] = time.time()

        elif key == keyboard.Key.backspace:  
            backspace_count += 1  # Count backspaces
        
    except AttributeError:
        pass

# Function to handle key release events
def on_release(key):
    global start_time

    try:
        if hasattr(key, 'char') and key.char is not None:
            key_char = key.char.lower()
            if key_char in key_press_times:
                press_time = key_press_times[key_char]
                release_time = time.time()
                hold_time = release_time - press_time

                # Calculate flight time (time between releasing previous key and pressing the next key)
                flight_time = (release_time - typed_keys[-2][1]) if len(typed_keys) > 1 else None
                
                # Stop when full word is typed
                if len(typed_keys) == len(TARGET_WORD):
                    completion_time = round(release_time - start_time, 4)  # Total time taken to type the word
                    typing_speed = round(len(TARGET_WORD) / completion_time, 2)  # Keys per second
                    error_rate = round((error_count / len(TARGET_WORD)) * 100, 2)  # % of errors

                    print("\nTyping test completed. Saving data...")

                    # Append data to the existing CSV file
                    with open(csv_filename, "a", newline="") as f:
                        writer = csv.writer(f)
                        # Append the calculated completion time, typing speed, and error rate to the data
                        for row in data:
                            writer.writerow(row + [completion_time, typing_speed, error_rate])  # Add new parameters

                    print(f"✅ Data successfully saved to {csv_filename}")
                    return False  # Stop listener

                # Store data
                data.append([participant_id, condition, key_char, 
                             round(press_time, 4), round(release_time, 4), 
                             round(hold_time, 4), round(flight_time, 4) if flight_time else None])

                # Remove key from held keys after it's released
                held_keys.discard(key_char)

    except AttributeError:
        pass

# Start listening to keyboard
print(f"Type the word: {TARGET_WORD}")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
