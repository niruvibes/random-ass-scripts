# Define the pieces
pieces = {'R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚', 'P': '♟',
          'r': '♖', 'n': '♘', 'b': '♗', 'q': '♕', 'k': '♔', 'p': '♙',
          ' ': ''}

# Define the initial board
board = [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
         ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
         ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']]

def print_board():
    for i in range(8):
        for j in range(8):
            # Print each piece with its color
            if (i + j) % 2 == 0:
                print(f"\033[30m{pieces[board[i][j]]}\033[0m", end="")
            else:
                print(f"\033[37m{pieces[board[i][j]]}\033[0m", end="")
        # Add a newline character after each row is printed
        print("\n")



# Function to move a piece
def move_piece(current_pos, new_pos):
    # Get the row and column of the current and new positions
    current_row, current_col = current_pos
    new_row, new_col = new_pos

    # Make sure the current and new positions are on the board
    if current_row < 1 or current_row > 8 or current_col < 1 or current_col > 8:
        raise ValueError("Current position is not on the board")
    if new_row < 1 or new_row > 8 or new_col < 1 or new_col > 8:
        raise ValueError("New position is not on the board")

    # Make sure the current position has a piece on it
    if board[current_row - 1][current_col - 1] == ' ':
        raise ValueError("There is no piece at the current position")

    # Update the board with the move
    board[new_row - 1][new_col - 1] = board[current_row - 1][current_col - 1]
    board[current_row - 1][current_col - 1] = ' '

# Main function
def main():
    # Reverse the order of the rows in the board
    board.reverse()

    # Print the initial board
    print_board()

    # Move the white king's pawn one square forward
    move_piece((2, 2), (3, 2))

    # Print the updated board
    print_board()


# Call the main function
main()
