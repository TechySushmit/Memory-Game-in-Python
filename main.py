# Python Memory Game using Tkinter and Pygame.

import tkinter as tk                # Import the Tkinter module for the GUI
from ui import MemoryGameUI         # Import the MemoryGameUI class from ui.py
import pygame                       # Import the pygame module for sound effects
import pandas as pd                 # Import the pandas module for data analysis
import matplotlib.pyplot as plt     # Import the matplotlib module for plotting

# Function to handle cleanup when the window is closed
def on_closing(root):
    pygame.quit()       # Quit pygame
    plt.close('all')    # Close all matplotlib windows (if any)
    root.destroy()      # Destroy the Tkinter window

# Main function to run the game.
def main():
    # Initialize pygame
    pygame.init()
    
    # Create the main window
    root = tk.Tk()
    
    # Initialize the game UI
    game_ui = MemoryGameUI(root)
    
    # Bind the on_closing function to the window close event
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    
    # Start the Tkinter event loop
    root.mainloop()

# Entry point of the program
if __name__ == "__main__":
    main() # Call the main function to run the game
