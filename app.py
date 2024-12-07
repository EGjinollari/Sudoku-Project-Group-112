'''
######

NEED TO:
Add "Game over" and "you won" screen.
simplify code to an easier level in app.py
Can sketched-and-confirmed cells be resketched?

######
'''
import pygame
from board import Board

# Constants for screen dimensions and colors
SCREEN_WIDTH = 603 # Closest integer to 600 that is divisible by 9
SCREEN_HEIGHT = 700
BACKGROUND_COLOR = (255, 255, 255)
BUTTON_COLOR = (175, 175, 255)
TEXT_COLOR = (0, 0, 0)

"""
    Draws the Reset, Restart, and Exit buttons

    Return: Reset, Restart, and Exit buttons to use in the main loop
"""

def draw_game_buttons(screen):
    font = pygame.font.Font(None, 36)
    button_labels = ["Reset", "Restart", "Exit"]
    button_positions = [SCREEN_WIDTH // 2 - 140, SCREEN_WIDTH // 2, SCREEN_WIDTH // 2 + 140]
    button_rects = []

    for i in range(len(button_labels)):
        rect = pygame.Rect(button_positions[i] - 60, SCREEN_HEIGHT - 50, 120, 40)
        pygame.draw.rect(screen, BUTTON_COLOR, rect)
        text = font.render(button_labels[i], True, TEXT_COLOR)
        screen.blit(text, text.get_rect(center=rect.center))
        button_rects.append(rect)
    
    pygame.display.flip()

    return button_rects[0], button_rects[1], button_rects[2]  # Returns Reset, Restart, and Exit button rects

'''
    Draws the game board along with all UI elements
'''

def update_board(screen, board):
    screen.fill(BACKGROUND_COLOR)
    board.draw()
    buttons = draw_game_buttons(screen)
    pygame.display.flip()

    return buttons


'''
    Draws the Easy, Medium, and Hard buttons

    Returns: The easy, medium, and hard buttons to be used in the main loop 
'''

def draw_difficulty_buttons(screen):
    font = pygame.font.Font(None, 48)
    title_text = font.render("Select Difficulty", True, TEXT_COLOR)
    screen.fill(BACKGROUND_COLOR)
    screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))
    
    button_labels = ["Easy", "Medium", "Hard"]
    button_positions = [SCREEN_WIDTH // 4, SCREEN_WIDTH // 2, SCREEN_WIDTH * 3 // 4]
    button_rects = []

    for i in range(len(button_labels)):
        rect = pygame.Rect(button_positions[i] - 50, 400, 140, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, rect)
        text = font.render(button_labels[i], True, TEXT_COLOR)
        screen.blit(text, text.get_rect(center=rect.center))
        button_rects.append(rect)

    return button_rects[0], button_rects[1], button_rects[2]  # Returns Easy, Medium, and Hard button rects

"""
    Displays the Game Over screen with a Restart button

    Return: The restart button in the game over menu to be used in main()
"""

def draw_game_over_screen(screen):
    screen.fill(BACKGROUND_COLOR)

    # Game Over text
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("Game Over!", True, TEXT_COLOR)
    screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))

    # Restart button
    button_font = pygame.font.Font(None, 48)
    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2, 120, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, restart_button)
    restart_text = button_font.render("Restart", True, TEXT_COLOR)
    screen.blit(restart_text, restart_text.get_rect(center=restart_button.center))

    pygame.display.flip()  # Update the screen with the new elements
    return restart_button

"""
    Displays the Game Won screen with a Restart button

    Return: The exit button in the game won menu to be used in main()
"""

def draw_game_won_screen(screen):
    """Displays the Game Won screen with only an Exit button."""
    screen.fill(BACKGROUND_COLOR)

    # Game Over text
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("Game Won!", True, TEXT_COLOR)
    screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))

    # Restart button
    button_font = pygame.font.Font(None, 48)
    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2, 120, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, restart_button)
    restart_text = button_font.render("Exit Game", True, TEXT_COLOR)
    screen.blit(restart_text, restart_text.get_rect(center=restart_button.center))

    pygame.display.flip()  # Update the screen with the new elements
    return restart_button

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sudoku Game")
    clock = pygame.time.Clock()

    running = True

    # Difficulty buttons
    easy_button, medium_button, hard_button = draw_difficulty_buttons(screen)
    pygame.display.flip()

    difficulty = None
    while difficulty is None and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    difficulty = "easy"
                elif medium_button.collidepoint(event.pos):
                    difficulty = "medium"
                elif hard_button.collidepoint(event.pos):
                    difficulty = "hard"

    # Initialize the Sudoku board
    board = Board(SCREEN_WIDTH, SCREEN_WIDTH, screen, difficulty)

    # Main game loop
    game_over = False
    game_won = False

    while running:
        if not (game_over or game_won): # While user is playing, update UI
            reset_btn, restart_btn, exit_btn = update_board(screen, board)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                break

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if reset_btn.collidepoint(event.pos): # User presses reset button
                    board.reset_to_original()

                elif restart_btn.collidepoint(event.pos): # User presses restart button
                    main()  # Restart the game via recursion

                elif exit_btn.collidepoint(event.pos): # User presses exit button
                    running = False
                    break

                else:
                    cell = board.click(event.pos[0], event.pos[1])
                    if cell:
                        board.select(cell[0], cell[1])

            elif event.type == pygame.KEYDOWN:
                if board.selected:
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        board.sketch(event.key - pygame.K_0) # cool trick get the sketch value

                    elif event.key == pygame.K_RETURN:
                        row, col = board.selected
                        value = board.cells[row][col].sketched_value

                        if value != 0:
                            board.place_number(value)

                            if board.is_full() and not (game_over or game_won):
                                if board.check_board(): # If user won
                                    print("Sudoku Solved Successfully!")
                                    game_won = True
                                    exit_btn = draw_game_won_screen(screen)
                                    
                                else: # If user lost
                                    game_over = True
                                    restart_btn = draw_game_over_screen(screen)

    pygame.quit()

if __name__ == "__main__":
    main()