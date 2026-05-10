from model import ColorPlane
from character import Monster
from party import Party
from advanced_battle_system import AdvancedBattleSystem
from particle_system import ParticleSystem
from health_bar_renderer import HealthBarRenderer
from ui_renderer import UIRenderer


class Scene:
    def __init__(self, app, use_advanced=True):
        self.app = app
        self.objects = []
        
        # Battle components
        self.party = None
        self.monster = None
        self.battle_system = None
        self.particle_system = ParticleSystem(app)
        self.health_bar_renderer = HealthBarRenderer(app)
        self.ui_renderer = UIRenderer(app)
        
        # Battle state
        self.battle_timer = 0.0
        self.action_delay = 2.0  # Delay antara turns
        self.use_advanced = use_advanced
        
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        add = self.add_object
        app = self.app

        # Ground
        add(ColorPlane(app, scale=(10, 10, 10)))
        
        # Create party
        self.party = Party(app)
        self.party.create_default_party()
        
        # Add party members to scene
        for member in self.party.members:
            add(member)
        
        # Create monster
        self.monster = Monster(app, name="Shadow Overlord", pos=(6, 1, 0), monster_type="strong")
        add(self.monster)
        
        # Battle system
        if self.use_advanced:
            self.battle_system = AdvancedBattleSystem(app, self.party, self.monster)
        else:
            from battle_system import BattleSystem
            from character import Player
            player = Player(app, name="Player", pos=(0, 1, 0))
            add(player)
            self.battle_system = BattleSystem(app, player, self.monster)

    def update(self):
        delta_time = self.app.delta_time / 1000.0  # Convert milliseconds to seconds
        
        # Update scene objects
        for o in self.objects:
            o.update(delta_time)
        
        # Update particle system
        self.particle_system.update(delta_time)
        
        # Update battle system
        self.battle_system.update(delta_time)
        
        # Handle AI turns dengan timing
        self.battle_timer += delta_time
        if self.battle_timer >= self.action_delay:
            self.battle_system.update_ai(delta_time)
            self.battle_timer = 0.0
            
            # Emit particles pada serangan monster
            if self.battle_system.monster.current_action == "slash":
                direction = self.party.members[0].pos - self.monster.pos
                self.particle_system.emit_slash_effect(
                    tuple(self.battle_system.monster.pos),
                    direction=tuple(direction)
                )
            elif self.battle_system.monster.current_action == "magic":
                self.particle_system.emit_magic_effect(
                    tuple(self.battle_system.monster.pos)
                )
            elif self.battle_system.monster.current_action in ["multi"]:
                self.particle_system.emit_explosion(
                    tuple(self.battle_system.monster.pos),
                    particle_count=30
                )
    
    def render(self):
        # Render objects
        for o in self.objects:
            o.render()
        
        # Render particle effects
        self.particle_system.render()
        
        # Render health bars
        self.health_bar_renderer.render_party_bars(self.party)
        self.health_bar_renderer.render_monster_bar(self.monster)
    
    def get_ui_data(self):
        """Get data untuk UI rendering"""
        return self.battle_system.get_battle_status()
    
    def get_ui_data(self):
        """Get data untuk UI rendering"""
        status = self.battle_system.get_battle_status()
        status['turn'] = self.battle_system.turn_counter
        return status
