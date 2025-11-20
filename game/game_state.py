"""
Game state management
"""

import pygame
from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED,
    FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL
)


class GameState:
    """Base game state class"""
    
    def __init__(self):
        self.next_state = None
    
    def handle_event(self, event):
        """Handle input events"""
        pass
    
    def update(self):
        """Update state logic"""
        pass
    
    def draw(self, screen):
        """Draw state"""
        pass
    
    def get_next_state(self):
        """Get next state to transition to"""
        return self.next_state
    
    def reset_next_state(self):
        """Reset next state"""
        self.next_state = None


class MenuState(GameState):
    """Start menu state"""
    
    def __init__(self):
        super().__init__()
        self.font_large = None
        self.font_medium = None
    
    def init_fonts(self):
        """Initialize fonts"""
        try:
            self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
            self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        except:
            # Fallback if fonts fail
            self.font_large = pygame.font.SysFont('arial', FONT_SIZE_LARGE)
            self.font_medium = pygame.font.SysFont('arial', FONT_SIZE_MEDIUM)
    
    def handle_event(self, event):
        """Handle menu input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                self.next_state = 'playing'
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.next_state = 'playing'
    
    def draw(self, screen):
        """Draw menu"""
        if not self.font_large:
            self.init_fonts()
        
        screen.fill((135, 206, 235))  # Sky blue background
        
        # Title
        title_text = self.font_large.render("FLAPPY BIRD", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(title_text, title_rect)
        
        # Instructions
        instruction_text = self.font_medium.render("Press SPACE or CLICK to Start", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(instruction_text, instruction_rect)
        
        # Game info
        info_text = self.font_medium.render("Collect coins! You have 3 lives!", True, WHITE)
        info_rect = info_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(info_text, info_rect)


class PlayingState(GameState):
    """Game playing state"""
    
    def __init__(self, bird, pipes, coin_manager, coin_sound=None, collision_sound=None):
        super().__init__()
        self.bird = bird
        self.pipes = pipes
        self.coin_manager = coin_manager
        self.coin_sound = coin_sound  # Store sound reference
        self.collision_sound = collision_sound  # Store collision sound reference
        self.score = 0
        self.font_medium = None
        self.font_small = None
        self.hit_pipe_pairs = set()  # Track which pipe pairs have been hit
    
    def init_fonts(self):
        """Initialize fonts"""
        try:
            self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
            self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        except:
            self.font_medium = pygame.font.SysFont('arial', FONT_SIZE_MEDIUM)
            self.font_small = pygame.font.SysFont('arial', FONT_SIZE_SMALL)
    
    def handle_event(self, event):
        """Handle game input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.bird.jump()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.bird.jump()
    
    def update(self):
        """Update game logic"""
        # Only check collisions if bird is alive and not invincible
        if not self.bird.alive or self.bird.invincible:
            return
        
        # Check collisions with pipes
        for pipe_pair in self.pipes:
            # Skip if this pipe pair already caused damage
            if id(pipe_pair) in self.hit_pipe_pairs:
                continue
                
            for pipe in pipe_pair.get_sprites():
                if self.bird.rect.colliderect(pipe.rect):
                    # Play collision sound if available
                    if self.collision_sound:
                        self.collision_sound.play()
                    self.bird.lose_life()
                    # Mark this pipe pair as hit
                    self.hit_pipe_pairs.add(id(pipe_pair))
                    # Clear hit pipe pairs when bird loses a life (so it can be hit by new pipes after invincibility)
                    if self.bird.invincible:
                        self.hit_pipe_pairs.clear()
                    if not self.bird.alive:
                        self.next_state = 'game_over'
                    return  # Exit early to prevent multiple collisions in same frame
        
        # Check coin collection
        if self.coin_manager.check_collision(self.bird.rect):
            self.score += 10  # Coin score
            # Play coin sound if available
            if self.coin_sound:
                self.coin_sound.play()
        
        # Check if bird hit top or bottom
        if self.bird.rect.top <= 0 or self.bird.rect.bottom >= SCREEN_HEIGHT:
            # Play collision sound if available
            if self.collision_sound:
                self.collision_sound.play()
            self.bird.lose_life()
            if not self.bird.alive:
                self.next_state = 'game_over'
    
    def draw(self, screen):
        """Draw game"""
        if not self.font_medium:
            self.init_fonts()
        
        screen.fill((135, 206, 235))  # Sky blue background
        
        # Draw pipes
        for pipe_pair in self.pipes:
            for pipe in pipe_pair.get_sprites():
                screen.blit(pipe.image, pipe.rect)
        
        # Draw coins
        self.coin_manager.draw(screen)
        
        # Draw bird
        screen.blit(self.bird.image, self.bird.rect)
        
        # Draw UI
        # Score
        score_text = self.font_medium.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Coins collected
        coins_text = self.font_small.render(f"Coins: {self.coin_manager.get_collected_count()}", True, WHITE)
        screen.blit(coins_text, (10, 50))
        
        # Lives
        lives_text = self.font_small.render(f"Lives: {self.bird.get_lives()}", True, RED)
        screen.blit(lives_text, (10, 80))
        
        # Draw hearts for lives
        heart_size = 20
        for i in range(self.bird.get_lives()):
            heart_x = SCREEN_WIDTH - 30 - (i * 30)
            pygame.draw.circle(screen, RED, (heart_x, 20), heart_size // 2)
            # Simple heart shape
            pygame.draw.polygon(screen, RED, [
                (heart_x, 20),
                (heart_x - 5, 15),
                (heart_x - 10, 20),
                (heart_x, 30),
                (heart_x + 10, 20),
                (heart_x + 5, 15)
            ])
    
    def get_score(self):
        """Get current score"""
        return self.score


class GameOverState(GameState):
    """Game over state"""
    
    def __init__(self, final_score, coins_collected):
        super().__init__()
        self.final_score = final_score
        self.coins_collected = coins_collected
        self.font_large = None
        self.font_medium = None
    
    def init_fonts(self):
        """Initialize fonts"""
        try:
            self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
            self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        except:
            self.font_large = pygame.font.SysFont('arial', FONT_SIZE_LARGE)
            self.font_medium = pygame.font.SysFont('arial', FONT_SIZE_MEDIUM)
    
    def handle_event(self, event):
        """Handle game over input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                self.next_state = 'menu'
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.next_state = 'menu'
    
    def draw(self, screen):
        """Draw game over screen"""
        if not self.font_large:
            self.init_fonts()
        
        screen.fill((50, 50, 50))  # Dark background
        
        # Game Over text
        game_over_text = self.font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.font_medium.render(f"Final Score: {self.final_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(score_text, score_rect)
        
        # Coins collected
        coins_text = self.font_medium.render(f"Coins Collected: {self.coins_collected}", True, WHITE)
        coins_rect = coins_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(coins_text, coins_rect)
        
        # Restart instruction
        restart_text = self.font_medium.render("Press SPACE or CLICK to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
        screen.blit(restart_text, restart_rect)

