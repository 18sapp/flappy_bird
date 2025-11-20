"""
Pipe obstacle system
"""

import pygame
import random
from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PIPE_WIDTH, PIPE_GAP,
    PIPE_SPEED, PIPE_SPAWN_DISTANCE, PIPE_MIN_HEIGHT, PIPE_MAX_HEIGHT,
    PIPE_COLOR, PIPE_HORIZONTAL_PADDING
)


class Pipe(pygame.sprite.Sprite):
    """Single pipe obstacle"""
    
    def __init__(self, x, gap_y, is_top=False):
        super().__init__()
        self.is_top = is_top
        
        if is_top:
            # Top pipe (hangs from top) - Mario style with horizontal padding
            height = gap_y
            cap_height = 20
            total_height = height + cap_height
            
            # Add horizontal padding to image width
            image_width = PIPE_WIDTH + (PIPE_HORIZONTAL_PADDING * 2)
            self.image = pygame.Surface((image_width, total_height), pygame.SRCALPHA)
            
            # Draw horizontal extension at the bottom (opening)
            padding_y = total_height - cap_height  # Position at the opening
            # Left horizontal extension
            pygame.draw.rect(self.image, PIPE_COLOR, 
                            (0, padding_y - 5, PIPE_HORIZONTAL_PADDING, cap_height + 10))
            pygame.draw.rect(self.image, PIPE_COLOR, 
                            (0, padding_y - 5, PIPE_HORIZONTAL_PADDING, cap_height + 10), 2)
            # Right horizontal extension
            pygame.draw.rect(self.image, PIPE_COLOR, 
                            (PIPE_WIDTH + PIPE_HORIZONTAL_PADDING, padding_y - 5, 
                             PIPE_HORIZONTAL_PADDING, cap_height + 10))
            pygame.draw.rect(self.image, PIPE_COLOR, 
                            (PIPE_WIDTH + PIPE_HORIZONTAL_PADDING, padding_y - 5, 
                             PIPE_HORIZONTAL_PADDING, cap_height + 10), 2)
            
            # Draw pipe cap/rim (top part)
            pipe_x = PIPE_HORIZONTAL_PADDING
            pygame.draw.rect(self.image, PIPE_COLOR, 
                           (pipe_x, 0, PIPE_WIDTH, cap_height))
            pygame.draw.rect(self.image, PIPE_COLOR, 
                           (pipe_x, 0, PIPE_WIDTH, cap_height), 2)
            
            # Draw pipe body (offset by horizontal padding)
            pipe_y = cap_height
            pygame.draw.rect(self.image, PIPE_COLOR, 
                            (pipe_x, pipe_y, PIPE_WIDTH, height))
            
            # Draw vertical borders
            pygame.draw.line(self.image, PIPE_COLOR, 
                            (pipe_x, pipe_y), (pipe_x, total_height), 3)
            pygame.draw.line(self.image, PIPE_COLOR, 
                            (pipe_x + PIPE_WIDTH-1, pipe_y), 
                            (pipe_x + PIPE_WIDTH-1, total_height), 3)
            
            # Draw light green area starting from top (covering full height)
            highlight_width = 15  # Width of the light green area
            pygame.draw.rect(self.image, PIPE_COLOR, 
                            (pipe_x, 0, highlight_width, total_height))
            
            # Draw horizontal bands for texture (only on right side, not in highlight area)
            # Skip the highlight area on the left side
            for y in range(pipe_y + 20, total_height, 20):
                # Draw band only on the right side (after highlight area)
                pygame.draw.line(self.image, PIPE_COLOR, 
                               (pipe_x + highlight_width + 5, y), 
                               (pipe_x + PIPE_WIDTH-5, y), 1)
            
            self.rect = self.image.get_rect()
            # Adjust x position to account for padding (center the pipe body)
            self.rect.x = x - PIPE_HORIZONTAL_PADDING
            self.rect.y = 0
            
            # Store collision rect (only the main pipe body, not the extensions)
            self.collision_rect = pygame.Rect(x, 0, PIPE_WIDTH, total_height)
        else:
            # Bottom pipe (rises from bottom) - Mario style with horizontal padding
            height = SCREEN_HEIGHT - (gap_y + PIPE_GAP)
            cap_height = 20
            
            # Add horizontal padding to image width
            image_width = PIPE_WIDTH + (PIPE_HORIZONTAL_PADDING * 2)
            self.image = pygame.Surface((image_width, height + cap_height), pygame.SRCALPHA)
            
            # Draw horizontal extension at the BEGINNING (top, y=0) instead of at the opening
            padding_y = 0  # Position at the beginning/top
            # Left horizontal extension
            pygame.draw.rect(self.image, PIPE_COLOR, 
                            (0, padding_y - 5, PIPE_HORIZONTAL_PADDING, cap_height + 10))
            pygame.draw.rect(self.image, PIPE_COLOR, 
                            (0, padding_y - 5, PIPE_HORIZONTAL_PADDING, cap_height + 10), 2)
            # Right horizontal extension
            pygame.draw.rect(self.image, PIPE_COLOR, 
                            (PIPE_WIDTH + PIPE_HORIZONTAL_PADDING, padding_y - 5, 
                             PIPE_HORIZONTAL_PADDING, cap_height + 10))
            pygame.draw.rect(self.image, PIPE_COLOR, 
                            (PIPE_WIDTH + PIPE_HORIZONTAL_PADDING, padding_y - 5, 
                             PIPE_HORIZONTAL_PADDING, cap_height + 10), 2)
            
            # Draw pipe body (offset by horizontal padding)
            pipe_x = PIPE_HORIZONTAL_PADDING
            pygame.draw.rect(self.image, PIPE_COLOR, 
                            (pipe_x, 0, PIPE_WIDTH, height))
            
            # Draw vertical borders
            pygame.draw.line(self.image, PIPE_COLOR, 
                            (pipe_x, 0), (pipe_x, height), 3)
            pygame.draw.line(self.image, PIPE_COLOR, 
                            (pipe_x + PIPE_WIDTH-1, 0), (pipe_x + PIPE_WIDTH-1, height), 3)
            
            # Draw light green area starting from bottom (going upward)
            highlight_width = 15  # Width of the light green area
            highlight_height = height // 3  # Height of the light green area (1/3 of pipe height)
            # Draw light green area starting from bottom (going upward)
            pygame.draw.rect(self.image, PIPE_COLOR, 
                            (pipe_x, height - highlight_height, highlight_width, highlight_height))
            
            # Draw horizontal bands for texture (only on right side, not in highlight area)
            for y in range(20, height, 20):
                # Draw band only on the right side (after highlight area)
                pygame.draw.line(self.image, PIPE_COLOR, 
                               (pipe_x + highlight_width + 5, y), 
                               (pipe_x + PIPE_WIDTH-5, y), 1)
            
            # Draw pipe cap/rim (bottom part, at the opening)
            cap_y = height
            pygame.draw.rect(self.image, PIPE_COLOR, 
                            (pipe_x, cap_y, PIPE_WIDTH, cap_height))
            pygame.draw.rect(self.image, PIPE_COLOR, 
                            (pipe_x, cap_y, PIPE_WIDTH, cap_height), 2)
            
            self.rect = self.image.get_rect()
            # Adjust x position to account for padding
            self.rect.x = x - PIPE_HORIZONTAL_PADDING
            self.rect.bottom = SCREEN_HEIGHT
            
            # Store collision rect (only the main pipe body, not the extensions)
            self.collision_rect = pygame.Rect(x, SCREEN_HEIGHT - (height + cap_height), 
                                             PIPE_WIDTH, height + cap_height)
        
        self.passed = False
    
    def update(self):
        """Move pipe to the left"""
        self.rect.x -= PIPE_SPEED
        
        # Update collision rect position to match pipe movement
        if hasattr(self, 'collision_rect'):
            self.collision_rect.x -= PIPE_SPEED
        
        # Remove pipe if off screen
        if self.rect.right < 0:
            self.kill()


class PipePair:
    """Pair of top and bottom pipes with a gap"""
    
    def __init__(self, x):
        self.x = x
        # Random gap position
        gap_y = random.randint(PIPE_MIN_HEIGHT, PIPE_MAX_HEIGHT)
        self.gap_y = gap_y
        self.gap_center = gap_y + PIPE_GAP // 2
        
        # Create top and bottom pipes
        self.top_pipe = Pipe(x, gap_y, is_top=True)
        self.bottom_pipe = Pipe(x, gap_y, is_top=False)
        
        self.passed = False
    
    def get_sprites(self):
        """Get both pipe sprites"""
        return [self.top_pipe, self.bottom_pipe]
    
    def update(self):
        """Update both pipes"""
        self.x -= PIPE_SPEED
        self.top_pipe.update()
        self.bottom_pipe.update()
    
    def check_passed(self, bird_x):
        """Check if bird has passed this pipe pair"""
        if not self.passed and self.x + PIPE_WIDTH < bird_x:
            self.passed = True
            return True
        return False
    
    def get_gap_center(self):
        """Get the y-coordinate of the gap center"""
        return self.gap_center
    
    def is_off_screen(self):
        """Check if pipe pair is completely off screen"""
        return self.x + PIPE_WIDTH < 0
    
    def get_collision_rects(self):
        """Get collision rectangles for both pipes"""
        return [self.top_pipe.rect, self.bottom_pipe.rect]

