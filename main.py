import tkinter as tk

from PIL import ImageTk, Image

import numpy as np
from tkinter import messagebox, simpledialog

ChessN = 0
def print_board(board):
    n = board.shape[0]
    for i in range(n):
        for j in range(n):
            if board[i, j] == 1:
                print('Q', end=' ')
            else:
                print('.', end=' ')
        print()

def is_safe(board, row, col):
    n = board.shape[0]

    # Check row and column
    for i in range(n):
        if board[row, i] == 1 or board[i, col] == 1:
            return False

    # Check diagonals
    for i in range(n):
        for j in range(n):
            if (i + j == row + col) or (i - j == row - col):
                if board[i, j] == 1:
                    return False

    return True

def evaluate(board):
    n = board.shape[0]
    score = 0

    # Count the number of queens in each row
    row_counts = np.sum(board, axis=1)
    score += np.sum(row_counts > 1)

    # Count the number of queens in each column
    col_counts = np.sum(board, axis=0)
    score += np.sum(col_counts > 1)

    # Count the number of queens in each diagonal
    diagonal_counts = []
    for i in range(2 * n - 1):
        diagonal_counts.append(np.sum(np.diagonal(board, i)))
        diagonal_counts.append(np.sum(np.diagonal(np.fliplr(board), i)))
    score += np.sum(np.array(diagonal_counts) > 1)

    return score

def minimax(board, depth, alpha, beta, is_maximizing_player):
    if depth == 0 or np.sum(board) == board.shape[0]:
        return evaluate(board)

    if is_maximizing_player:
        max_eval = float('-inf')
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if board[i, j] == 0 and is_safe(board, i, j):
                    board[i, j] = 1
                    eval = minimax(board, depth - 1, alpha, beta, False)
                    board[i, j] = 0
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval

    else:
        min_eval = float('inf')
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if board[i, j] == 0 and is_safe(board, i, j):
                    board[i, j] = 1
                    eval = minimax(board, depth - 1, alpha, beta, True)
                    board[i, j] = 0
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def get_best_move(board):
    best_score = float('-inf')
    best_move = None
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i, j] == 0 and is_safe(board, i, j):
                board[i, j] = 1
                score = minimax(board, 3, float('-inf'), float('inf'), False)
                board[i, j] = 0
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move
queen_photo = None
def draw_board(canvas, board):
    global queen_photo
    n = board.shape[0]
    canvas.delete("all")
    cell_size = 50

    # Draw the chessboard
    for row in range(n):
        for col in range(n):
            color = 'white' if (row + col) % 2 == 0 else 'gray'
            canvas.create_rectangle(col * cell_size, row * cell_size, (col + 1) * cell_size, (row + 1) * cell_size,
                                    fill=color)


    queen_image = Image.open("images/Queen.jpg")
    queen_image = queen_image.resize((cell_size, cell_size), Image.LANCZOS)
    queen_photo = ImageTk.PhotoImage(queen_image)

    # Place the queens on the chessboard
    for i in range(n):
        for j in range(n):
            if board[i, j] == 1:
                canvas.create_image(j * cell_size, i * cell_size, anchor='nw', image=queen_photo)

    canvas.update()

def on_board_click(event):
    global board, turn, canvas, ChessN, n

    col = event.x // 50
    row = event.y // 50

    if ChessN > 0:
        if board[row, col] == 0:
            if is_safe(board, row, col):
                board[row, col] = 1
                draw_board(canvas, board)
                ChessN -= 1

                if np.sum(board) == n:
                    messagebox.showinfo("Game Over", "You placed all the queens!")
                else:
                    ai_move()
            else:
                show_game_over_dialog("The position is unsafe. Try again.")
    else:
        show_game_over_dialog("No more queens left to place!")

def show_game_over_dialog(message):
    global ChessN, n
    result = messagebox.askretrycancel("Game Over", message, icon='error')

    if result:
        reset_game()
        ChessN = n
    else:
        pass



def reset_game():
    global board, turn, ChessN, n

    n = simpledialog.askinteger("Chess Queens", "Enter the number of rows/columns:")
    board = np.zeros((n, n))
    turn = 0
    ChessN = n

    # Clear the canvas and redraw the empty board
    canvas.delete('all')
    draw_board(canvas, board)


def ai_move():
    global board, turn, canvas, n

    move = get_best_move(board)
    row, col = move
    board[row, col] = 1
    draw_board(canvas, board)

    if np.sum(board) == n:
        print_board(board)
        print("Game over!")

def play_game(n):
    global board, turn, canvas

    board = np.zeros((n, n))
    turn = 0

    window = tk.Tk()
    window.title("N-Queens Game")
    canvas = tk.Canvas(window, width=n * 50, height=n * 50)
    canvas.pack()
    draw_board(canvas, board)
    canvas.bind("<Button-1>", on_board_click)
    window.mainloop()

# Start the game
n = int(input("Enter the size of the board: "))
ChessN = n
play_game(n)
