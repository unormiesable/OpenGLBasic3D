import pygame as pg
import moderngl as mgl
import numpy as np
from text_overlay import SimpleBattleHUD


class SceneRenderer:
    def __init__(self, app):
        self.app = app
        self.scene = app.scene
        self.battle_hud = SimpleBattleHUD(app)
        self.hud_texture = None
        self.overlay_texture = None
        
        # 2D rendering
        self.quad_vao = None
        self.quad_program = None
        self._init_2d_rendering()
    
    def _init_2d_rendering(self):
        """Initialize 2D rendering for HUD overlay"""
        # Simple quad for 2D overlay
        vertices = np.array([
            -1.0, -1.0, 0.0, 0.0,
             1.0, -1.0, 1.0, 0.0,
            -1.0,  1.0, 0.0, 1.0,
             1.0,  1.0, 1.0, 1.0,
        ], dtype='f4')
        
        # Try to create 2D rendering, but don't fail if not available
        try:
            vbo = self.app.ctx.buffer(vertices.tobytes())
            vao = self.app.ctx.vertex_array(
                None,
                [(vbo, '2f 2f', 'in_position', 'in_texcoord')]
            )
            self.quad_vao = vao
        except:
            pass

    def render(self):
        # Render 3D scene
        for obj in self.scene.objects:
            obj.render()
        
        self.scene.render()
        
        # Update scene logic
        self.scene.update()
        
        # Render HUD overlay (using simple print for now)
        self._render_hud_console()

    def _render_hud_console(self):
        """Render HUD info to console"""
        ui_data = self.scene.get_ui_data()
        
        # Limit printing to not spam console
        if hasattr(self, '_last_log_turn'):
            if self._last_log_turn == ui_data['turn']:
                return
        
        self._last_log_turn = ui_data['turn']
        
        # Print battle status
        print(f"\n{'='*70}")
        print(f"TURN {ui_data['turn']} - Party Condition: {ui_data.get('party_condition', 'N')}")
        print(f"{'='*70}")
        
        # Party status
        party_status = ui_data['party']
        print(f"PARTY (Alive: {party_status['alive_count']}/{party_status['total_count']})")
        print(f"  Total HP: {party_status['total_hp']}/{party_status['max_hp']} | Total SP: {party_status['total_sp']}/{party_status['max_sp']}")
        
        for member in self.scene.party.members:
            status_str = member.get_status()
            print(f"  {status_str}")
        
        # Monster status
        print(f"\nMONSTER:")
        print(f"  HP: {ui_data['monster_hp']}/{ui_data['monster_max_hp']} | SP: {ui_data['monster_sp']}/{ui_data['monster_max_sp']}")
        
        # Current actor
        if ui_data['current_turn'] == 'party' and ui_data['current_actor'] is not None:
            actor = self.scene.party.members[ui_data['current_actor']]
            print(f"\n→ {actor.name}'s turn (Press 1-4 for action)")
        else:
            print(f"\n→ Monster's turn")
        
        print(f"{'='*70}")

    def destroy(self):
        if self.quad_vao:
            self.quad_vao.release()


