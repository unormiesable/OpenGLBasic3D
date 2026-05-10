"""
Auto-demo battle tanpa input manual untuk testing
"""

import sys
import time
import pygame as pg
import moderngl as mgl
from main import SxvxnEngine
from battle_system import ActionType


class AutoBattleDemo:
    """Automatic battle demo untuk demonstration"""
    
    def __init__(self):
        self.app = SxvxnEngine()
        self.action_sequence = [
            ActionType.NORMAL_ATTACK,
            ActionType.MAGIC_ATTACK,
            ActionType.NORMAL_ATTACK,
            ActionType.SKILL,
        ]
        self.action_index = 0
        self.action_timer = 0.0
        self.action_interval = 3.0  # Action setiap 3 detik
    
    def run_demo(self, max_turns=20):
        """Run demo battle"""
        print("=" * 60)
        print("AUTO BATTLE DEMO - Press any key to stop")
        print("=" * 60)
        
        turn_count = 0
        
        try:
            while turn_count < max_turns and self.app.scene.battle_system.is_battle_active:
                self.app.get_time()
                
                # Handle events (ESC to exit)
                for event in pg.event.get():
                    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                        print("\nDemo stopped by user.")
                        self.app.destroy()
                        pg.quit()
                        return
                
                # Camera update
                self.app.camera.update()
                
                # Auto action logic
                self.action_timer += self.app.delta_time / 1000.0
                if self.action_timer >= self.action_interval:
                    if self.app.scene.battle_system.current_turn == 'player':
                        action = self.action_sequence[self.action_index % len(self.action_sequence)]
                        self.app.scene.battle_system.execute_player_action(action)
                        self.action_index += 1
                    
                    self.action_timer = 0.0
                    turn_count += 1
                
                # Render
                self.app.render()
                
                # Frame timing
                self.app.delta_time = self.app.clock.tick(60)
            
            # Show final status
            print("\n" + "=" * 60)
            print("DEMO FINISHED")
            print("=" * 60)
            
            final_status = self.app.scene.battle_system.get_battle_status()
            if final_status['player_hp'] > 0:
                print("PLAYER VICTORY!")
            else:
                print("MONSTER VICTORY!")
            
            print(f"Final HP - Player: {final_status['player_hp']}, Monster: {final_status['monster_hp']}")
            print("=" * 60)
            
            # Wait before closing
            time.sleep(2)
            self.app.destroy()
            pg.quit()
            
        except Exception as e:
            print(f"Error during demo: {e}")
            import traceback
            traceback.print_exc()
            self.app.destroy()
            pg.quit()


if __name__ == '__main__':
    demo = AutoBattleDemo()
    demo.run_demo(max_turns=50)
