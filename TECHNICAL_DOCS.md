# Dokumentasi Teknis - Algoritma & Sistem

## 1. Battle System Architecture

### State Machine
```
INITIALIZATION
    ↓
┌─────────────────────────────────┐
│   PLAYER_TURN                   │
│   - Wait for player input       │
│   - Execute action              │
│   - Log damage & effects        │
└──────────────┬──────────────────┘
               ↓
      [Turn Counter++]
               ↓
┌──────────────────────────────────┐
│   MONSTER_TURN                   │
│   - AI decision making           │
│   - Execute action               │
│   - Calculate damage             │
└──────────────┬───────────────────┘
               ↓
     [Check battle status]
      ↙              ↘
[ACTIVE]          [END]
  ↓                  ↓
Loop          [VICTORY/DEFEAT]
```

### Turn Order Calculation
```python
if player.speed >= monster.speed:
    current_turn = 'player'
else:
    current_turn = 'monster'
```

Stats:
- Player.speed = 12
- Monster.speed = 10
- Result: Player goes first

---

## 2. Damage Calculation System

### Formula
```python
base_damage = attacker.attack
# For magic: base_damage *= 1.2

variance = random(-5, +5)

if is_magic:
    defense_reduction = target.defense * 0.5
else:
    defense_reduction = target.defense * 0.3

final_damage = max(5, int(base_damage + variance - defense_reduction))
```

### Example Calculation
```
Player Normal Attack vs Monster:
  base_damage = 20
  variance = +2 (random)
  defense_reduction = 8 * 0.3 = 2.4
  final_damage = max(5, int(20 + 2 - 2.4)) = 19

Player Magic Attack vs Monster:
  base_damage = 20 * 1.2 = 24
  variance = -1 (random)
  defense_reduction = 8 * 0.5 = 4
  final_damage = max(5, int(24 - 1 - 4)) = 19

Player Skill vs Monster (damage x1.5):
  base_damage = 24 * 1.5 = 36
  variance = +3 (random)
  defense_reduction = 8 * 0.5 = 4
  final_damage = max(5, int(36 + 3 - 4)) = 35
```

---

## 3. AI Decision Making (Persona-Inspired Algorithm)

### Decision Tree
```python
def _get_ai_action():
    monster.recover_sp(8)
    
    if monster.hp < monster.max_hp * 0.3 and monster.sp >= 30:
        return ActionType.SKILL  # Low HP → Burst damage
    
    elif monster.sp >= 20 and random() < 0.4:
        return ActionType.MAGIC_ATTACK  # 40% chance for magic
    
    else:
        return ActionType.NORMAL_ATTACK  # Default
```

### Priority Levels
```
Priority 1 (Highest): Emergency Skill
  - Condition: HP < 30% AND SP >= 30
  - Reason: Desperate attempt to turn tide
  - Behavior: High damage burst attack

Priority 2 (Medium): Magic Attack
  - Condition: SP >= 20
  - Chance: 40%
  - Reason: Better damage than normal attack
  - Cost: 20 SP (40% of max)

Priority 3 (Low): Normal Attack
  - Condition: Always available
  - Reason: Default safe option
  - Cost: 0 SP (always available)
```

### Adaptive Behavior
```
Monster HP Status          | Action Tendency
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> 60%                      | Mix of normal + magic (40% magic)
40-60%                     | Maintain pressure (40% magic)
30-40%                     | Increase aggression (50% magic)
< 30%                      | Desperate Skill spam (if SP available)
```

---

## 4. Resource Management System

### SP (Skill Points) Recovery
```python
# Player recovery
player.recover_sp(5)  # Per turn

# Monster recovery
monster.recover_sp(8)  # Per turn (faster)

# Total per 5 turns:
# Player: +25 SP
# Monster: +40 SP
```

### Action Costs
```
Normal Attack:  0 SP
Defend:         0 SP
Magic Attack:   20 SP
Skill:          30 SP
```

### SP Management Strategy
```
Player Strategy (manual control):
- Use Magic at turn 4 (when SP = 80-20 = 60)
- Use Skill at turn 6 (when SP = 60-30 = 30, need another +30)
- Balance between normal attacks & skills

Monster Strategy (auto):
- Recover 8 SP/turn
- Use Magic every 2-3 turns (when SP ≥ 20)
- Save for Skill if HP drops low
```

---

## 5. Character Stats System

### Player Stats
```
HP:      150  (high survivability)
SP:      80   (good skill point pool)
ATK:     20   (offensive power)
DEF:     12   (defensive capability)
SPD:     12   (first to act)

Survivability: 150 HP + 12 DEF → Can take hits
Damage Output: 20 ATK base → Decent sustained damage
Skill Potential: 80 SP → Can use multiple skills
```

### Monster Stats (Normal)
```
HP:      100  (balanced)
SP:      50   (moderate skill pool)
ATK:     15   (lower than player)
DEF:     8    (lower defense)
SPD:     10   (acts second)

Weakness: Lower ATK & DEF means player advantage
Compensation: SP recovery 8/turn (faster than player 5/turn)
```

### Monster Variants
```
TYPE: STRONG
- HP:  120 (+20%)
- ATK: 25  (+67%)
- DEF: 10  (+25%)
- SPD: 8   (-20%)
- Threat: High damage output
- Weakness: Slower, easier to act first

TYPE: WEAK
- HP:  60  (-40%)
- ATK: 12  (-20%)
- DEF: 5   (-37%)
- SPD: 14  (+40%)
- Threat: Acts faster
- Weakness: Low HP, easy to defeat
```

---

## 6. Particle System Architecture

### Particle Lifecycle
```
1. EMISSION
   - Position: Determined by action source
   - Velocity: Random direction based on effect type
   - Lifetime: Random 0.2-0.8 seconds
   
2. UPDATE
   - Position: pos += velocity * dt
   - Velocity: velocity.y -= gravity * dt
   - Age: age += dt
   
3. FADE
   - Color: color *= (1 - age/lifetime)
   - Size: maintained constant
   
4. DEATH
   - When: age >= lifetime
   - Action: Remove from active list
```

### Effect Types

#### Slash Effect (Physical)
```python
particle_count = 15
color = (1.0, 0.8, 0.2)  # Yellow-orange
lifetime = 0.2-0.5s
velocity = direction * random(2-5) + spread(-0.5 to 0.5)
```

#### Magic Effect (Mystical)
```python
particle_count = 25
color = (0.3, 0.8, 1.0)  # Cyan-blue
lifetime = 0.4-0.8s
velocity = spiral upward with radius spread
```

#### Explosion (Impact)
```python
particle_count = 20
color = (1.0, 0.5, 0.0)  # Red-orange
lifetime = 0.3-0.8s
velocity = random 3D spread all directions
```

---

## 7. Event Logging System

### Log Levels
```
[INIT]     - System initialization
[STATE]    - State changes
[ACTION]   - Action taken
[DAMAGE]   - Damage dealt
[WARNING]  - Warnings
[VICTORY]  - Battle victory
[DEFEAT]   - Battle defeat
```

### Log Format
```
[LEVEL] Message

Example:
[ACTION] Player uses Normal Attack on Monster! Damage: 18
→ Monster takes 18 damage! HP: 82
```

### Battle Status Display
```
============================================================
TURN 5
============================================================

Player       │ HP: [████████████░░░░░░░░] 100/150 (67%)
             │ SP: 45/80

Monster      │ HP: [██████░░░░░░░░░░░░░░░░]  45/100 (45%)
             │ SP: 38/50

============================================================
```

---

## 8. Turn Timing System

### Turn Delay
```python
action_delay = 1.0  # seconds between turns

# In scene.py update():
battle_timer += delta_time
if battle_timer >= action_delay:
    battle_system.update_ai(delta_time)
    battle_timer = 0.0
```

### Frame Rate Management
```python
FPS = 60  # Target frame rate
dt_per_frame ≈ 16.67 ms

Turn happens every:
1.0 second / 16.67 ms = ~60 frames

This allows smooth camera/animation updates
while maintaining clear turn separation
```

---

## 9. 3D Rendering System

### Model Hierarchy
```
Scene
├── ColorPlane (ground)
├── Player (ColorCapsule)
│   ├── Position: (0, 1, 0)
│   ├── Scale: (1.0, 1.5, 1.0)
│   ├── Color: (0.2, 0.8, 1.0) blue
│   └── Model Matrix: Translation × Rotation × Scale
└── Monster (ColorCapsule)
    ├── Position: (4, 1, 0)
    ├── Scale: (0.8, 1.2, 0.8)
    ├── Color: (1.0, 0.2, 0.2) red
    └── Model Matrix: Translation × Rotation × Scale
```

### Capsule Mesh Generation
```python
# Top hemisphere + Bottom hemisphere + Cylinder
# Segments: 16
# Rings: 8
# Total vertices: ~256
# Total triangles: ~512

vertices_layout = [
    (x, y, z),  # Position
    (nx, ny, nz)  # Normal
]
```

### Lighting Setup
```
Light Position: (6.0, 8.0, 6.0)
Light Type: Point light
Color: White (1.0, 1.0, 1.0)
Intensity: 1.2

Material Properties:
- Ambient (Ia)
- Diffuse (Id)
- Specular (Is)
```

---

## 10. Performance Considerations

### Optimization Points
```
Particle Management:
- Remove dead particles every frame
- Limit max particles: 500
- Use simple sphere representation

Model Rendering:
- Reuse VAO/VBO
- Single batch render per frame
- Simple color-based shading

Scene Updates:
- Update delta_time once per frame
- Batch character updates
- Lazy particle emission (only on action)
```

### Memory Usage
```
Per Battle:
- Player Object:    ~2 KB
- Monster Object:   ~2 KB
- Particles (100):  ~4 KB
- Battle System:    ~1 KB
- Total:            ~10 KB

Minimal memory footprint, suitable for resource-constrained systems
```

---

## Implementation Checklist

- [x] Character class with stats
- [x] Player & Monster classes
- [x] Turn-based battle system
- [x] Damage calculation
- [x] AI decision making
- [x] Resource management (HP/SP)
- [x] Particle system
- [x] Logging system
- [x] 3D rendering (capsule models)
- [x] Camera system
- [x] Scene management
- [ ] Text overlay rendering (future)
- [ ] Sound effects (future)
- [ ] Advanced animations (future)
