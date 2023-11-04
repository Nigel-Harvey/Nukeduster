import pygame
from data import constants


class TBoxEdit:
    def __init__(self, x_coord, y_coord, width, height, font_size=50):
        self.rectangle = pygame.Rect(x_coord, y_coord, width, height)
        self.font = pygame.font.Font(None, font_size)
        self.text = ""
        self.active = False
        self.hovering = False
        self.colour = constants.GREY
        self.hover_colour = constants.GREY_DARK

    def set_position(self, x_coord, y_coord):
        self.rectangle = pygame.Rect(x_coord, y_coord, self.width, self.length)

    def draw(self, screen):
        # if the box is being hovered over with the mouse
        if self.hovering:
            pygame.draw.rect(screen, self.hover_colour, self.rectangle)
        else:
            pygame.draw.rect(screen, self.colour, self.rectangle)

        # set the border colour of the editable text box
        colour_border = constants.BLACK
        if self.active:
            colour_border = constants.WHITE
        pygame.draw.rect(screen, colour_border, self.rectangle, 5)

        # set text and blit to screen
        text_surface = self.font.render(self.text, True, constants.BLACK)
        screen.blit(text_surface, (self.rectangle.x + 5, self.rectangle.y + 5))

    def handle_event(self, event):
        # if the mouse cursor moves
        if event.type == pygame.MOUSEMOTION:
            # set hovering to True if the mouse curser is within the buttons coordinates
            if self.rectangle.collidepoint(event.pos):
                self.hovering = True
            else:
                if not self.active:
                    self.hovering = False
        
        # if the user left clicks the text box, set the box to active
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rectangle.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

        # if the user types a key and the box is clicked
        if event.type == pygame.KEYDOWN:
            if self.active:
                # if the enter or return key is pressed
                if event.key == pygame.K_RETURN:
                    self.active = False
                # if the backspace key is pressed
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                # if any other key is pressed
                else:
                    self.text += event.unicode
