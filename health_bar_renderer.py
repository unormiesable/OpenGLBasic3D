"""
Health Bar Renderer - Render HP/SP bars in OpenGL as 3D quads
"""

import numpy as np
from pyglm import glm


class HealthBarRenderer:
    """Render health bars in 3D space using OpenGL quads"""
    
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.vao_dict = {}
        self.program = None
        
        self._create_bar_program()
    
    def _create_bar_program(self):
        """Create simple shader program for bars"""
        vertex_shader = '''
            #version 330 core
            
            layout(location = 0) in vec3 in_position;
            layout(location = 1) in vec3 in_color;
            
            out vec3 fragColor;
            
            uniform mat4 m_model;
            uniform mat4 m_view;
            uniform mat4 m_proj;
            
            void main() {
                gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
                fragColor = in_color;
            }
        '''
        
        fragment_shader = '''
            #version 330 core
            
            in vec3 fragColor;
            out vec4 FragColor;
            
            void main() {
                FragColor = vec4(fragColor, 0.8);
            }
        '''
        
        try:
            self.program = self.ctx.program(
                vertex_shader=vertex_shader,
                fragment_shader=fragment_shader
            )
        except Exception as e:
            print(f"Error creating bar program: {e}")
            self.program = None
    
    def _create_bar_quad(self, width=1.0, height=0.15):
        """Create a quad for health bar"""
        # Create a simple quad
        vertices = np.array([
            # pos                      color (will be overwritten)
            -width/2, 0, 0,           1, 0, 0,
             width/2, 0, 0,           1, 0, 0,
             width/2, height, 0,      1, 0, 0,
            -width/2, height, 0,      1, 0, 0,
        ], dtype='f4')
        
        indices = np.array([0, 1, 2, 0, 2, 3], dtype='i4')
        
        vbo = self.ctx.buffer(vertices.tobytes())
        ebo = self.ctx.buffer(indices.tobytes())
        
        vao = self.ctx.vertex_array(
            self.program,
            [(vbo, '3f 3f', 'in_position', 'in_color')],
            ebo
        )
        
        return vao, len(indices)
    
    def render_health_bar(self, position, current_hp, max_hp, bar_width=2.0, 
                         hp_color=(0.2, 1.0, 0.2), bg_color=(0.3, 0.3, 0.3)):
        """Render a health bar at position
        
        Args:
            position: (x, y, z) world position
            current_hp: Current HP value
            max_hp: Maximum HP value
            bar_width: Width of bar in world units
            hp_color: RGB color tuple for HP bar
            bg_color: RGB color for background
        """
        if not self.program:
            return
        
        hp_percent = max(0, min(1, current_hp / max_hp)) if max_hp > 0 else 0
        bar_height = 0.15
        
        # Background bar (gray)
        self._draw_bar_quad(
            position,
            bar_width,
            bar_height,
            bg_color
        )
        
        # HP bar (colored, fills from left)
        hp_bar_width = bar_width * hp_percent
        self._draw_bar_quad(
            (position[0] - bar_width/2 + hp_bar_width/2, position[1] + bar_height/2, position[2]),
            hp_bar_width,
            bar_height,
            hp_color
        )
    
    def render_sp_bar(self, position, current_sp, max_sp, bar_width=2.0,
                     sp_color=(0.2, 0.8, 1.0), bg_color=(0.2, 0.2, 0.3)):
        """Render a SP bar at position"""
        if not self.program:
            return
        
        sp_percent = max(0, min(1, current_sp / max_sp)) if max_sp > 0 else 0
        bar_height = 0.1
        
        # Background bar
        self._draw_bar_quad(
            position,
            bar_width,
            bar_height,
            bg_color
        )
        
        # SP bar (colored)
        sp_bar_width = bar_width * sp_percent
        self._draw_bar_quad(
            (position[0] - bar_width/2 + sp_bar_width/2, position[1] + bar_height/2, position[2]),
            sp_bar_width,
            bar_height,
            sp_color
        )
    
    def _draw_bar_quad(self, position, width, height, color):
        """Draw a simple colored quad"""
        if not self.program:
            return
        
        # Create vertex data for this quad
        half_w = width / 2
        vertices = np.array([
            -half_w, 0, 0,              color[0], color[1], color[2],
             half_w, 0, 0,              color[0], color[1], color[2],
             half_w, height, 0,         color[0], color[1], color[2],
            -half_w, height, 0,         color[0], color[1], color[2],
        ], dtype='f4')
        
        indices = np.array([0, 1, 2, 0, 2, 3], dtype='i4')
        
        vbo = self.ctx.buffer(vertices.tobytes())
        ebo = self.ctx.buffer(indices.tobytes())
        
        vao = self.ctx.vertex_array(
            self.program,
            [(vbo, '3f 3f', 'in_position', 'in_color')],
            ebo
        )
        
        # Set up model matrix to position the quad
        m_model = glm.mat4()
        m_model = glm.translate(m_model, glm.vec3(position))
        
        self.program['m_model'].write(m_model)
        self.program['m_view'].write(self.app.camera.m_view)
        self.program['m_proj'].write(self.app.camera.m_proj)
        
        vao.render()
        vao.release()
        vbo.release()
        ebo.release()
    
    def render_party_bars(self, party):
        """Render health bars for all party members"""
        bar_spacing = 0.5  # Space between bars
        
        for i, member in enumerate(party.members):
            # Position above each character
            bar_y_offset = 2.0
            bar_pos = (member.pos.x, member.pos.y + bar_y_offset, member.pos.z)
            
            # HP bar
            self.render_health_bar(
                bar_pos,
                member.hp,
                member.max_hp,
                bar_width=1.5,
                hp_color=self._get_health_color(member.hp, member.max_hp)
            )
            
            # SP bar below HP bar
            sp_bar_pos = (bar_pos[0], bar_pos[1] - 0.25, bar_pos[2])
            self.render_sp_bar(
                sp_bar_pos,
                member.sp,
                member.max_sp,
                bar_width=1.5,
                sp_color=(0.2, 0.8, 1.0)
            )
    
    def render_monster_bar(self, monster):
        """Render health bar for monster"""
        bar_y_offset = 2.0
        bar_pos = (monster.pos.x, monster.pos.y + bar_y_offset, monster.pos.z)
        
        # HP bar
        self.render_health_bar(
            bar_pos,
            monster.hp,
            monster.max_hp,
            bar_width=1.5,
            hp_color=self._get_health_color(monster.hp, monster.max_hp)
        )
        
        # SP bar
        sp_bar_pos = (bar_pos[0], bar_pos[1] - 0.25, bar_pos[2])
        self.render_sp_bar(
            sp_bar_pos,
            monster.sp,
            monster.max_sp,
            bar_width=1.5,
            sp_color=(1.0, 0.5, 0.2)  # Orange for monster
        )
    
    def _get_health_color(self, current, maximum):
        """Get color based on health percentage"""
        health_pct = current / maximum if maximum > 0 else 0
        
        if health_pct > 0.7:
            return (0.2, 1.0, 0.2)  # Green
        elif health_pct > 0.4:
            return (1.0, 1.0, 0.2)  # Yellow
        elif health_pct > 0.2:
            return (1.0, 0.5, 0.2)  # Orange
        else:
            return (1.0, 0.2, 0.2)  # Red
    
    def destroy(self):
        """Clean up resources"""
        if self.program:
            self.program.release()
