import pygame

class Cell:
    '''
        Create a sudoku cell - Initialize instance variables set properties for displaying cells
        
        self.value   - Initial value of the cell
        self.row     - Row position of the cell
        self.col     - Column position of the cell
        self.screen  - Pygame screen surface
    '''

    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        
        self.sketched_value = 0
        
        self.selected = False
        
        self.length = screen.get_width() // 9
    
    '''
        Setter for the cell's value
        
        Parameters:
        value is the new value to set for the cell

        Return: None
    '''
    
    def set_cell_value(self, value):
        self.value = value
    
    '''
        Setter for the cell's sketched value
        
        Parameters:
        value is the new sketched value to set for the cell

        Return: None
    '''

    def set_sketched_value(self, value):
        self.sketched_value = value
    
    '''
    Draws the cell on the screen, including its value and selection state

    Parameters: None
    
    Return: None
    '''

    def draw(self):
        x = self.col * self.length
        y = self.row * self.length
        
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        WHITE = (255, 255, 255)
        
        pygame.draw.rect(self.screen, BLACK, (x, y, self.length, self.length), 2)
        
        if self.selected:
            pygame.draw.rect(self.screen, RED, (x, y, self.length, self.length), 3)
        
        if self.value != 0:
            font = pygame.font.Font(None, 40)
            text = font.render(str(self.value), True, BLACK)
            text_rect = text.get_rect(center=(x + self.length//2, y + self.length//2))
            self.screen.blit(text, text_rect)
        
        if self.sketched_value != 0:
            font = pygame.font.Font(None, 40)
            text = font.render(str(self.sketched_value), True, pygame.Color(125, 125, 125))
            text_rect = text.get_rect(center=(x + self.length//2, y + self.length//2))
            self.screen.blit(text, text_rect)