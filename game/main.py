"""
Main game loop and entry point
"""

import pygame
import sys
from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PIPE_SPAWN_DISTANCE
)
from .bird import Bird
from .pipes import PipePair
from .coins import CoinManager
from .game_state import MenuState, PlayingState, GameOverState


class Game:
    """Main game class"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird - Collect Coins!")
        self.clock = pygame.time.Clock()
        
        # Game objects
        self.bird = Bird()
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
        
        # Spawn coin in the gap
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
                    self.bird, self.pipes, self.coin_manager
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

