"""
Pipe obstacle system
"""

import pygame
import random
from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PIPE_WIDTH, PIPE_GAP,
    PIPE_SPEED, PIPE_SPAWN_DISTANCE, PIPE_MIN_HEIGHT, PIPE_MAX_HEIGHT,
    GREEN, DARK_GREEN
)


class Pipe(pygame.sprite.Sprite):
    """Single pipe obstacle"""
    
    def __init__(self, x, gap_y, is_top=False):
        super().__init__()
        self.is_top = is_top
        
        if is_top:
            # Top pipe (hangs from top)
            height = gap_y
            self.image = pygame.Surface((PIPE_WIDTH, height))
            self.image.fill(GREEN)
            pygame.draw.rect(self.image, DARK_GREEN, (0, 0, PIPE_WIDTH, height), 3)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = 0
        else:
            # Bottom pipe (rises from bottom)
            height = SCREEN_HEIGHT - (gap_y + PIPE_GAP)
            self.image = pygame.Surface((PIPE_WIDTH, height))
            self.image.fill(GREEN)
            pygame.draw.rect(self.image, DARK_GREEN, (0, 0, PIPE_WIDTH, height), 3)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.bottom = SCREEN_HEIGHT
        
        self.passed = False
    
    def update(self):
        """Move pipe to the left"""
        self.rect.x -= PIPE_SPEED
        
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

