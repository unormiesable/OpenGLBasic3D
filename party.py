"""
Party System - Multiple players management
"""

from pyglm import glm
from character import Character, Player


class PartyMember(Player):
    """Extended Player class untuk party member dengan role"""
    
    def __init__(self, app, name="Ally", pos=(0, 1, 0), role="attacker", color=(0.2, 0.8, 1.0)):
        super().__init__(app, name, pos)
        self.role = role  # "attacker", "defender", "healer", "supporter"
        self.color_base = glm.vec3(color)
        self.color = self.color_base
        self.party_position = 0  # 0, 1, 2 untuk position di party
        
        # Role-specific stat adjustments
        self._apply_role_stats()
    
    def _apply_role_stats(self):
        """Adjust stats based on role"""
        if self.role == "attacker":
            # High ATK, normal DEF
            self.attack = 25
            self.defense = 10
            
        elif self.role == "defender":
            # High DEF & HP, low ATK
            self.max_hp = 180
            self.hp = self.max_hp
            self.attack = 12
            self.defense = 18
            
        elif self.role == "healer":
            # High SP, moderate HP
            self.max_sp = 120
            self.sp = self.max_sp
            self.attack = 15
            self.defense = 12
            self.max_hp = 140
            self.hp = self.max_hp
            
        elif self.role == "supporter":
            # Balanced
            self.max_hp = 160
            self.hp = self.max_hp
            self.attack = 18
            self.defense = 14
    
    def get_status(self):
        """Get simple status string"""
        hp_pct = int((self.hp / self.max_hp) * 100) if self.max_hp > 0 else 0
        sp_pct = int((self.sp / self.max_sp) * 100) if self.max_sp > 0 else 0
        status = "ALIVE" if self.is_alive else "DEAD"
        return f"{self.name:10} | HP:{hp_pct:3d}% SP:{sp_pct:3d}% [{status}]"


class Party:
    """Party of 3 players"""
    
    def __init__(self, app):
        self.app = app
        self.members = []
        self.current_actor = 0  # Index of current member acting
    
    def add_member(self, member):
        """Add member to party"""
        if len(self.members) < 3:
            member.party_position = len(self.members)
            self.members.append(member)
            return True
        return False
    
    def create_default_party(self):
        """Create default party with 3 members"""
        # Position spread across battlefield
        positions = [
            (0, 1, 0),    # Left - Attacker
            (1.5, 1, 2.5),  # Center - Supporter
            (3, 1, 5)     # Right - Defender
        ]
        
        colors = [
            (0.2, 0.8, 1.0),   # Blue - Attacker
            (0.8, 0.8, 0.2),   # Yellow - Supporter
            (1.0, 0.2, 0.8)    # Purple - Defender
        ]
        
        roles = ["attacker", "supporter", "defender"]
        names = ["Warrior", "Mage", "Knight"]
        
        for i in range(3):
            member = PartyMember(
                self.app,
                name=names[i],
                pos=positions[i],
                role=roles[i],
                color=colors[i]
            )
            self.add_member(member)
    
    def get_alive_members(self):
        """Get list of alive members"""
        return [m for m in self.members if m.is_alive]
    
    def get_dead_members(self):
        """Get list of dead members"""
        return [m for m in self.members if not m.is_alive]
    
    def get_total_hp(self):
        """Get total HP of all members"""
        return sum(m.hp for m in self.members)
    
    def get_max_total_hp(self):
        """Get max total HP"""
        return sum(m.max_hp for m in self.members)
    
    def get_total_sp(self):
        """Get total SP of all members"""
        return sum(m.sp for m in self.members)
    
    def get_max_total_sp(self):
        """Get max total SP"""
        return sum(m.max_sp for m in self.members)
    
    def get_party_status(self):
        """Get party status dict"""
        return {
            'total_hp': self.get_total_hp(),
            'max_hp': self.get_max_total_hp(),
            'total_sp': self.get_total_sp(),
            'max_sp': self.get_max_total_sp(),
            'alive_count': len(self.get_alive_members()),
            'total_count': len(self.members),
        }
    
    def analyze_party_condition(self):
        """Analyze party condition: A, B, C, or D
        A = HP Full (80%+) & SP Full (80%+)
        B = HP Critical (<50%) & SP Full (80%+)
        C = HP Full (80%+) & SP Critical (<50%)
        D = HP Critical (<50%) & SP Critical (<50%)
        """
        avg_hp_pct = (self.get_total_hp() / self.get_max_total_hp()) if self.get_max_total_hp() > 0 else 0
        avg_sp_pct = (self.get_total_sp() / self.get_max_total_sp()) if self.get_max_total_sp() > 0 else 0
        
        # Determine condition
        if avg_hp_pct >= 0.8 and avg_sp_pct >= 0.8:
            return 'A'  # Kondisi Kuat - HP & SP Penuh
        elif avg_hp_pct < 0.5 and avg_sp_pct >= 0.8:
            return 'B'  # HP Kritis tapi SP Penuh
        elif avg_hp_pct >= 0.8 and avg_sp_pct < 0.5:
            return 'C'  # HP Penuh tapi SP Kritis
        elif avg_hp_pct < 0.5 and avg_sp_pct < 0.5:
            return 'D'  # Kondisi Kritis - HP & SP Kritis
        else:
            return 'N'  # Normal/Balanced
    
    def update(self, delta_time):
        """Update all party members"""
        for member in self.members:
            member.update(delta_time)
    
    def render(self):
        """Render all party members"""
        for member in self.members:
            member.render()
