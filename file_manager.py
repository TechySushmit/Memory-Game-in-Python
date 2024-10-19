import csv                      # Import the CSV module to read and write CSV files
import os                       # Import the OS module to check if a file exists
from datetime import datetime   # Import the datetime module to get the current date and time

# Define the ScoreManager class

# This class will handle saving and retrieving scores from a CSV file
# It will save the player name, number of moves, time taken, date, and time for each game
# It will also read all scores from the CSV file
# The CSV file will have the following headers: Game Number, Player Name, Moves, Time Taken, Date, Time
# The save_score method will append a new score entry to the CSV file

# The ScoreManager class will have the following methods:
class ScoreManager:
    def __init__(self):
        # Initialize the file name
        self.file_name = "scores.csv"
        # Create the CSV file with headers if it doesn't exist
        if not os.path.exists(self.file_name):
            # Exception handling for file creation
            try:
                with open(self.file_name, 'w', newline='') as file: # Open the file in write mode
                    writer = csv.writer(file) # Create a CSV writer object
                    writer.writerow(["Game Number", "Player Name", "Moves", "Time Taken", "Date", "Time"]) # Write the headers
            except IOError as e: 
                print(f"Error creating file: {e}") # Print an error message if file creation fails

    # Method to save the score of a game
    def save_score(self, player_name, moves, time_taken):
        # Exception handling for appending to the file
        try:
            with open(self.file_name, 'a', newline='') as file: # Open the file in append mode
                writer = csv.writer(file)
                # Count existing games
                game_number = sum(1 for _ in open(self.file_name))
                # Get the current time
                current_time = datetime.now()
                # Format time taken to 2 decimal places
                formatted_time_taken = f"{time_taken:.2f}"
                # Write the new score entry
                writer.writerow([game_number, player_name, moves, formatted_time_taken, current_time.strftime("%Y-%m-%d"), current_time.strftime("%H:%M:%S")])
        except IOError as e:
            print(f"Error appending to file: {e}")

    # Method to get all scores from the CSV file
    def get_scores(self):
        # Exception handling for reading the file
        try:
            with open(self.file_name, 'r') as file: # Open the file in read mode
                reader = csv.reader(file)
                # Skip the header
                next(reader)
                # Return all score records
                return list(reader)
        except IOError as e:
            print(f"Error reading file: {e}")
            # Return an empty list if there is an error
            return [] 
