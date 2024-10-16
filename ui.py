import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from game_logic import MemoryGame
from file_manager import ScoreManager
import time
import pygame
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

class MemoryGameUI:
    def __init__(self, root):
        # Initialize pygame mixer for sound effects
        pygame.mixer.init()
        self.flip_sound = pygame.mixer.Sound('audio\switch.wav')
        self.match_sound = pygame.mixer.Sound('audio\match.wav')
        self.error_sound = pygame.mixer.Sound('audio\error.mp3')

        # Set volume levels for sound effects
        self.flip_sound.set_volume(0.7)
        self.match_sound.set_volume(0.4)
        self.error_sound.set_volume(1.0)

        # Initialize main window properties
        self.root = root
        self.root.title("Memory Game")
        self.root.iconbitmap('game.ico')  
        self.root.geometry("1000x600")  # Kept the window size as 1000x600
        self.root.state('zoomed')  # Make the main window full screen

        # Initialize game components
        self.score_manager = ScoreManager()
        self.grid_size = 4
        self.card_size = 130  
        self.player_name = None

        # Define color palette for UI elements
        self.colors = {
            'background': '#1A1A2E',
            'card_back': '#16213E',
            'card_front': '#0F3460',
            'text': '#E94560',
            'button': '#533483',
            'button_text': '#E94560',
            'panel': '#0F3460',  
            'border': '#FFFFFF' 
        }

        # Create the initial game screen
        self.create_initial_screen()

    def center_window(self, window=None):
        # Center the window on the screen
        if window is None:
            window = self.root
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width/2) - (1000/2)
        y = (screen_height/2) - (600/2)
        window.geometry(f'1000x600+{int(x)}+{int(y)}')

    def create_initial_screen(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create main frame for initial screen
        self.initial_frame = tk.Frame(self.root, bg=self.colors['background'])
        self.initial_frame.pack(fill="both", expand=True)
        
        # Load and display the game title image
        image = Image.open("memory_game_title.png") 
        image = image.resize((int(1930/4), int(984/4)), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        
        title_label = tk.Label(self.initial_frame, image=photo, bg=self.colors['background'])
        title_label.image = photo  # Keep a reference
        title_label.pack(pady=(30, 15))

        # Add game instructions
        instructions = """

        How to Play: \n
        1. Click on a card to reveal its symbol.
        2. Click on another card to find its match.
        3. If the cards match, they stay face up.
        4. If they don't match, they flip back over.
        5. Remember the positions of the cards and try to 
            match all pairs in the fewest moves and the 
            shortest time possible.

        """

        instructions_label = tk.Label(self.initial_frame, text=instructions, font=("Arial", 15), bg=self.colors['background'], fg=self.colors['text'], justify=tk.LEFT, wraplength=500)
        instructions_label.pack(pady=18)

        
        good_luck_label = tk.Label(self.initial_frame, text="Good Luck and Have Fun!", font=("Arial", 17, "bold"), bg=self.colors['background'], fg=self.colors['text'])
        good_luck_label.pack(pady=15)

        # Add buttons for starting a new game, viewing history, showing stats and credits
        button_frame = tk.Frame(self.initial_frame, bg=self.colors['background'])
        button_frame.pack(pady=15)

        new_game_button = tk.Button(button_frame, text="New Game", font=("Arial", 16, "bold"), bg=self.colors['button'], fg=self.colors['button_text'], command=self.start_new_game, padx=15, pady=8)
        new_game_button.pack(side=tk.LEFT, padx=15)

        history_button = tk.Button(button_frame, text="View History", font=("Arial", 16, "bold"), bg=self.colors['button'], fg=self.colors['button_text'], command=self.show_history, padx=15, pady=8)
        history_button.pack(side=tk.LEFT, padx=15)

        stats_button = tk.Button(button_frame, text="Player Stats", font=("Arial", 16, "bold"), bg=self.colors['button'], fg=self.colors['button_text'], command=self.show_player_stats, padx=15, pady=8)
        stats_button.pack(side=tk.LEFT, padx=15)

        credits_button = tk.Button(button_frame, text="Credits", font=("Arial", 16, "bold"), bg=self.colors['button'], fg=self.colors['button_text'], command=self.show_credits, padx=15, pady=8)
        credits_button.pack(side=tk.LEFT, padx=15)

    def show_credits(self):
        # Create a new window for credits
        credits_window = tk.Toplevel(self.root)
        credits_window.title("Credits")
        credits_window.iconbitmap('game.ico')
        credits_window.geometry("600x400")
        credits_window.configure(bg=self.colors['background'])
        self.center_window(credits_window)

        # Add credits information using lists (bullet points)
        credits_text = """
        Game developed by:
        • Sushmit Biswas (Lead Developer & Designer)
        • Kabir Ahuja (Contributor, Game Logic)
        • Aryan Malik (Contributor, UI Design)
        • Santosh Reddy (Contributor, CSV Handling)
        """
        credits_label = tk.Label(credits_window, text=credits_text, font=("Arial", 18, "bold"), bg=self.colors['background'], fg=self.colors['text'], justify=tk.LEFT, wraplength=800)
        credits_label.pack(pady=10)

        # Add a FUN FACT about game development
        fun_fact = """
        DID YOU KNOW ?\n
        The first computer game, 'Spacewar !',
        was developed in 1962
        by Steve Russell, Martin Graetz, and Wayne Wiitanen
        at the Massachusetts Institute of Technology (MIT).
        """
        fact_label = tk.Label(credits_window, text=fun_fact, font=("Arial", 14, "italic"), bg=self.colors['background'], fg=self.colors['text'], justify=tk.CENTER, wraplength=500)
        fact_label.pack(pady=5)  

        # Add a decorative element
        canvas = tk.Canvas(credits_window, width=400, height=100, bg=self.colors['background'], highlightthickness=0)
        canvas.pack(pady=20)

        # Function to create a gradient color list
        def create_gradient_colors(colors, steps):
            gradient = []
            for j in range(len(colors) - 1):
                start_color = colors[j]
                end_color = colors[j + 1]
                for i in range(steps):
                    r = int(np.interp(i, [0, steps - 1], [int(start_color[1:3], 16), int(end_color[1:3], 16)]))
                    g = int(np.interp(i, [0, steps - 1], [int(start_color[3:5], 16), int(end_color[3:5], 16)]))
                    b = int(np.interp(i, [0, steps - 1], [int(start_color[5:], 16), int(end_color[5:], 16)]))
                    color = f'#{r:02x}{g:02x}{b:02x}'
                    gradient.append(color)
            return gradient
       
       
        red_pink = ["#CC313D", "#F7C5CC"]  # Shades of Cherry red & bubblegum pink
        gradient = create_gradient_colors(red_pink, 100)

        # Draw the gradient background
        for i, color in enumerate(gradient):
            canvas.create_rectangle(i * 8, 0, (i + 1) * 8, 100, fill=color, outline='')
        
        # Add a thank you message
        thank_you = "💕 Thank You for Playing! 💕"
        canvas.create_text(200, 50, text=thank_you, font=("Arial", 20, "bold"), fill="white")

    def start_new_game(self):
        # Close any existing game windows before starting a new game
        if hasattr(self, 'game_window'):
            self.game_window.destroy()
        # Prompt for player name and start a new game
        self.player_name = simpledialog.askstring("Player Name", "Enter your name:", parent=self.root)
        if self.player_name:
            self.memory_game = MemoryGame(grid_size=self.grid_size)
            self.start_time = time.time()
            self.create_game_ui()

    def create_game_ui(self):
        # Create a new game window of size 1000x600
        self.game_window = tk.Toplevel(self.root)
        self.game_window.geometry("1000x600")
        self.game_window.title("Memory Game")
        self.game_window.iconbitmap('game.ico')
        self.center_window(self.game_window)
        
        # Create a frame to hold the game canvas and side panel
        game_frame = tk.Frame(self.game_window, bg=self.colors['background'])
        game_frame.pack(fill="both", expand=True)

        # Create game canvas with a white border
        canvas_frame = tk.Frame(game_frame, bg=self.colors['border'], padx=2, pady=2)
        canvas_frame.pack(side=tk.LEFT, padx=30, pady=30)
        self.canvas = tk.Canvas(canvas_frame, width=self.grid_size * self.card_size, height=self.grid_size * self.card_size, bg=self.colors['background'], highlightthickness=0)
        self.canvas.pack()

        # Create side panel for moves and time
        side_panel = tk.Frame(game_frame, bg=self.colors['panel'], width=400, height=self.grid_size * self.card_size)
        side_panel.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 30), pady=30)
        side_panel.pack_propagate(False)  # Prevent the frame from shrinking

        # Add player name with truncation if it exceeds the given area
        if len(self.player_name) <= 10:
            player_label_text = f"Player: {self.player_name}"
        else:
            player_label_text = f"Player: {self.player_name[:10]}..."
        player_label = tk.Label(side_panel, text=player_label_text, font=("Arial", 18, "bold"), bg=self.colors['panel'], fg=self.colors['text'])
        player_label.pack(pady=(20, 15))

        # Create a frame for moves and time
        stats_frame = tk.Frame(side_panel, bg=self.colors['panel'])
        stats_frame.pack(pady=15)

        # Moves counter
        moves_icon = tk.Label(stats_frame, text="🔢", font=("Arial", 22), bg=self.colors['panel'], fg=self.colors['text'])
        moves_icon.grid(row=0, column=0, padx=(0, 8))
        self.moves_label = tk.Label(stats_frame, text="Moves: 0", font=("Arial", 18), bg=self.colors['panel'], fg=self.colors['text'])
        self.moves_label.grid(row=0, column=1, sticky="w")

        # Time counter
        time_icon = tk.Label(stats_frame, text="⏱️", font=("Arial", 22), bg=self.colors['panel'], fg=self.colors['text'])
        time_icon.grid(row=1, column=0, padx=(0, 8), pady=(8, 0))
        self.time_label = tk.Label(stats_frame, text="Time: 0.00 s", font=("Arial", 18), bg=self.colors['panel'], fg=self.colors['text'])
        self.time_label.grid(row=1, column=1, sticky="w", pady=(8, 0))

        # Add buttons for Return to Homescreen and New Game
        button_frame = tk.Frame(side_panel, bg=self.colors['panel'])
        button_frame.pack(pady=15)

        home_button = tk.Button(button_frame, text="Return to Homescreen", font=("Arial", 14, "bold"), bg=self.colors['button'], fg=self.colors['button_text'], command=self.create_initial_screen, padx=10, pady=5)
        home_button.pack(pady=5)

        new_game_button = tk.Button(button_frame, text="New Game", font=("Arial", 14, "bold"), bg=self.colors['button'], fg=self.colors['button_text'], command=self.start_new_game, padx=10, pady=5)
        new_game_button.pack(pady=5)
        
        
        # Add a beautiful design
        design_canvas = tk.Canvas(side_panel, width=300, height=100, bg=self.colors['panel'], highlightthickness=0)
        design_canvas.pack(pady=12)

        # Create a smooth gradient background from violet to red
        gradient_colors = ["#8B00FF", "#FF0000"]
        gradient = []
        for i in range(300):
            r = int(np.interp(i, [0, 299], [int(gradient_colors[0][1:3], 16), int(gradient_colors[-1][1:3], 16)]))
            g = int(np.interp(i, [0, 299], [int(gradient_colors[0][3:5], 16), int(gradient_colors[-1][3:5], 16)]))
            b = int(np.interp(i, [0, 299], [int(gradient_colors[0][5:], 16), int(gradient_colors[-1][5:], 16)]))
            color = f'#{r:02x}{g:02x}{b:02x}'
            gradient.append(color)

        for i, color in enumerate(gradient):
            design_canvas.create_line(i, 0, i, 100, fill=color)

        
        # Write "All the best!" in a beautiful cursive handwriting with a contrasting color (black & white)
        design_canvas.create_text(150, 50, text="All the Best!", font=("Brush Script MT", 40, "bold"), fill="black")
        design_canvas.create_text(152, 52, text="All the Best!", font=("Brush Script MT", 40, "bold"), fill="white")

        # Add a FUN FACT section
        fun_facts = [
            "DID YOU KNOW? In 1936, Russia built a computer that ran on water. It was used to solve partial differential equations.",
            "FUN FACT: The most expensive phone number is 666-6666. In 2006, it sold at a charity auction for £1.5m in Qatar.",
            "DID YOU KNOW? Amazon was originally an online bookstore called Cadabra. It came from the word 'abracadabra'.",
            "FUN FACT: The world's first 3D-printed car, the Strati, was created in 2014 and took just 44 hours to print.",
            "DID YOU KNOW? Samsung was founded in 1938 as a grocery store while Apple was founded in 1976."
        ]

        fun_fact = random.choice(fun_facts)
        fun_fact_label = tk.Label(side_panel, text=f'{fun_fact}', font=("Calibri", 12, "italic"), bg=self.colors['panel'], fg=self.colors['text'], wraplength=300, justify="left")
        fun_fact_label.pack(side=tk.BOTTOM, pady=15)

        # Bind click event and initialize game state
        self.canvas.bind("<Button-1>", self.on_click)
        self.first_card = None
        self.draw_board()

        # Start updating the time
        self.update_time()

    def update_time(self):
        elapsed_time = time.time() - self.start_time
        self.time_label.config(text=f"Time: {int(elapsed_time)} s")
        self.root.after(1000, self.update_time)  # Update every 1000ms = 1s

    def draw_board(self):
        # Get current board state and draw it on the canvas
        board = self.memory_game.get_board()
        self.canvas.delete("all")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1, y1 = j * self.card_size, i * self.card_size
                x2, y2 = x1 + self.card_size, y1 + self.card_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.colors['card_back'], outline=self.colors['text'])
                if board[i][j] != '':
                    # Draw colorful shapes and emojis instead of alphabets
                    if board[i][j] == 'A':
                        self.canvas.create_text(x1 + self.card_size/2, y1 + self.card_size/2, text='👽', font=('Arial', 54), fill=self.colors['text'], anchor='center')
                    elif board[i][j] == 'B':
                        self.canvas.create_text(x1 + self.card_size/2, y1 + self.card_size/2, text='💗', font=('Arial', 54), fill=self.colors['text'], anchor='center')
                    elif board[i][j] == 'C':
                        self.canvas.create_text(x1 + self.card_size/2, y1 + self.card_size/2, text='🦄', font=('Arial', 54), fill=self.colors['text'], anchor='center')
                    elif board[i][j] == 'D':
                        self.canvas.create_text(x1 + self.card_size/2, y1 + self.card_size/2, text='🍭', font=('Arial', 54), fill=self.colors['text'], anchor='center')
                    elif board[i][j] == 'E':
                        self.canvas.create_text(x1 + self.card_size/2, y1 + self.card_size/2, text='🌷', font=('Arial', 54), fill=self.colors['text'], anchor='center')
                    elif board[i][j] == 'F':
                        self.canvas.create_text(x1 + self.card_size/2, y1 + self.card_size/2, text='🧩', font=('Arial', 54), fill=self.colors['text'], anchor='center')
                    elif board[i][j] == 'G':
                        self.canvas.create_text(x1 + self.card_size/2, y1 + self.card_size/2, text='💡', font=('Arial', 54), fill=self.colors['text'], anchor='center')
                    elif board[i][j] == 'H':
                        self.canvas.create_text(x1 + self.card_size/2, y1 + self.card_size/2, text='💖', font=('Arial', 54), fill=self.colors['text'], anchor='center')

    def on_click(self, event):
        # Handle card click events
        x, y = event.x // self.card_size, event.y // self.card_size
        if self.first_card is None:
            if self.memory_game.flip_card(y, x):
                self.flip_sound.play()
                self.first_card = (x, y)
                self.draw_board()
        else:
            if self.memory_game.flip_card(y, x):
                self.flip_sound.play()
                self.draw_board()
                self.root.after(500, self.check_match, x, y)

    def check_match(self, x, y):
        # Check if the two flipped cards match
        if self.memory_game.check_match():
            self.match_sound.play()
        else:
            self.error_sound.play()

        self.first_card = None
        self.draw_board()
        self.moves_label.config(text=f"Moves: {self.memory_game.get_moves()}")

        # Check if the game is over
        if self.memory_game.is_game_over():
            end_time = time.time()
            time_taken = round(end_time - self.start_time, 2)
            congratulation_messages = [
                f"Congratulations {self.player_name}! You completed the game in {self.memory_game.get_moves()} moves.",
                f"Wow, {self.player_name}! You solved the game in {self.memory_game.get_moves()} moves.",
                f"Great job, {self.player_name}! You finished the game in {self.memory_game.get_moves()} moves.",
                f"Excellent work, {self.player_name}! You completed the game in {self.memory_game.get_moves()} moves.",
                f"Bravo, {self.player_name}! You solved the game in {self.memory_game.get_moves()} moves."
            ]
            self.game_window.destroy()
            random_message = random.choice(congratulation_messages)
            messagebox.showinfo("Game Over", random_message)
            self.score_manager.save_score(self.player_name, self.memory_game.get_moves(), time_taken)
            
            self.create_initial_screen()

    def show_history(self):
        # Display game history in a new window
        history = self.score_manager.get_scores()
        history_window = tk.Toplevel(self.root)
        history_window.title("Score History")
        history_window.iconbitmap('game.ico') 
        history_window.geometry("1000x600")
        history_window.configure(bg=self.colors['background'])
        self.center_window(history_window)  # Center the history window on the screen

        # Add a title to the history window
        tk.Label(history_window, 
                 text="Game History", 
                 font=("Arial", 26, "bold"), 
                 bg=self.colors['background'], 
                 fg=self.colors['text']).pack(pady=(20, 10))

        # Add a feature to sort the results
        sort_frame = tk.Frame(history_window, bg=self.colors['background'])
        sort_frame.pack(pady=10)

        sort_label = tk.Label(sort_frame, text="Sort by:", font=("Arial", 14), bg=self.colors['background'], fg=self.colors['text'])
        sort_label.pack(side=tk.LEFT, padx=10)

        sort_options = ["Game", "Player", "Moves", "Time Taken", "Date", "Time"]
        sort_variable = tk.StringVar(sort_frame)
        sort_variable.set(sort_options[0])  # Set the default value

        sort_menu = ttk.Combobox(sort_frame, textvariable=sort_variable, values=sort_options, state="readonly", width=16, font=("Arial", 12))
        sort_menu.pack(side=tk.LEFT, padx=10)

        sort_button = tk.Button(sort_frame, text="Sort", command=lambda: self.sort_table(table, sort_variable.get()),
                                bg=self.colors['button'], fg=self.colors['button_text'], 
                                font=("Arial", 14, "bold"), relief=tk.RAISED, bd=3)
        sort_button.pack(side=tk.LEFT, padx=10)

        # Create a frame for the table
        frame = tk.Frame(history_window, bg=self.colors['background'])
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Create the table
        table = ttk.Treeview(frame, columns=("Game", "Player", "Moves", "Time Taken", "Date", "Time"), show="headings")
        table.heading("Game", text="Game")
        table.heading("Player", text="Player")
        table.heading("Moves", text="Moves")
        table.heading("Time Taken", text="Time (sec)")
        table.heading("Date", text="Date")
        table.heading("Time", text="Time")

        # Configure column widths
        table.column("Game", width=100, anchor=tk.CENTER)
        table.column("Player", width=150, anchor=tk.CENTER) 
        table.column("Moves", width=100, anchor=tk.CENTER)
        table.column("Time Taken", width=120, anchor=tk.CENTER)
        table.column("Date", width=150, anchor=tk.CENTER)
        table.column("Time", width=120, anchor=tk.CENTER)

        # Insert data into the table
        for score in history:
            table.insert("", "end", values=score)

        table.pack(fill="both", expand=True)

        # Configure colors and fonts for the table
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
                        background=self.colors['background'],
                        foreground=self.colors['text'],
                        fieldbackground=self.colors['background'],
                        font=('Arial', 13))
        style.configure("Treeview.Heading", 
                        font=('Arial', 14, 'bold'),
                        background=self.colors['button'],
                        foreground=self.colors['button_text'])

    # Add a method to sort the table based on the selected option
    def sort_table(self, table, sort_option):
        # Sort the table based on the selected option
        if sort_option == "Game" or sort_option == "Moves" or sort_option == "Time Taken":
            data = [(float(table.set(child, sort_option)), child) for child in table.get_children('')]
        else:
            data = [(table.set(child, sort_option), child) for child in table.get_children('')]
        
        data.sort()
        for i, (val, child) in enumerate(data):
            table.move(child, '', i)

    def show_player_stats(self):
        # Create a new window for player stats
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Player Statistics")
        stats_window.iconbitmap('game.ico')
        stats_window.geometry("1000x600")
        stats_window.configure(bg=self.colors['background'])
        self.center_window(stats_window)

        # Load and process the data
        df = pd.read_csv('scores.csv')
        df['Time Taken'] = pd.to_numeric(df['Time Taken'])
        df['Moves'] = pd.to_numeric(df['Moves'])

        # Calculate average and best statistics
        avg_moves = df['Moves'].mean()
        avg_time = df['Time Taken'].mean()
        best_moves = df['Moves'].min()
        best_time = df['Time Taken'].min()

        # Create a figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        fig.patch.set_facecolor(self.colors['background'])

        # Define a new color scheme for the bars (Gwen-Spiderman themed)
        bar_colors = ['#FF69B4', '#00FFFF', '#FF1493', '#1E90FF']

        # Plot average and best moves
        ax1.bar(['Average', 'Best'], [avg_moves, best_moves], color=bar_colors[:2])
        ax1.set_ylabel('Moves', color=self.colors['text'])
        ax1.set_title('Moves Comparison', color=self.colors['text'])
        ax1.tick_params(colors=self.colors['text'])
        ax1.set_facecolor(self.colors['panel'])

        # Plot average and best time
        ax2.bar(['Average', 'Best'], [avg_time, best_time], color=bar_colors[:2])
        ax2.set_ylabel('Time (seconds)', color=self.colors['text'])
        ax2.set_title('Time Comparison', color=self.colors['text'])
        ax2.tick_params(colors=self.colors['text'])
        ax2.set_facecolor(self.colors['panel'])

        # Add value labels on top of each bar
        for ax in [ax1, ax2]:
            for i, v in enumerate(ax.containers[0]):
                ax.text(v.get_x() + v.get_width()/2, v.get_height(), f'{v.get_height():.2f}',
                        ha='center', va='bottom', color=self.colors['text'])

        # Adjust layout and add the plot to the window
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=stats_window)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

        # Add a dropdown to select a player for comparison
        player_frame = tk.Frame(stats_window, bg=self.colors['background'])
        player_frame.pack(pady=10)

        player_label = tk.Label(player_frame, text="Select a player:", font=("Arial", 14), bg=self.colors['background'], fg=self.colors['text'])
        player_label.pack(side=tk.LEFT, padx=10)

        players = df['Player Name'].unique().tolist()
        player_var = tk.StringVar(player_frame)
        player_var.set(players[0] if players else "No players")

        player_menu = ttk.Combobox(player_frame, textvariable=player_var, values=players, state="readonly", width=20, font=("Arial", 13))
        player_menu.pack(side=tk.LEFT, padx=10)

        compare_button = tk.Button(player_frame, text="Compare", command=lambda: self.update_player_stats(fig, ax1, ax2, canvas, df, player_var.get()),
                                   bg=self.colors['button'], fg=self.colors['button_text'], 
                                   font=("Arial", 14, "bold"), relief=tk.RAISED, bd=3)
        compare_button.pack(side=tk.LEFT, padx=10)

        # Add some decorative elements
        quote_frame = tk.Frame(stats_window, bg=self.colors['background'])
        quote_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        quotes = [
            '"The only way to do great work is to love what you do." - Steve Jobs',
            '"Success is not final, failure is not fatal: it is the courage to continue that counts." - Winston Churchill',
            '"The future belongs to those who believe in the beauty of their dreams." - Eleanor Roosevelt',
            '"Believe you can and you are halfway there." - Theodore Roosevelt',
            '"The secret of getting ahead is getting started." - Mark Twain'
        ]
        quote = random.choice(quotes)
        quote_label = tk.Label(quote_frame, text=quote, font=("Arial", 13, "italic"), bg=self.colors['background'], fg=self.colors['text'], wraplength=800)
        quote_label.pack()

    def update_player_stats(self, fig, ax1, ax2, canvas, df, selected_player):
        # Clear previous plots
        ax1.clear()
        ax2.clear()

        # Calculate average and best statistics
        avg_moves = df['Moves'].mean()
        avg_time = df['Time Taken'].mean()
        best_moves = df['Moves'].min()
        best_time = df['Time Taken'].min()

        # Get player's stats
        player_stats = df[df['Player Name'] == selected_player]
        player_avg_moves = player_stats['Moves'].mean()
        player_avg_time = player_stats['Time Taken'].mean()
        player_best_moves = player_stats['Moves'].min()
        player_best_time = player_stats['Time Taken'].min()


        # Define a new color scheme for the bars using only pinkish purplish shades
        bar_colors = ['#FF69B4', '#FF1493', '#E6DAC3', '#D2B48C']

        # Plot moves comparison
        moves_data = [avg_moves, best_moves, player_avg_moves, player_best_moves]
        ax1.bar(['Average', 'Best', f'{selected_player}\nAvg', f'{selected_player}\nBest'], 
                moves_data,
                color=bar_colors)
        ax1.set_ylabel('Moves', color=self.colors['text'])
        ax1.set_title('Moves Comparison', color=self.colors['text'])
        ax1.tick_params(colors=self.colors['text'])
        ax1.set_facecolor(self.colors['panel'])

        # Plot time comparison
        time_data = [avg_time, best_time, player_avg_time, player_best_time]
        ax2.bar(['Average', 'Best', f'{selected_player}\nAvg', f'{selected_player}\nBest'], 
                time_data,
                color=bar_colors)
        ax2.set_ylabel('Time (seconds)', color=self.colors['text'])
        ax2.set_title('Time Comparison', color=self.colors['text'])
        ax2.tick_params(colors=self.colors['text'])
        ax2.set_facecolor(self.colors['panel'])

        # Add value labels on top of each bar
        for ax, data in zip([ax1, ax2], [moves_data, time_data]):
            for i, v in enumerate(ax.containers[0]):
                ax.text(v.get_x() + v.get_width()/2, v.get_height(), f'{data[i]:.2f}',
                        ha='center', va='bottom', color=self.colors['text'])

        # Adjust layout and redraw
        plt.tight_layout()
        canvas.draw()
