import random
import math
from pyglm import glm


class Particle:
    """Single particle untuk efek visual"""
    
    def __init__(self, pos, velocity, lifetime, color, size=0.1):
        self.pos = glm.vec3(pos)
        self.velocity = glm.vec3(velocity)
        self.lifetime = lifetime
        self.age = 0.0
        self.color = glm.vec3(color)
        self.size = size
        self.is_alive = True
    
    def update(self, delta_time):
        """Update particle physics"""
        self.age += delta_time
        
        if self.age >= self.lifetime:
            self.is_alive = False
            return
        
        # Apply gravity
        self.velocity.y -= 9.8 * delta_time * 0.5
        
        # Update position
        self.pos += self.velocity * delta_time
        
        # Fade out
        progress = self.age / self.lifetime
        self.color *= glm.vec3(1.0 - progress * 0.5)
    
    def render(self, app):
        """Render particle sebagai small sphere"""
        from model import ColorCube
        # Simple sphere representation dengan cube
        pass


class ParticleSystem:
    """System untuk manage particle effects"""
    
    def __init__(self, app):
        self.app = app
        self.particles = []
        self.effect_timers = {}
    
    def emit_explosion(self, pos, particle_count=20, color=(1.0, 0.5, 0.0)):
        """Emit explosion particle effect"""
        for _ in range(particle_count):
            # Random velocity dalam semua arah
            angle = random.random() * 2 * math.pi
            elevation = random.random() * math.pi
            speed = random.uniform(3.0, 8.0)
            
            vx = speed * math.sin(elevation) * math.cos(angle)
            vy = speed * math.cos(elevation) + random.uniform(1.0, 3.0)
            vz = speed * math.sin(elevation) * math.sin(angle)
            
            particle = Particle(
                pos=pos,
                velocity=(vx, vy, vz),
                lifetime=random.uniform(0.3, 0.8),
                color=color,
                size=random.uniform(0.05, 0.15)
            )
            self.particles.append(particle)
    
    def emit_slash_effect(self, pos, direction=(1, 0, 0)):
        """Emit slash effect particles"""
        particle_count = 15
        for _ in range(particle_count):
            # Particles spread dalam arah slash
            spread = random.uniform(-0.5, 0.5)
            velocity = glm.normalize(glm.vec3(direction))
            velocity = velocity * random.uniform(2.0, 5.0)
            velocity += glm.vec3(spread, random.uniform(-1, 1), spread)
            
            particle = Particle(
                pos=pos,
                velocity=tuple(velocity),
                lifetime=random.uniform(0.2, 0.5),
                color=(1.0, 0.8, 0.2),  # Yellow-orange
                size=random.uniform(0.08, 0.12)
            )
            self.particles.append(particle)
    
    def emit_magic_effect(self, pos, color=(0.3, 0.8, 1.0)):
        """Emit magic particle effect"""
        particle_count = 25
        for _ in range(particle_count):
            angle = random.random() * 2 * math.pi
            radius = random.uniform(0.5, 1.5)
            
            vx = math.cos(angle) * radius
            vy = random.uniform(2.0, 4.0)
            vz = math.sin(angle) * radius
            
            particle = Particle(
                pos=pos,
                velocity=(vx, vy, vz),
                lifetime=random.uniform(0.4, 0.8),
                color=color,
                size=random.uniform(0.06, 0.14)
            )
            self.particles.append(particle)
    
    def emit_hit_effect(self, pos):
        """Emit hit/impact particle effect"""
        self.emit_explosion(pos, particle_count=15, color=(1.0, 0.3, 0.3))
    
    def update(self, delta_time):
        """Update all particles"""
        alive_particles = []
        for particle in self.particles:
            particle.update(delta_time)
            if particle.is_alive:
                alive_particles.append(particle)
        
        self.particles = alive_particles
    
    def render(self):
        """Render all particles"""
        # Particles akan di-render sebagai visual indicator
        # Untuk implementasi lebih detail, bisa gunakan point sprites
        pass
    
    def clear(self):
        """Clear all particles"""
        self.particles.clear()
