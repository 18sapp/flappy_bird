"""
Main game loop and entry point
"""

import pygame
import sys
import os
import random
from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PIPE_SPAWN_DISTANCE, BIRD_IMAGE_PATH, COIN_SPAWN_PROBABILITY
)
from .bird import Bird
from .pipes import PipePair
from .coins import CoinManager
from .game_state import MenuState, PlayingState, GameOverState


class Game:
    """Main game class"""
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # Initialize audio mixer
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird - Collect Coins!")
        self.clock = pygame.time.Clock()
        
        # Get bird image path (check if file exists)
        bird_image = BIRD_IMAGE_PATH if os.path.exists(BIRD_IMAGE_PATH) else None
        
        # Load sound effects
        from .constants import COIN_SOUND_PATH, COLLISION_SOUND_PATH
        self.coin_sound = None
        if os.path.exists(COIN_SOUND_PATH):
            try:
                self.coin_sound = pygame.mixer.Sound(COIN_SOUND_PATH)
            except pygame.error:
                print(f"Warning: Could not load sound {COIN_SOUND_PATH}")
        
        # Load collision sound
        self.collision_sound = None
        if os.path.exists(COLLISION_SOUND_PATH):
            try:
                self.collision_sound = pygame.mixer.Sound(COLLISION_SOUND_PATH)
            except pygame.error:
                print(f"Warning: Could not load sound {COLLISION_SOUND_PATH}")
        
        # Load and start background music
        from .constants import BACKGROUND_MUSIC_PATH
        if os.path.exists(BACKGROUND_MUSIC_PATH):
            try:
                pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
                pygame.mixer.music.play(-1)  # -1 means loop infinitely
            except pygame.error:
                print(f"Warning: Could not load background music {BACKGROUND_MUSIC_PATH}")
        
        # Game objects
        self.bird = Bird(image_path=bird_image)
        self.pipes = []
        self.coin_manager = CoinManager()
        
        # Game state
        self.current_state = MenuState()
        self.running = True
        
        # Pipe spawning
        self.last_pipe_x = SCREEN_WIDTH
        self.pipe_spawn_timer = 0
    
    def reset_game(self):
        """Reset game to initial state"""
        self.bird.reset()
        self.pipes = []
        self.coin_manager.reset()
        self.last_pipe_x = SCREEN_WIDTH
        self.pipe_spawn_timer = 0
    
    def spawn_pipe_pair(self):
        """Spawn a new pipe pair"""
        pipe_pair = PipePair(self.last_pipe_x + PIPE_SPAWN_DISTANCE)
        self.pipes.append(pipe_pair)
        self.last_pipe_x = pipe_pair.x
        
        # Randomly spawn coin in the gap (based on probability)
        if random.random() < COIN_SPAWN_PROBABILITY:
            gap_center_y = pipe_pair.get_gap_center()
            coin_x = pipe_pair.x + 40  # Center of pipe width
            coin_y = gap_center_y
            self.coin_manager.spawn_coin(coin_x, coin_y)
    
    def update_pipes(self):
        """Update all pipes and remove off-screen ones"""
        for pipe_pair in self.pipes[:]:
            pipe_pair.update()
            if pipe_pair.is_off_screen():
                self.pipes.remove(pipe_pair)
    
    def handle_state_transition(self):
        """Handle state transitions"""
        next_state = self.current_state.get_next_state()
        if next_state:
            self.current_state.reset_next_state()
            
            if next_state == 'playing':
                self.reset_game()
                self.current_state = PlayingState(
                    self.bird, self.pipes, self.coin_manager, self.coin_sound, self.collision_sound
                )
            elif next_state == 'game_over':
                playing_state = self.current_state
                final_score = playing_state.get_score()
                coins_collected = self.coin_manager.get_collected_count()
                self.current_state = GameOverState(final_score, coins_collected)
            elif next_state == 'menu':
                self.reset_game()
                self.current_state = MenuState()
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                self.current_state.handle_event(event)
            
            # Handle state transitions
            self.handle_state_transition()
            
            # Update game objects based on state
            if isinstance(self.current_state, PlayingState):
                # Spawn pipes
                self.pipe_spawn_timer += 1
                if self.pipe_spawn_timer >= PIPE_SPAWN_DISTANCE // 3:  # Adjust spawn rate
                    self.spawn_pipe_pair()
                    self.pipe_spawn_timer = 0
                
                # Update game objects
                self.bird.update()
                self.update_pipes()
                self.coin_manager.update()
                self.coin_manager.remove_off_screen(SCREEN_WIDTH)
                
                # Update score when passing pipes
                for pipe_pair in self.pipes:
                    if pipe_pair.check_passed(self.bird.rect.x):
                        if isinstance(self.current_state, PlayingState):
                            self.current_state.score += 1
            
            # Update state
            self.current_state.update()
            
            # Draw everything
            self.current_state.draw(self.screen)
            
            # Draw game objects in playing state
            if isinstance(self.current_state, PlayingState):
                # Objects are drawn by PlayingState, but we ensure they're updated
                pass
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()

