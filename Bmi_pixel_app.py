import pygame
import sys
import os

# Initialize pygame
pygame.init()

# Constants
PIXEL_SIZE = 4
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FONT_SIZE = 16

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (13, 28, 61)
LIGHT_BLUE = (66, 133, 244)
GREEN = (106, 190, 48)
YELLOW = (255, 213, 0)
ORANGE = (255, 128, 0)
RED = (255, 0, 0)
PURPLE = (146, 7, 131)
BLUE = (0, 121, 241)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pixel BMI Calculator")

# Load font
try:
    font = pygame.font.Font("PressStart2P-Regular.ttf", FONT_SIZE)
except:
    font = pygame.font.SysFont("courier", FONT_SIZE, bold=True)

# Background (optional)
bg_image = None
if os.path.exists("bg_city.jpg"):
    bg_image = pygame.image.load("bg_city.jpg")
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Input box class
class PixelInputBox:
    def __init__(self, x, y, width, height, default_text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = DARK_BLUE
        self.text = default_text
        self.active = False
        self.cursor_visible = False
        self.cursor_timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit() or event.unicode == ".":
                self.text += event.unicode

    def update(self):
        self.cursor_timer += 1
        if self.cursor_timer > 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        border_color = LIGHT_BLUE if self.active else WHITE
        pygame.draw.rect(surface, border_color, self.rect, 2)

        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        surface.blit(text_surf, text_rect)

        if self.active and self.cursor_visible:
            cursor_x = text_rect.right + 2
            pygame.draw.rect(surface, WHITE, (cursor_x, self.rect.y + 5, 8, self.rect.height - 10))

# Button class
class PixelButton:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface):
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)

        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def check_click(self, pos, event):
        return self.rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

# Character sprite
def draw_pixel_character(x, y, size, color):
    pygame.draw.rect(screen, color, (x, y, size*3, size*3))  # Head
    pygame.draw.rect(screen, color, (x + size, y + size*3, size, size*4))  # Body
    pygame.draw.rect(screen, color, (x - size, y + size*4, size, size))  # Left arm
    pygame.draw.rect(screen, color, (x + size*3, y + size*4, size, size))  # Right arm
    pygame.draw.rect(screen, color, (x, y + size*7, size, size*2))  # Left leg
    pygame.draw.rect(screen, color, (x + size*2, y + size*7, size, size*2))  # Right leg

# UI Elements
weight_input = PixelInputBox(100, 200, 200, 40)
height_input = PixelInputBox(100, 300, 200, 40)
calculate_button = PixelButton(100, 400, 200, 50, "CALCULATE", GREEN, YELLOW)
result_text = ""
bmi_value = 0

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        weight_input.handle_event(event)
        height_input.handle_event(event)

        if calculate_button.check_click(mouse_pos, event):
            try:
                weight = float(weight_input.text)
                height = float(height_input.text) / 100
                bmi_value = weight / (height ** 2)

                if bmi_value < 18.5:
                    result_text = f"BMI: {bmi_value:.1f} - Underweight"
                    char_color = BLUE
                elif 18.5 <= bmi_value < 25:
                    result_text = f"BMI: {bmi_value:.1f} - Normal weight"
                    char_color = GREEN
                elif 25 <= bmi_value < 30:
                    result_text = f"BMI: {bmi_value:.1f} - Overweight"
                    char_color = YELLOW
                else:
                    result_text = f"BMI: {bmi_value:.1f} - Obese"
                    char_color = RED
            except:
                result_text = "Please enter valid numbers"

    weight_input.update()
    height_input.update()
    calculate_button.check_hover(mouse_pos)

    # Draw background
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(BLACK)

    # Title
    title_surf = font.render("BMI CALCULATOR", True, LIGHT_BLUE)
    screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 50))

    # Labels
    weight_label = font.render("WEIGHT (kg):", True, WHITE)
    screen.blit(weight_label, (100, 170))
    height_label = font.render("HEIGHT (cm):", True, WHITE)
    screen.blit(height_label, (100, 270))

    # Draw UI
    weight_input.draw(screen)
    height_input.draw(screen)
    calculate_button.draw(screen)

    # Result
    if result_text:
        result_surf = font.render(result_text, True, WHITE)
        screen.blit(result_surf, (SCREEN_WIDTH//2 - result_surf.get_width()//2, 480))
        if bmi_value > 0:
            draw_pixel_character(180, 510, PIXEL_SIZE, char_color)

    # Footer
    footer_text = font.render("PIXEL HEALTH 2023 - Made by GS", True, PURPLE)
    screen.blit(footer_text, (SCREEN_WIDTH//2 - footer_text.get_width()//2, 570))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
