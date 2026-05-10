import sys
import pygame as pg
import moderngl as mgl

from camera import Camera
from point_light import PointLight
from mesh import Mesh
from scene import Scene
from scene_renderer import SceneRenderer
from advanced_battle_system import ActionType


class SxvxnEngine:
    def __init__(self, win_size=(1280, 720)):
        pg.init()
        pg.display.set_caption("Advanced Battle Simulation - Party vs Monster")
        self.WIN_SIZE = win_size

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.ctx = mgl.create_context(require=330)
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        self.ctx.gc_mode = 'auto'

        self.clock = pg.time.Clock()
        self.time = 0.0
        self.delta_time = 0.0
        self.background_color = (0.10, 0.12, 0.16)

        self.light = PointLight(position=(6.0, 8.0, 6.0), color=(1.0, 1.0, 1.0), intensity=1.2)
        self.camera = Camera(self)
        self.mesh = Mesh(self)
        self.scene = Scene(self, use_advanced=True)
        self.scene_renderer = SceneRenderer(self)
        
        self.current_member = 0  # Current party member acting

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.destroy()
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN and event.key == pg.K_TAB:
                self.camera.use_orbit = not self.camera.use_orbit
                self.camera.set_default()

            if event.type == pg.KEYDOWN and event.key == pg.K_BACKQUOTE:
                visible = not pg.mouse.get_visible()
                pg.mouse.set_visible(visible)
                pg.event.set_grab(not visible)

            if event.type == pg.MOUSEBUTTONDOWN and self.camera.use_orbit:
                if event.button == 4:
                    self.camera.orbit_radius = max(2.0, self.camera.orbit_radius - 0.5)
                elif event.button == 5:
                    self.camera.orbit_radius = min(40.0, self.camera.orbit_radius + 0.5)
            
            # Battle controls for party actions
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    # Normal Attack
                    self.scene.battle_system.execute_party_action(
                        self.current_member, 
                        ActionType.NORMAL_ATTACK
                    )
                elif event.key == pg.K_2:
                    # Magic Attack
                    self.scene.battle_system.execute_party_action(
                        self.current_member,
                        ActionType.MAGIC_ATTACK
                    )
                elif event.key == pg.K_3:
                    # Defend
                    self.scene.battle_system.execute_party_action(
                        self.current_member,
                        ActionType.DEFEND
                    )
                elif event.key == pg.K_4:
                    # Skill
                    self.scene.battle_system.execute_party_action(
                        self.current_member,
                        ActionType.SKILL
                    )
                elif event.key == pg.K_5:
                    # Heal
                    self.scene.battle_system.execute_party_action(
                        self.current_member,
                        ActionType.HEAL,
                        self.scene.party.members[self.current_member]
                    )
                elif event.key == pg.K_6:
                    # Multi Attack
                    self.scene.battle_system.execute_party_action(
                        self.current_member,
                        ActionType.MULTI_ATTACK
                    )
                elif event.key == pg.K_r:
                    # Reset battle
                    self.scene = Scene(self, use_advanced=True)
                    self.scene_renderer.scene = self.scene
                    self.current_member = 0

    def render(self):
        self.ctx.clear(color=self.background_color)
        self.scene_renderer.render()
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def destroy(self):
        self.mesh.destroy()
        self.scene_renderer.destroy()

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.delta_time = self.clock.tick(60)
            self.render()


if __name__ == '__main__':
    app = SxvxnEngine()
    app.run()
