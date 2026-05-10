"""
Simple logging system untuk battle simulation
"""

class BattleLogger:
    """Logger untuk mencatat battle events"""
    
    def __init__(self):
        self.logs = []
        self.max_logs = 100
    
    def log(self, message, log_type="INFO"):
        """Add log entry"""
        log_entry = f"[{log_type}] {message}"
        self.logs.append(log_entry)
        
        # Print immediately untuk debugging
        print(log_entry)
        
        # Keep log size manageable
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)
    
    def log_turn(self, turn_number, player, monster):
        """Log turn information"""
        self.log(f"\n{'='*60}")
        self.log(f"TURN {turn_number}", "TURN")
        self.log(f"Player   HP: {player.hp:3d}/{player.max_hp:3d} | SP: {player.sp:2d}/{player.max_sp:2d}", "STATE")
        self.log(f"Monster  HP: {monster.hp:3d}/{monster.max_hp:3d} | SP: {monster.sp:2d}/{monster.max_sp:2d}", "STATE")
    
    def log_action(self, actor_name, action, target_name, damage=0):
        """Log action"""
        if target_name:
            self.log(f"{actor_name} uses {action} on {target_name}! Damage: {damage}", "ACTION")
        else:
            self.log(f"{actor_name} uses {action}!", "ACTION")
    
    def log_damage(self, target_name, damage, hp_remaining):
        """Log damage received"""
        self.log(f"→ {target_name} takes {damage} damage! HP: {hp_remaining}", "DAMAGE")
    
    def log_victory(self, winner_name):
        """Log battle end"""
        self.log(f"\n{'='*60}")
        self.log(f"VICTORY! {winner_name} wins!", "VICTORY")
        self.log(f"{'='*60}\n")
    
    def log_defeat(self, loser_name):
        """Log battle end"""
        self.log(f"\n{'='*60}")
        self.log(f"DEFEAT! {loser_name} is knocked out!", "DEFEAT")
        self.log(f"{'='*60}\n")
    
    def print_battle_status(self, player, monster, turn_number):
        """Print current battle status"""
        width = 60
        print("\n" + "="*width)
        print(f"TURN {turn_number}".center(width))
        print("="*width)
        
        player_hp_pct = int((player.hp / player.max_hp) * 100) if player.max_hp > 0 else 0
        monster_hp_pct = int((monster.hp / monster.max_hp) * 100) if monster.max_hp > 0 else 0
        
        # HP Bar visualization
        bar_length = 30
        player_bar = "█" * int((player_hp_pct / 100) * bar_length) + "░" * (bar_length - int((player_hp_pct / 100) * bar_length))
        monster_bar = "█" * int((monster_hp_pct / 100) * bar_length) + "░" * (bar_length - int((monster_hp_pct / 100) * bar_length))
        
        print(f"\n{player.name:12} │ HP: [{player_bar}] {player.hp:3d}/{player.max_hp:3d} ({player_hp_pct:3d}%)")
        print(f"{'':12} │ SP: {player.sp:2d}/{player.max_sp:2d}")
        
        print(f"\n{monster.name:12} │ HP: [{monster_bar}] {monster.hp:3d}/{monster.max_hp:3d} ({monster_hp_pct:3d}%)")
        print(f"{'':12} │ SP: {monster.sp:2d}/{monster.max_sp:2d}")
        
        print("\n" + "="*width)


# Global logger instance
battle_logger = BattleLogger()


def get_logger():
    """Get global logger instance"""
    return battle_logger
