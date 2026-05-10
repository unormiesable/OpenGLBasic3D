"""
Advanced Battle System with Party vs Monster
Support untuk analisis 4 kondisi party
"""

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
    HEAL = "heal"
    MULTI_ATTACK = "multi_attack"


class AdvancedBattleSystem:
    """Advanced battle system untuk Party vs Monster
    
    Menganalisis 4 kondisi party:
    A: HP Penuh (80%+) & SP Penuh (80%+) - Kondisi Optimal
    B: HP Kritis (<50%) & SP Penuh (80%+) - Urgent Heal Needed
    C: HP Penuh (80%+) & SP Kritis (<50%) - Recover SP
    D: HP Kritis (<50%) & SP Kritis (<50%) - Critical Survival
    """
    
    def __init__(self, app, party, monster):
        self.app = app
        self.party = party
        self.monster = monster
        self.logger = get_logger()
        
        self.turn_counter = 0
        self.current_actor_index = None  # Index of current party member
        self.current_turn = None  # 'party' atau 'monster'
        self.battle_log = []
        self.is_battle_active = True
        self.party_condition = 'N'  # A, B, C, D, N
        
        self._calculate_turn_order()
        self.logger.log(f"Advanced Battle Started!", "INIT")
        self.logger.log(f"Party vs Monster!", "INIT")
    
    def _calculate_turn_order(self):
        """Calculate turn order berdasarkan party vs monster"""
        # Simple: Party selalu duluan
        self.current_turn = 'party'
        self.current_actor_index = 0
    
    def analyze_party_condition(self):
        """Analyze kondisi party (A, B, C, atau D)"""
        self.party_condition = self.party.analyze_party_condition()
        return self.party_condition
    
    def execute_party_action(self, member_index, action_type=ActionType.NORMAL_ATTACK, 
                           target_member=None):
        """Execute party member action"""
        if self.current_turn != 'party' or not self.is_battle_active:
            self.logger.log(f"Cannot execute action: not party turn or battle inactive", "WARNING")
            return False
        
        if member_index >= len(self.party.members):
            return False
        
        actor = self.party.members[member_index]
        
        if not actor.is_alive:
            self.logger.log(f"{actor.name} is dead and cannot act!", "WARNING")
            return False
        
        # Different logic based on action type
        if action_type in [ActionType.NORMAL_ATTACK, ActionType.MAGIC_ATTACK, 
                          ActionType.SKILL, ActionType.MULTI_ATTACK]:
            # Attack the monster
            self._execute_action(actor, self.monster, action_type)
        elif action_type == ActionType.HEAL:
            # Heal a party member
            self._execute_heal(actor, target_member)
        elif action_type == ActionType.DEFEND:
            actor.perform_action("defend", None, 0)
            self.logger.log_action(actor.name, "Defend", None, 0)
        
        # Move to next party member or monster turn
        self.current_actor_index += 1
        
        # Check if all party members acted
        if self.current_actor_index >= len(self.party.members):
            # Switch to monster turn
            self.current_turn = 'monster'
            self.current_actor_index = None
        
        return True
    
    def _execute_action(self, actor, target, action_type):
        """Execute attack action"""
        damage = 0
        action_name = ""
        
        if action_type == ActionType.NORMAL_ATTACK:
            damage = self._calculate_damage(actor, target, is_magic=False)
            actor.perform_action("slash", target, damage)
            action_name = "Normal Attack"
            
        elif action_type == ActionType.MAGIC_ATTACK:
            if actor.consume_sp(20):
                damage = self._calculate_damage(actor, target, is_magic=True)
                actor.perform_action("magic", target, damage)
                action_name = "Magic Attack"
            else:
                self.logger.log(f"{actor.name} doesn't have enough SP!", "WARNING")
                return
        
        elif action_type == ActionType.SKILL:
            if actor.consume_sp(30):
                damage = self._calculate_damage(actor, target, is_magic=True) * 1.5
                damage = int(damage)
                actor.perform_action("skill", target, damage)
                action_name = "Skill Attack"
            else:
                self.logger.log(f"{actor.name} doesn't have enough SP!", "WARNING")
                return
        
        elif action_type == ActionType.MULTI_ATTACK:
            # Attack all with reduced damage
            if actor.consume_sp(40):
                base_damage = self._calculate_damage(actor, target, is_magic=True) * 0.8
                damage = int(base_damage)
                actor.perform_action("multi", target, damage)
                action_name = "Multi-Hit Attack"
            else:
                self.logger.log(f"{actor.name} doesn't have enough SP!", "WARNING")
                return
        
        # Log action
        self.logger.log_action(actor.name, action_name, target.name, int(damage))
        self.logger.log_damage(target.name, int(damage), target.hp)
        
        # Check if monster still alive
        if not target.is_alive:
            self.is_battle_active = False
            self.logger.log_victory(self.party.members[0].name)
    
    def _execute_heal(self, actor, target_member):
        """Execute heal action"""
        if actor.consume_sp(25):
            if target_member is None:
                target_member = actor
            
            heal_amount = self._calculate_heal(actor)
            actual_heal = target_member.recover_hp(heal_amount)
            
            action_name = f"Heal (+{actual_heal})"
            self.logger.log_action(actor.name, action_name, target_member.name, actual_heal)
        else:
            self.logger.log(f"{actor.name} doesn't have enough SP for heal!", "WARNING")
    
    def _calculate_damage(self, attacker, target, is_magic=False):
        """Calculate damage"""
        base_damage = attacker.attack if not is_magic else attacker.attack * 1.2
        variance = random.randint(-5, 5)
        defense_reduction = target.defense if is_magic else target.defense * 0.5
        
        total_damage = max(5, int(base_damage + variance - defense_reduction * 0.3))
        return total_damage
    
    def _calculate_heal(self, healer):
        """Calculate heal amount"""
        base_heal = healer.attack + random.randint(5, 15)
        return int(base_heal)
    
    def update_ai(self, delta_time):
        """Update AI monster turn"""
        if self.current_turn == 'monster' and self.is_battle_active:
            # Analyze party condition
            self.analyze_party_condition()
            
            # Get AI action based on party condition
            ai_action = self._get_ai_action_from_condition()
            
            self._execute_action(self.monster, self._select_target(), ai_action)
            
            # Back to party turn
            self.current_turn = 'party'
            self.current_actor_index = 0
            self.turn_counter += 1
    
    def _get_ai_action_from_condition(self):
        """Get AI action based on party condition analysis"""
        party_condition = self.party_condition
        monster = self.monster
        
        # Recover SP every turn
        monster.recover_sp(10)
        
        self.logger.log(f"[AI ANALYSIS] Party Condition: {party_condition}", "ACTION")
        
        if party_condition == 'A':
            # Kondisi A: HP Penuh & SP Penuh - Party Strong
            # Monster harus aggressive
            if monster.sp >= 40:
                self.logger.log(f"[AI] Kondisi A: Enemy Strong → Multi-Attack", "ACTION")
                return ActionType.MULTI_ATTACK
            elif monster.sp >= 30:
                self.logger.log(f"[AI] Kondisi A: Enemy Strong → Skill", "ACTION")
                return ActionType.SKILL
            else:
                self.logger.log(f"[AI] Kondisi A: Enemy Strong → Magic", "ACTION")
                return ActionType.MAGIC_ATTACK if monster.sp >= 20 else ActionType.NORMAL_ATTACK
        
        elif party_condition == 'B':
            # Kondisi B: HP Kritis & SP Penuh - Party Weak but High SP
            # Monster fokus destroy, HP low = easy target
            if monster.sp >= 30:
                self.logger.log(f"[AI] Kondisi B: Enemy HP Critical → SKILL BURST", "ACTION")
                return ActionType.SKILL
            else:
                self.logger.log(f"[AI] Kondisi B: Enemy HP Critical → Magic", "ACTION")
                return ActionType.MAGIC_ATTACK if monster.sp >= 20 else ActionType.NORMAL_ATTACK
        
        elif party_condition == 'C':
            # Kondisi C: HP Penuh & SP Kritis - Party Low SP
            # Monster harus manage resources tapi tetap aggressive
            if monster.sp >= 30:
                self.logger.log(f"[AI] Kondisi C: Enemy SP Low → Strategic Skill", "ACTION")
                return ActionType.SKILL
            elif monster.sp >= 20:
                self.logger.log(f"[AI] Kondisi C: Enemy SP Low → Magic", "ACTION")
                return ActionType.MAGIC_ATTACK
            else:
                self.logger.log(f"[AI] Kondisi C: Enemy SP Low → Normal", "ACTION")
                return ActionType.NORMAL_ATTACK
        
        elif party_condition == 'D':
            # Kondisi D: HP Kritis & SP Kritis - Party Critical
            # Monster full aggressive, party in critical condition
            if monster.sp >= 40:
                self.logger.log(f"[AI] Kondisi D: Enemy CRITICAL → MULTI-ATTACK FINISH", "ACTION")
                return ActionType.MULTI_ATTACK
            elif monster.sp >= 30:
                self.logger.log(f"[AI] Kondisi D: Enemy CRITICAL → SKILL FINISH", "ACTION")
                return ActionType.SKILL
            elif monster.sp >= 20:
                self.logger.log(f"[AI] Kondisi D: Enemy CRITICAL → Magic", "ACTION")
                return ActionType.MAGIC_ATTACK
            else:
                self.logger.log(f"[AI] Kondisi D: Enemy CRITICAL → Normal", "ACTION")
                return ActionType.NORMAL_ATTACK
        
        else:  # Kondisi N - Normal/Balanced
            if monster.hp < monster.max_hp * 0.3 and monster.sp >= 30:
                return ActionType.SKILL
            elif monster.sp >= 20 and random.random() < 0.4:
                return ActionType.MAGIC_ATTACK
            else:
                return ActionType.NORMAL_ATTACK
    
    def _select_target(self):
        """Select target dari party"""
        # Untuk sekarang, select random alive member
        alive = self.party.get_alive_members()
        if alive:
            return random.choice(alive)
        return self.party.members[0]
    
    def get_battle_status(self):
        """Get battle status untuk UI"""
        return {
            'party': self.party.get_party_status(),
            'monster_hp': self.monster.hp,
            'monster_max_hp': self.monster.max_hp,
            'monster_sp': self.monster.sp,
            'monster_max_sp': self.monster.max_sp,
            'current_turn': self.current_turn,
            'current_actor': self.current_actor_index,
            'is_active': self.is_battle_active,
            'party_condition': self.party_condition,
            'turn': self.turn_counter,
        }
    
    def update(self, delta_time):
        """Update battle"""
        if not self.is_battle_active:
            return
        
        self.party.update(delta_time)
        self.monster.update(delta_time)
        
        # Recover SP
        for member in self.party.members:
            if member.is_alive:
                member.recover_sp(3)
