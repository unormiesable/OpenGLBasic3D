from pyglm import glm
import math


class Character:
    """Base class untuk karakter (Player/Monster)"""
    
    def __init__(self, app, name, pos, color, is_player=False):
        self.app = app
        self.name = name
        self.pos = glm.vec3(pos)
        self.color = glm.vec3(color)
        self.is_player = is_player
        
        # Stats
        self.max_hp = 100
        self.hp = self.max_hp
        self.max_sp = 50
        self.sp = self.max_sp
        self.attack = 15
        self.defense = 8
        self.speed = 10  # untuk menentukan urutan serangan
        
        # Status
        self.is_alive = True
        self.current_action = None
        self.target = None
        
        # Visual
        self.scale = glm.vec3(1.0, 1.5, 1.0) if is_player else glm.vec3(0.8, 1.2, 0.8)
        self.model = self._create_model()
        
        # Animation
        self.action_timer = 0.0
        self.action_duration = 0.0
        self.hit_flash = 0.0
    
    def _create_model(self):
        """Create mesh untuk karakter"""
        # Import di sini untuk menghindari circular import
        from model import ColorCapsule
        try:
            capsule = ColorCapsule(
                self.app, 
                pos=tuple(self.pos),
                scale=tuple(self.scale),
                color=tuple(self.color)
            )
            return capsule
        except Exception as e:
            print(f"Error creating capsule model: {e}")
            return None
    
    def take_damage(self, damage):
        """Menerima damage"""
        actual_damage = max(1, damage - self.defense // 2)
        self.hp = max(0, self.hp - actual_damage)
        self.hit_flash = 0.2
        
        if self.hp <= 0:
            self.is_alive = False
        
        return actual_damage
    
    def consume_sp(self, amount):
        """Konsumsi SP"""
        if self.sp >= amount:
            self.sp -= amount
            return True
        return False
    
    def recover_sp(self, amount=5):
        """Recover SP setiap turn"""
        self.sp = min(self.max_sp, self.sp + amount)
    
    def recover_hp(self, amount):
        """Recover HP"""
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp
    
    def get_hp_percentage(self):
        """Return persentase HP (0-1)"""
        return max(0, min(1, self.hp / self.max_hp))
    
    def get_sp_percentage(self):
        """Return persentase SP (0-1)"""
        return max(0, min(1, self.sp / self.max_sp))
    
    def update(self, delta_time):
        """Update character logic"""
        self.hit_flash = max(0, self.hit_flash - delta_time)
        self.action_timer += delta_time
        
        # Update model position
        if self.model:
            self.model.pos = self.pos
            self.model.m_model = self.model.get_model_matrix()
            
            # Flash effect saat terkena damage
            if self.hit_flash > 0:
                flash_intensity = (self.hit_flash / 0.2) * 0.5
                self.model.color = glm.vec3(1.0) + glm.vec3(flash_intensity)
            else:
                self.model.color = self.color
    
    def render(self):
        """Render character"""
        if self.model:
            self.model.render()
    
    def perform_action(self, action_type, target, damage):
        """Perform attack action"""
        self.current_action = action_type
        self.target = target
        self.action_duration = 0.5
        self.action_timer = 0
        
        if target:
            target.take_damage(damage)
    
    def is_action_complete(self):
        """Check if current action is complete"""
        return self.action_timer >= self.action_duration


class Player(Character):
    """Karakter Player"""
    
    def __init__(self, app, name="Player", pos=(0, 1, 0)):
        super().__init__(app, name, pos, (0.2, 0.8, 1.0), is_player=True)
        self.max_hp = 150
        self.hp = self.max_hp
        self.max_sp = 80
        self.sp = self.max_sp
        self.attack = 20
        self.defense = 12
        self.speed = 12


class Monster(Character):
    """Karakter Monster"""
    
    def __init__(self, app, name="Monster", pos=(3, 1, 0), monster_type="normal"):
        color_map = {
            "normal": (1.0, 0.2, 0.2),
            "strong": (1.0, 0.0, 0.0),
            "weak": (1.0, 0.8, 0.2),
        }
        color = color_map.get(monster_type, (1.0, 0.2, 0.2))
        
        super().__init__(app, name, pos, color, is_player=False)
        self.monster_type = monster_type
        
        # Variasi stat berdasarkan type
        if monster_type == "strong":
            self.max_hp = 120
            self.hp = self.max_hp
            self.attack = 25
            self.defense = 10
            self.speed = 8
        elif monster_type == "weak":
            self.max_hp = 60
            self.hp = self.max_hp
            self.attack = 12
            self.defense = 5
            self.speed = 14
