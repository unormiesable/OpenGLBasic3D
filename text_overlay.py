import pygame as pg
import numpy as np
from pyglm import glm


class TextOverlay:
    """Simple text overlay system menggunakan pygame"""
    
    def __init__(self, app):
        self.app = app
        self.display = pg.display.get_surface()
        self.overlay_surface = None
        self.overlay_text = []
        
        # Fonts
        self.font_small = pg.font.Font(None, 20)
        self.font_normal = pg.font.Font(None, 28)
        self.font_large = pg.font.Font(None, 36)
    
    def add_text(self, text, pos, color=(255, 255, 255), font_size='normal'):
        """Add text to be rendered"""
        if font_size == 'small':
            font = self.font_small
        elif font_size == 'large':
            font = self.font_large
        else:
            font = self.font_normal
        
        text_surface = font.render(text, True, color)
        self.overlay_text.append((text_surface, pos))
    
    def clear(self):
        """Clear all text"""
        self.overlay_text.clear()
    
    def render(self):
        """Render all overlaid text"""
        for text_surface, pos in self.overlay_text:
            if self.display:
                # Get current OpenGL framebuffer
                pixels = pg.image.tostring(text_surface, 'RGBA', True)
                
                # Simple blit using pygame (akan ter-composite setelah OpenGL render)
                # Note: ini adalah workaround karena text rendering di OpenGL kompleks
                pass
    
    def render_to_surface(self, surface):
        """Render text to a surface"""
        for text_surface, pos in self.overlay_text:
            surface.blit(text_surface, pos)


class SimpleBattleHUD:
    """Simple battle HUD menggunakan pygame surface overlay"""
    
    def __init__(self, app):
        self.app = app
        self.surface = pg.Surface(app.WIN_SIZE, pg.SRCALPHA)
        self.font_normal = pg.font.Font(None, 24)
        self.font_large = pg.font.Font(None, 32)
    
    def render_hud(self, battle_status):
        """Create HUD surface"""
        # Clear surface
        self.surface.fill((0, 0, 0, 0))
        
        width, height = self.app.WIN_SIZE
        
        # Player info (top left)
        player_hp_text = self.font_normal.render(
            f"Player HP: {battle_status['player_hp']}/{battle_status['player_max_hp']}", 
            True, (100, 200, 100)
        )
        player_sp_text = self.font_normal.render(
            f"SP: {battle_status['player_sp']}/{battle_status['player_max_sp']}", 
            True, (100, 150, 255)
        )
        
        # Monster info (top right)
        monster_hp_text = self.font_normal.render(
            f"Monster HP: {battle_status['monster_hp']}/{battle_status['monster_max_hp']}", 
            True, (200, 100, 100)
        )
        monster_sp_text = self.font_normal.render(
            f"SP: {battle_status['monster_sp']}/{battle_status['monster_max_sp']}", 
            True, (100, 150, 255)
        )
        
        # Draw on surface
        self.surface.blit(player_hp_text, (20, 20))
        self.surface.blit(player_sp_text, (20, 50))
        self.surface.blit(monster_hp_text, (width - monster_hp_text.get_width() - 20, 20))
        self.surface.blit(monster_sp_text, (width - monster_sp_text.get_width() - 20, 50))
        
        # Turn info (bottom center)
        turn_color = (100, 200, 100) if battle_status['current_turn'] == 'player' else (200, 100, 100)
        turn_text = self.font_large.render(
            f"Turn {battle_status['turn']}: {battle_status['current_turn'].upper()}", 
            True, turn_color
        )
        self.surface.blit(
            turn_text, 
            (width // 2 - turn_text.get_width() // 2, height - 50)
        )
        
        # Status
        if not battle_status.get('is_active', True):
            if battle_status['player_hp'] <= 0:
                status_text = "PLAYER DEFEATED!"
                status_color = (255, 0, 0)
            else:
                status_text = "VICTORY!"
                status_color = (0, 255, 0)
            
            status_surface = self.font_large.render(status_text, True, status_color)
            self.surface.blit(
                status_surface,
                (width // 2 - status_surface.get_width() // 2, height // 2 - 30)
            )
        
        # Controls hint
        hint_font = pg.font.Font(None, 18)
        controls = [
            "1: Normal Attack | 2: Magic | 3: Defend | 4: Skill",
            "TAB: Orbit Camera | R: Reset Battle | ESC: Exit"
        ]
        
        for i, control in enumerate(controls):
            control_text = hint_font.render(control, True, (200, 200, 200))
            self.surface.blit(control_text, (20, height - 100 + i * 25))
        
        return self.surface
    
    def draw_bar(self, surface, x, y, width, height, value, max_value, color):
        """Draw a progress bar"""
        # Background
        pg.draw.rect(surface, (50, 50, 50), (x, y, width, height))
        
        # Fill
        fill_width = int(width * (value / max_value)) if max_value > 0 else 0
        pg.draw.rect(surface, color, (x, y, fill_width, height))
        
        # Border
        pg.draw.rect(surface, (200, 200, 200), (x, y, width, height), 2)
