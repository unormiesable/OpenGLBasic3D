import pygame as pg
from pyglm import glm


class UIRenderer:
    """Render UI elements seperti HP/SP bars"""
    
    def __init__(self, app):
        self.app = app
        self.font = pg.font.Font(None, 24)
        self.font_large = pg.font.Font(None, 36)
        self.ui_texture = None
    
    def render_health_bar(self, surface, x, y, width=150, height=20, hp_percent=1.0, 
                          sp_percent=1.0, name="Character", is_player=True):
        """Render health dan SP bar"""
        # Background
        bar_bg_color = (50, 50, 50)
        pg.draw.rect(surface, bar_bg_color, (x, y, width, height))
        
        # HP bar (merah)
        hp_width = int(width * hp_percent)
        hp_color = (100, 200, 100) if is_player else (200, 100, 100)
        pg.draw.rect(surface, hp_color, (x, y, hp_width, height))
        
        # HP border
        pg.draw.rect(surface, (200, 200, 200), (x, y, width, height), 2)
        
        # SP bar (biru, di bawah HP)
        sp_y = y + height + 5
        sp_width = int(width * sp_percent)
        sp_color = (100, 150, 255)
        pg.draw.rect(surface, (50, 50, 50), (x, sp_y, width, height // 2))
        pg.draw.rect(surface, sp_color, (x, sp_y, sp_width, height // 2))
        pg.draw.rect(surface, (200, 200, 200), (x, sp_y, width, height // 2), 1)
        
        # Name text
        name_text = self.font.render(name, True, (255, 255, 255))
        surface.blit(name_text, (x - 50, y - 25))
    
    def render_battle_info(self, surface, battle_status):
        """Render informasi battle"""
        width, height = surface.get_size()
        
        # Player info (left side)
        player_x, player_y = 20, 20
        self.render_health_bar(
            surface, player_x, player_y,
            hp_percent=battle_status['player_hp'] / max(1, battle_status['player_max_hp']),
            sp_percent=battle_status['player_sp'] / max(1, battle_status['player_max_sp']),
            name="Player",
            is_player=True
        )
        
        # Monster info (right side)
        monster_x = width - 200
        monster_y = 20
        self.render_health_bar(
            surface, monster_x, monster_y,
            hp_percent=battle_status['monster_hp'] / max(1, battle_status['monster_max_hp']),
            sp_percent=battle_status['monster_sp'] / max(1, battle_status['monster_max_sp']),
            name="Monster",
            is_player=False
        )
        
        # Turn info
        turn_text = f"Turn: {battle_status.get('turn', 0)}"
        if battle_status.get('current_turn') == 'player':
            turn_text += " - PLAYER TURN"
            color = (100, 200, 100)
        else:
            turn_text += " - MONSTER TURN"
            color = (200, 100, 100)
        
        turn_surface = self.font_large.render(turn_text, True, color)
        surface.blit(turn_surface, (width // 2 - turn_surface.get_width() // 2, height - 50))
        
        # Battle active status
        if not battle_status.get('is_active', True):
            status_text = "BATTLE ENDED"
            status_surface = self.font_large.render(status_text, True, (255, 255, 0))
            surface.blit(status_surface, (width // 2 - status_surface.get_width() // 2, height // 2))
    
    def create_ui_surface(self, width, height, battle_status):
        """Create UI surface untuk di-overlay ke OpenGL"""
        surface = pg.Surface((width, height), pg.SRCALPHA)
        surface.fill((0, 0, 0, 0))  # Transparent background
        
        self.render_battle_info(surface, battle_status)
        
        return surface
    
    def render_text_2d(self, text, x, y, color=(255, 255, 255), size=24):
        """Render text 2D"""
        font = pg.font.Font(None, size)
        text_surface = font.render(text, True, color)
        return text_surface
