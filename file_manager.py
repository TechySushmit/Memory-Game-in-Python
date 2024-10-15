import csv
import os
from datetime import datetime

class ScoreManager:
    def __init__(self):
        # Initialize the file name
        self.file_name = "scores.csv"
        # Create the CSV file with headers if it doesn't exist
        if not os.path.exists(self.file_name):
            with open(self.file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Game Number", "Player Name", "Moves", "Time Taken", "Date", "Time"])

    def save_score(self, player_name, moves, time_taken):
        # Append a new score entry to the CSV file
        with open(self.file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            # Count existing games
            game_number = sum(1 for _ in open(self.file_name))
            # Get the current time
            current_time = datetime.now()
            # Format time taken to 2 decimal places
            formatted_time_taken = round(time_taken, 2)
            # Write the new score entry
            writer.writerow([game_number, player_name, moves, formatted_time_taken, current_time.strftime("%Y-%m-%d"), current_time.strftime("%H:%M:%S")])

    def get_scores(self):
        # Read all scores from the CSV file
        with open(self.file_name, 'r') as file:
            reader = csv.reader(file)
            # Skip the header
            next(reader)
            # Return all score records
            return list(reader)
