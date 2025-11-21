
import os
import tkinter as tk #gui
import chess  #board
import chess.engine #stockfish
from ai import ChatbotGUIai  #Import chatbot
#stockfish ki exe file ki location
STOCKFISH_PATH = r"C:\Users\kushi\OneDrive\Desktop\BOT\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"  

#check if stock is not there
if not os.path.exists(STOCKFISH_PATH):
    raise FileNotFoundError(f"Stockfish not found at {STOCKFISH_PATH}. Please check the path.")


class ChessBotGUI:
    def __init__(self, root): #__init__ method stock se connect karne k liye
        self.root = root
        self.root.title("Chess Bot (Human vs Stockfish)")

        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) #connect to stockfish

        self.canvas = tk.Canvas(root, width=400, height=400) 
        self.canvas.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
#canvas n grid tkinter k function h, canvas draws boards and grid set position
        
        self.status_label = tk.Label(root, text="Your move!", font=("Arial", 14))
        self.status_label.grid(row=1, column=0, pady=5)

        self.chatbot_frame = tk.Frame(root)
        self.chatbot_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ne")  

        self.chatbot = ChatbotGUIai(self.chatbot_frame)

        # Restart Game Button
        self.restart_button = tk.Button(root, text="Restart Game", font=("Arial", 12), command=self.restart_game)
        self.restart_button.grid(row=2, column=0, pady=5)

        self.time_label = tk.Label(root, text="AI thinking Time:", font=("Arial", 12))
        self.time_label.grid(row=3, column=0, pady=5)

        #slide
        self.time_slider = tk.Scale(root, from_=0.1, to=5, resolution=0.1, orient="horizontal", length=300)
        self.time_slider.set(1)  # Default to 1 second
        self.time_slider.grid(row=4, column=0, pady=5)



        self.draw_board() #khud se chess banane wala fun call kar diya
        self.canvas.bind("<Button-1>", self.on_click) #(2 things r connected -  left click hua jaha, on click walal function chal jye ga_ this function is made neeche)
        #button 1 -  left click (tk ka function h)
        self.selected_square = None

    def draw_board(self):
        #to draw
        self.canvas.delete("all") # ye nhi kiya to pichla wala hate ga nhi n overlapping hoke mess ban jye ga
        colors = ["#ffffff", "#a9a9a9"] #colors of square

        for row in range(8):
            for col in range(8):
                x1, y1 = col * 50, row * 50 
                x2, y2 = x1 + 50, y1 + 50
                #50 means pixels (size)
                color = colors[(row + col) % 2]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

        piece_symbols = {
            "r": "♜", "n": "♞", "b": "♝", "q": "♛", "k": "♚", "p": "♟",
            "R": "♖", "N": "♘", "B": "♗", "Q": "♕", "K": "♔", "P": "♙"
        }
        #lower case wale r black, upper wale r white
        for square in chess.SQUARES:   #chess.SQUARES r fron chess library jisme 64 squares h (0-63) ,i.e.  by this loop ham 64 sq se traverse kar rhe
            piece = self.board.piece_at(square) 
            if piece:
                col = square % 8
                row = 7 - (square // 8)
                x, y = col * 50 + 25, row * 50 + 25 #(+25 kiya taaki beech me gooti dikhe)
                self.canvas.create_text(x, y, text=piece_symbols[piece.symbol()], font=("Arial", 24), fill="blue")
                                 # piece.symbol() returns something like "r" (rook) or "K" (king)
                                #piece_symbols[...] converts that into the correct Unicode character
                                        
    def on_click(self, event):
        #connected above 
        #to check click(by user)
        col, row = event.x // 50, event.y // 50 #(event tells pixel ki postion)
        square = chess.square(col, 7 - row) #(make a square)

        if self.selected_square is None: #ye batata h ki pehle is kuch selected to nhi
            piece = self.board.piece_at(square)
            if piece and piece.color == chess.WHITE:  #agar selected nhi h to user ko select karne ka chance deta h and also checks ki white wala chose hua ho
                self.selected_square = square
        else:       #agar already selected h koi square, to vo piece ko kaha chalna ye dekhta h
            move = chess.Move(self.selected_square, square) #1st n 2nd click
            if move in self.board.legal_moves:
                self.board.push(move) #agar 2nd move leagal h to move ho jye ga
                self.selected_square = None
                self.draw_board()
                self.root.after(500, self.bot_move) 
            else:
                self.status_label.config(text=" Illegal move! Try again.")
                self.selected_square = None 

    def bot_move(self):
         if not self.board.is_game_over():
            thinking_time = self.time_slider.get()  # Get slider value (bina iske bhi chale ga)
            result = self.engine.play(self.board, chess.engine.Limit(time=thinking_time)) #1st function me ye banaya h
            self.board.push(result.move) #move by stock
            self.draw_board()  #ye basicaly jo dikhe ga uske liye h, ye nhi kiya to bot ki chal nhi dikhe gi
            self.status_label.config(text="Your move!")


    def restart_game(self):
        #restart karne k liye
        self.board.reset()
        self.selected_square = None
        self.status_label.config(text="Your move!")
        self.draw_board()

    def close_engine(self):
        #engine k sath stockfish bhi band ho
        self.engine.quit()

#GUI
if __name__ == "__main__":  #actual me code run kar rha ya still working as module
    root = tk.Tk() #jaha jaha root word use kiya h, yaha pe usse define kiya i.e. it is main window
    app = ChessBotGUI(root) #jo class banayi h upar usse call kara
    root.protocol("WM_DELETE_WINDOW", app.close_engine)  # to check engine close h ki nhi, agar ham cross wala button press kare ge upar se to colse wala function chal jye ga
    root.mainloop() #tk ko start karne k liye

