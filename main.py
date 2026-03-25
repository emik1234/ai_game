from random import randint
import customtkinter as ctk
from state import GameState
from ai import minimax, alpha_beta
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GameGUI:
    def __init__(self, root, search_depth) -> None:
        self.root = root
        self.root.title("Skaitļu spēle")
        self.root.geometry("1600x700")

        self.current_state = None
        self.search_depth = search_depth

        self.build_ui()

    def build_ui(self):
        self.settings_frame = ctk.CTkFrame(self.root)
        self.settings_frame.pack(pady=20, padx=20, fill="x")

        # choose length of numbers
        ctk.CTkLabel(self.settings_frame, text="Skaitļu Garums (15-25):").grid(row=0, column=0, padx=10, pady=10)
        self.length_entry = ctk.CTkEntry(self.settings_frame, width=60)
        self.length_entry.grid(row=0, column=1, padx=10, pady=10)

        # choose starter
        ctk.CTkLabel(self.settings_frame, text="Spēli sāk:").grid(row=0, column=2, padx=10)
        self.starter_var = ctk.StringVar(value="Cilvēks")
        self.starter_menu = ctk.CTkOptionMenu(self.settings_frame, values=["Cilvēks", "Dators"], variable=self.starter_var)
        self.starter_menu.grid(row=0, column=3, padx=10)

        # choose algorithm
        ctk.CTkLabel(self.settings_frame, text="Algoritms:").grid(row=0, column=4, padx=10)
        self.algo_var = ctk.StringVar(value="Alfa-Beta")
        self.algo_menu = ctk.CTkOptionMenu(self.settings_frame, values=["Alfa-Beta", "Minimax"], variable=self.algo_var)
        self.algo_menu.grid(row=0, column=5, padx=10)

        # start button
        self.start_button = ctk.CTkButton(self.settings_frame, text="Sākt", command=self.start_game, fg_color="green", hover_color="darkgreen")
        self.start_button.grid(row=0, column=6, padx=20)

        # frame
        self.info_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.info_frame.pack(pady=10, fill="x")

        # turn label
        self.turn_label = ctk.CTkLabel(self.info_frame, text="Izvēlies spēles noteikumus un spied 'Sākt'", font=("Arial", 18, "bold"))
        self.turn_label.pack(pady=5)

        # score label
        self.score_label = ctk.CTkLabel(self.info_frame, text="Cilvēks: 0  |  Dators: 0", font=("Arial", 16))
        self.score_label.pack(pady=5)

        # main game board
        self.board_frame = ctk.CTkFrame(self.root)
        self.board_frame.pack(pady=20, padx=20, fill="both", expand=True)


    def start_game(self):
        try:
            # get list length
            length = int(self.length_entry.get())
            
            # check against constraints
            if not (15 <= length <= 25):
                raise ValueError
        except ValueError:
            print("Error")
            return
        
        # choose random numbers
        sequence = [randint(1, 9) for _ in range(length)]

        # define who starts
        computer_starts = (self.starter_var.get() == "Dators")

        # define starting Game State
        self.current_state = GameState(sequence, max_score=0, min_score=0, max_turn=computer_starts)

        self.total_nodes = 0
        self.total_time = 0.0
        self.computer_moves_count = 0

        self.update_ui()

    def update_ui(self):
        if not self.current_state:
            return
        
        # show scores
        self.score_label.configure(text=f"Cilvēks: {self.current_state.min_score}  |  Dators: {self.current_state.max_score}")
        
        # check if the game has ended
        if self.current_state.is_terminal():
            winner_text = "Neizšķirts!"
            text_color = "yellow"

            # define winner
            if self.current_state.max_score > self.current_state.min_score:
                winner_text = "Dators Uzvarēja!"
                text_color = "red"
                
            elif self.current_state.max_score < self.current_state.min_score:
                winner_text = "Tu uzvarēji!"
                text_color = "green"
            
            # show winner
            self.turn_label.configure(text=f"Spēle Beigusies! {winner_text}", text_color=text_color)
            self.draw_board(disable_all=True)
            self.start_button.configure(text="Spēlēt vēlreiz")

            print("\n" + "="*40)
            print("=== SPĒLES EKSPERIMENTA REZULTĀTI ===")
            print(f"Algoritms: {self.algo_var.get()} (Dziļums: {self.search_depth})")
            print(f"Uzvarētājs: {winner_text}")
            
            if self.computer_moves_count > 0:
                avg_time = self.total_time / self.computer_moves_count
                print(f"Kopējais ģenerēto virsotņu skaits: {self.total_nodes}")
                print(f"Datora gājienu skaits: {self.computer_moves_count}")
                print(f"Kopējais patērētais laiks: {self.total_time:.4f} sekundes")
                print(f"Vidējais laiks 1 gājienam: {avg_time:.4f} sekundes")
            else:
                print("Dators neveica nevienu gājienu.")
            print("="*40 + "\n")

            return
        
        # show whose turn it is
        if self.current_state.max_turn:
            self.turn_label.configure(text="Dators izvēlas skaitļus...", text_color="cyan")
            self.draw_board(disable_all=True)
            self.root.update()
            self.root.after(300, self.computer_move)
        else:
            self.turn_label.configure(text="Tava kārta!", text_color="lightgreen")
            self.draw_board(disable_all=False)

    def draw_board(self, disable_all=False):
        if not self.current_state:
            return
        
        # destroy currently drawn objects
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        # get current list of numbers
        sequence = self.current_state.current_sequence
        max_per_row = 12

        # iterate the list of numbers left
        for i, val in enumerate(sequence):
            row_index = (i // max_per_row) * 2
            col_index = (i % max_per_row) * 2

            # draw number
            label = ctk.CTkLabel(self.board_frame, text=str(val), font=("Arial", 22, "bold"), 
                               width=45, height=45, fg_color="gray30", corner_radius=8)
            
            label.grid(row=row_index, column=col_index, padx=5, pady=15)
            
            # draw the '+' signs
            if i < len(sequence) - 1:
                button_state = "disabled" if disable_all else "normal"
                
                # draw on the same row if it isn't the last number in the row
                if (i + 1) % max_per_row != 0:
                    btn = ctk.CTkButton(self.board_frame, text="+", width=30, height=30, 
                                        state=button_state, command=lambda idx=i: self.human_move(idx))
                    btn.grid(row=row_index, column=col_index + 1, padx=2)
                else:
                    # draw a button below the number if it's the last in the row
                    btn = ctk.CTkButton(self.board_frame, text="↴", width=30, height=30, 
                                        state=button_state, fg_color="darkblue",
                                        command=lambda idx=i: self.human_move(idx))
                    
                    btn.grid(row=row_index + 1, column=col_index, pady=2)
    
    def human_move(self, index):
        if not self.current_state:
            return
        
        # generate children nodes
        children = self.current_state.generate_nodes()

        # apply chosen state
        self.current_state = children[index]
        
        self.update_ui()

    def computer_move(self):
        if not self.current_state:
            return
        
        algorithm = self.algo_var.get()

        stats = {"nodes": 0}
        start_time = time.time()

        # choose the algorithm based on settings
        if algorithm == "Alfa-Beta":
            _, best_state = alpha_beta(self.current_state, self.search_depth, float("-inf"), float("inf"), True, stats)
        else:
            _, best_state = minimax(self.current_state, self.search_depth, True, stats)

        end_time = time.time()
        time_taken = end_time - start_time

        self.total_nodes += stats["nodes"]
        self.total_time += time_taken
        self.computer_moves_count += 1

        if best_state:
            self.current_state = best_state

        self.update_ui()

if __name__ == "__main__":
    # create main app loop
    search_depth = 4

    app = ctk.CTk()
    gui = GameGUI(app, search_depth)
    app.mainloop()