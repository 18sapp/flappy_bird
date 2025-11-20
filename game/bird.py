"""
Bird class with physics and lives system
"""

import pygame
import os
from .constants import (
    BIRD_WIDTH, BIRD_HEIGHT, BIRD_START_X, BIRD_START_Y,
    GRAVITY, JUMP_STRENGTH, BIRD_MAX_VELOCITY, INITIAL_LIVES
)


class Bird(pygame.sprite.Sprite):
    """Bird sprite with physics and lives management"""
    
    def __init__(self, x=BIRD_START_X, y=BIRD_START_Y, image_path=None):
        super().__init__()
        
        # Try to load image from file, otherwise use default drawing
        if image_path and os.path.exists(image_path):
            try:
                # Load and scale the image
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (BIRD_WIDTH, BIRD_HEIGHT))
            except pygame.error:
                # If image loading fails, use default drawing
                self.image = self._create_default_bird()
        else:
            # Use default drawing if no image path provided or file doesn't exist
            self.image = self._create_default_bird()
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Initialize bird properties
        self.velocity = 0
        self.lives = INITIAL_LIVES
        self.alive = True
        self.invincible = False
        self.invincible_timer = 0
        self.INVINCIBLE_DURATION = 120  # Frames of invincibility (2 seconds at 60 FPS)
    
    def _create_default_bird(self):
        """Create default bird using drawing functions"""
        surface = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT), pygame.SRCALPHA)
        surface.fill((255, 200, 0))  # Yellow bird
        # Draw a simple bird shape
        pygame.draw.ellipse(surface, (255, 200, 0), (0, 0, BIRD_WIDTH, BIRD_HEIGHT))
        pygame.draw.circle(surface, (255, 0, 0), (BIRD_WIDTH - 10, BIRD_HEIGHT // 2), 5)  # Eye
        pygame.draw.polygon(surface, (255, 100, 0), [
            (BIRD_WIDTH, BIRD_HEIGHT // 2),
            (BIRD_WIDTH + 10, BIRD_HEIGHT // 2 - 5),
            (BIRD_WIDTH + 10, BIRD_HEIGHT // 2 + 5)
        ])  # Beak
        return surface
        
    def jump(self):
        """Make the bird jump"""
        if self.alive:
            self.velocity = JUMP_STRENGTH
    
    def update(self):
        """Update bird position based on physics"""
        # Update invincibility timer
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
        
        if self.alive:
            # Apply gravity
            self.velocity += GRAVITY
            # Limit max velocity
            if self.velocity > BIRD_MAX_VELOCITY:
                self.velocity = BIRD_MAX_VELOCITY
            
            # Update position
            self.rect.y += self.velocity
            
            # Keep bird on screen
            if self.rect.top < 0:
                self.rect.top = 0
                self.velocity = 0
            if self.rect.bottom > 600:  # Screen height
                self.rect.bottom = 600
                self.velocity = 0
    
    def lose_life(self):
        """Lose a life and reset position"""
        if self.lives > 0 and not self.invincible:
            self.lives -= 1
            if self.lives <= 0:
                self.alive = False
            else:
                # Reset position when losing a life
                self.rect.x = BIRD_START_X
                self.rect.y = BIRD_START_Y
                self.velocity = 0
                # Start invincibility period
                self.invincible = True
                self.invincible_timer = self.INVINCIBLE_DURATION
    
    def reset(self):
        """Reset bird to initial state"""
        self.rect.x = BIRD_START_X
        self.rect.y = BIRD_START_Y
        self.velocity = 0
        self.lives = INITIAL_LIVES
        self.alive = True
        self.invincible = False
        self.invincible_timer = 0
    
    def get_lives(self):
        """Get current number of lives"""
        return self.lives

