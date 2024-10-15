import random
import time

class MemoryGame:
    def __init__(self, grid_size=4):  # Initialize the game with a default grid size of 4x4
        self.grid_size = grid_size  # Set the size of the game grid
        self.moves = 0  # Initialize the number of moves made
        self.first_click = None  # Track the first card clicked
        self.second_click = None  # Track the second card clicked
        self.board = []  # Initialize the game board
        self.answer_board = []  # Initialize the answer board with correct matches
        self.flipped_tiles = []  # Track which tiles are currently flipped
        self.is_processing = False  # Flag to check if the game is currently processing a move

        self.create_board()  # Call the method to create the game board

    def create_board(self):
        # Calculate the number of pairs needed for the game
        num_pairs = (self.grid_size * self.grid_size) // 2
        # Select symbols for the game, ensuring there are enough for the number of pairs
        symbols = list('ABCDEFGH')[:num_pairs] * 2
        # Shuffle the symbols to randomize their positions
        random.shuffle(symbols)

        # Create the answer board with the shuffled symbols
        self.answer_board = [symbols[i:i + self.grid_size] for i in range(0, len(symbols), self.grid_size)]
        # Initialize the game board with empty strings
        self.board = [['' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        # Initialize the flipped tiles tracker with all tiles initially unflipped
        self.flipped_tiles = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        # Reset moves and click trackers
        self.moves = 0
        self.first_click = None
        self.second_click = None

    def get_board(self):
        return self.board  # Return the current state of the game board

    def flip_card(self, i, j):
        # Check if the click is within the grid boundaries
        if i < 0 or j < 0 or i >= self.grid_size or j >= self.grid_size:
            return False  # Return False if the click is out of bounds

        # Check if the game is currently processing a move
        if self.is_processing:
            return False  # Return False if the game is processing

        # Check if the tile is already flipped
        if self.flipped_tiles[i][j]:
            return False  # Return False if the tile is already flipped

        # If no tile is currently flipped, flip the first tile
        if self.first_click is None:
            self.first_click = (i, j)  # Record the first click
            self.board[i][j] = self.answer_board[i][j]  # Reveal the symbol on the first click
            self.flipped_tiles[i][j] = True  # Mark the first tile as flipped
            return True  # Return True to indicate a successful flip

        # If a tile is already flipped, flip the second tile
        elif self.second_click is None:
            self.second_click = (i, j)  # Record the second click
            self.board[i][j] = self.answer_board[i][j]  # Reveal the symbol on the second click
            self.flipped_tiles[i][j] = True  # Mark the second tile as flipped
            return True  # Return True to indicate a successful flip

    def reset_pair(self):
        # Reset the first and second clicks
        i1, j1 = self.first_click
        i2, j2 = self.second_click
        # Hide the symbols on the first and second clicks
        self.board[i1][j1] = ''
        self.board[i2][j2] = ''
        # Mark the first and second tiles as unflipped
        self.flipped_tiles[i1][j1] = False
        self.flipped_tiles[i2][j2] = False
        # Reset the first and second click trackers
        self.first_click = None
        self.second_click = None

    def get_moves(self):
        return self.moves  # Return the total number of moves made

    def check_match(self):
        # Get the positions of the first and second clicks
        i1, j1 = self.first_click
        i2, j2 = self.second_click

        # Set the game processing flag to True
        self.is_processing = True
        # Check if the symbols on the first and second clicks match
        if self.answer_board[i1][j1] == self.answer_board[i2][j2]:
            # If they match, reset the first and second clicks
            self.first_click = None
            self.second_click = None
            # Increment the moves counter
            self.moves += 1
            # Set the game processing flag to False
            self.is_processing = False
            return True  # Return True to indicate a match
        else:
            # If they don't match, increment the moves counter
            self.moves += 1
            # Wait for a short time before resetting the pair
            time.sleep(0.5)
            # Reset the pair
            self.reset_pair()
            # Set the game processing flag to False
            self.is_processing = False
            return False  # Return False to indicate no match

    def is_game_over(self):
        # Check if all tiles have been flipped
        for row in self.flipped_tiles:
            if False in row:
                return False  # Return False if any tile is unflipped
        return True  # Return True if all tiles are flipped, indicating the game is over
