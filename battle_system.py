import random
from enum import Enum
from pyglm import glm
from battle_logger import get_logger


class ActionType(Enum):
    """Tipe action yang bisa dilakukan karakter"""
    NORMAL_ATTACK = "normal_attack"
    MAGIC_ATTACK = "magic_attack"
    DEFEND = "defend"
    SKILL = "skill"


class BattleSystem:
    """Sistem turn-based battle"""
    
    def __init__(self, app, player, monster):
        self.app = app
        self.player = player
        self.monster = monster
        self.logger = get_logger()
        
        self.turn_counter = 0
        self.current_turn = None  # 'player' atau 'monster'
        self.battle_log = []
        self.is_battle_active = True
        
        # Determine turn order
        self._calculate_turn_order()
        
        # Log initialization
        self.logger.log(f"Battle Started! {player.name} vs {monster.name}", "INIT")
    
    def _calculate_turn_order(self):
        """Hitung siapa yang jalan duluan berdasarkan speed"""
        if self.player.speed >= self.monster.speed:
            self.current_turn = 'player'
        else:
            self.current_turn = 'monster'
    
    def execute_player_action(self, action_type=ActionType.NORMAL_ATTACK):
        """Execute player action"""
        if self.current_turn != 'player' or not self.is_battle_active:
            self.logger.log(f"Cannot execute action: not player turn or battle inactive", "WARNING")
            return
        
        self.logger.print_battle_status(self.player, self.monster, self.turn_counter)
        
        self._execute_action(self.player, self.monster, action_type)
        self._log_action(self.player, action_type, self.monster)
        
        # Switch turn
        self._switch_turn()
    
    def _execute_action(self, attacker, target, action_type):
        """Execute actual action"""
        damage = 0
        action_name = ""
        
        if action_type == ActionType.NORMAL_ATTACK:
            damage = self._calculate_damage(attacker, target, is_magic=False)
            attacker.perform_action("slash", target, damage)
            action_name = "Normal Attack"
            
        elif action_type == ActionType.MAGIC_ATTACK:
            if attacker.consume_sp(20):
                damage = self._calculate_damage(attacker, target, is_magic=True)
                attacker.perform_action("magic", target, damage)
                action_name = "Magic Attack"
            else:
                self.logger.log(f"{attacker.name} doesn't have enough SP!", "WARNING")
                return
        
        elif action_type == ActionType.DEFEND:
            attacker.perform_action("defend", None, 0)
            action_name = "Defend"
            self.logger.log(f"{attacker.name} takes a defensive stance!", "ACTION")
            return
        
        elif action_type == ActionType.SKILL:
            if attacker.consume_sp(30):
                damage = self._calculate_damage(attacker, target, is_magic=True) * 1.5
                damage = int(damage)
                attacker.perform_action("skill", target, damage)
                action_name = "Skill Attack"
            else:
                self.logger.log(f"{attacker.name} doesn't have enough SP!", "WARNING")
                return
        
        # Log action
        self.logger.log_action(attacker.name, action_name, target.name, int(damage))
        self.logger.log_damage(target.name, int(damage), target.hp)
        
        # Check if target still alive
        if not target.is_alive:
            self.battle_log.append(f"{target.name} is defeated!")
            self.is_battle_active = False
            
            if target.is_player:
                self.logger.log_defeat(target.name)
            else:
                self.logger.log_victory(attacker.name)
    
    def _calculate_damage(self, attacker, target, is_magic=False):
        """Calculate damage"""
        base_damage = attacker.attack if not is_magic else attacker.attack * 1.2
        variance = random.randint(-5, 5)
        defense_reduction = target.defense if is_magic else target.defense * 0.5
        
        total_damage = max(5, int(base_damage + variance - defense_reduction * 0.3))
        return total_damage
    
    def _switch_turn(self):
        """Switch turn ke player atau monster"""
        if self.current_turn == 'player':
            self.current_turn = 'monster'
        else:
            self.current_turn = 'player'
        
        self.turn_counter += 1
    
    def update_ai(self, delta_time):
        """Update AI monster"""
        if self.current_turn == 'monster' and self.is_battle_active:
            self.logger.print_battle_status(self.player, self.monster, self.turn_counter)
            
            # AI decision
            ai_action = self._get_ai_action()
            self._execute_action(self.monster, self.player, ai_action)
            self._log_action(self.monster, ai_action, self.player)
            
            # Switch turn
            self._switch_turn()
    
    def _get_ai_action(self):
        """Get AI action berdasarkan kondisi"""
        monster = self.monster
        
        # Recover SP setiap turn
        monster.recover_sp(8)
        
        # Priority system (Persona-inspired)
        if monster.hp < monster.max_hp * 0.3 and monster.sp >= 30:
            # Low HP -> use skill untuk burst damage
            return ActionType.SKILL
        
        elif monster.sp >= 20 and random.random() < 0.4:
            # Punya SP -> gunakan magic attack
            return ActionType.MAGIC_ATTACK
        
        else:
            # Default -> normal attack
            return ActionType.NORMAL_ATTACK
    
    def _log_action(self, actor, action_type, target):
        """Log action untuk debugging"""
        action_name = action_type.value if hasattr(action_type, 'value') else str(action_type)
        log = f"Turn {self.turn_counter}: {actor.name} gunakan {action_name}"
        if target:
            log += f" pada {target.name}. HP: {target.hp}/{target.max_hp}"
        self.battle_log.append(log)
    
    def update(self, delta_time):
        """Update battle system"""
        if not self.is_battle_active:
            return
        
        self.player.update(delta_time)
        self.monster.update(delta_time)
        
        # Recover SP setiap turn
        self.player.recover_sp(5)
        self.monster.recover_sp(8)
    
    def get_battle_status(self):
        """Get battle status untuk UI"""
        return {
            'player_hp': self.player.hp,
            'player_max_hp': self.player.max_hp,
            'player_sp': self.player.sp,
            'player_max_sp': self.player.max_sp,
            'monster_hp': self.monster.hp,
            'monster_max_hp': self.monster.max_hp,
            'monster_sp': self.monster.sp,
            'monster_max_sp': self.monster.max_sp,
            'current_turn': self.current_turn,
            'is_active': self.is_battle_active,
        }
