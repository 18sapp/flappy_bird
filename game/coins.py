"""
Coin collection system
"""

import pygame
from .constants import COIN_SIZE, GOLD, YELLOW, COIN_ROTATION_SPEED, PIPE_SPEED


class Coin(pygame.sprite.Sprite):
    """Collectible coin sprite"""
    
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((COIN_SIZE, COIN_SIZE), pygame.SRCALPHA)
        self.base_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Draw coin
        pygame.draw.circle(self.base_image, GOLD, (COIN_SIZE // 2, COIN_SIZE // 2), COIN_SIZE // 2)
        pygame.draw.circle(self.base_image, YELLOW, (COIN_SIZE // 2, COIN_SIZE // 2), COIN_SIZE // 2 - 3)
        pygame.draw.circle(self.base_image, GOLD, (COIN_SIZE // 2, COIN_SIZE // 2), COIN_SIZE // 4)
        
        self.rotation_angle = 0
        self.collected = False
    
    def update(self):
        """Update coin animation and position"""
        if not self.collected:
            # Move coin left with pipes
            self.rect.x -= PIPE_SPEED
            
            # Rotate coin
            self.rotation_angle += COIN_ROTATION_SPEED
            if self.rotation_angle >= 360:
                self.rotation_angle = 0
            
            # Create rotated image
            self.image = pygame.transform.rotate(self.base_image, self.rotation_angle)
            # Update rect center to maintain position after rotation
            old_center = self.rect.center
            self.rect = self.image.get_rect(center=old_center)
    
    def collect(self):
        """Mark coin as collected"""
        self.collected = True
        self.kill()
    
    def is_collected(self):
        """Check if coin is collected"""
        return self.collected


class CoinManager:
    """Manages coin spawning and collection"""
    
    def __init__(self):
        self.coins = pygame.sprite.Group()
        self.collected_count = 0
    
    def spawn_coin(self, x, y):
        """Spawn a coin at the specified position"""
        coin = Coin(x, y)
        self.coins.add(coin)
        return coin
    
    def update(self):
        """Update all coins"""
        self.coins.update()
    
    def check_collision(self, bird_rect):
        """Check if bird collides with any coin"""
        # Check collision with bird rect
        for coin in list(self.coins):  # Use list to avoid modification during iteration
            if bird_rect.colliderect(coin.rect):
                coin.collect()
                self.collected_count += 1
                return True
        return False
    
    def remove_off_screen(self, screen_width):
        """Remove coins that are off screen"""
        for coin in self.coins:
            if coin.rect.right < 0:
                coin.kill()
    
    def get_collected_count(self):
        """Get number of collected coins"""
        return self.collected_count
    
    def reset(self):
        """Reset coin manager"""
        self.coins.empty()
        self.collected_count = 0
    
    def draw(self, screen):
        """Draw all coins"""
        self.coins.draw(screen)

