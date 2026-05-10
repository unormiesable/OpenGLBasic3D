# Battle Simulation - Turn-Based Battle dengan Visualisasi 3D OpenGL

## Deskripsi Proyek

Simulasi turn-based battle dengan visualisasi 3D berbasis OpenGL yang menampilkan pertarungan antara Player dan Monster. Sistem ini menggunakan algoritma prioritas serangan yang didasarkan pada parameter HP dan SP, terinspirasi dari mekanika Persona 3 Reload dan Persona 5 Royal.

### Fitur Utama:
- **Karakter 3D**: Player (biru) dan Monster (merah) dengan model capsule
- **Turn-Based Battle System**: Sistem pertarungan berbasis giliran dengan prioritas berdasarkan kecepatan
- **AI Monster**: Algoritma cerdas yang membuat keputusan berdasarkan kondisi HP dan SP
- **Status Bar**: Indikator HP dan SP untuk kedua karakter
- **Efek Visual**: Particle effects untuk serangan (slash, magic)
- **Sistem Action**: Normal Attack, Magic Attack, Defend, Skill
- **Orbit Camera**: Kontrol kamera interaktif untuk observasi battle

## Struktur File

### Core Systems
- **character.py**: Definisi class Character, Player, dan Monster
- **battle_system.py**: Logic turn-based battle dan AI decision making
- **particle_system.py**: Sistem particle untuk efek visual serangan
- **text_overlay.py**: UI rendering untuk HUD battle

### 3D Graphics
- **model.py**: Base model classes dan model definitions
- **mesh.py**: Mesh management
- **vao.py**: Vertex Array Objects
- **vbo.py**: Vertex Buffer Objects (termasuk ColorCapsule)
- **scene.py**: Scene management dan object orchestration
- **scene_renderer.py**: Rendering engine

### Shader
- **shaders/default_color.vert**: Vertex shader
- **shaders/default_color.frag**: Fragment shader

### Main
- **main.py**: Entry point dan main engine loop
- **camera.py**: Camera control (dari template)
- **point_light.py**: Lighting system (dari template)
- **shader_program.py**: Shader program management

## Kontrol Game

| Tombol | Aksi |
|--------|------|
| **1** | Normal Attack (Physical attack biasa) |
| **2** | Magic Attack (Serangan magic, butuh 20 SP) |
| **3** | Defend (Pertahanan) |
| **4** | Skill (Powerful skill, butuh 30 SP) |
| **TAB** | Toggle Orbit Camera |
| **Mouse Wheel** | Zoom in/out (saat orbit camera aktif) |
| **~** | Toggle mouse visibility |
| **R** | Reset Battle |
| **ESC** | Exit Game |

## Mekanika Battle

### Turn Order
- Urutan turn ditentukan oleh parameter `speed` masing-masing karakter
- Player speed: 12, Monster speed: 10 (Player lebih cepat)

### Damage Calculation
```
base_damage = attacker.attack (magic attack x1.2)
variance = random(-5, +5)
defense_reduction = target.defense * 0.3 untuk physical, x0.5 untuk magic
total_damage = max(5, base_damage + variance - defense_reduction)
```

### AI Decision (Persona-inspired)
Monster membuat keputusan berdasarkan:
1. **Low HP (< 30%)** dengan SP cukup → Gunakan Skill untuk burst damage
2. **SP >= 20** dengan 40% chance → Gunakan Magic Attack
3. **Default** → Normal Attack

### Resource Management
- **HP**: Health Points - karakter defeat saat HP = 0
- **SP**: Skill Points - resource untuk skills
  - Magic Attack: cost 20 SP
  - Skill: cost 30 SP
  - Recovery: +5 SP per turn untuk player, +8 SP untuk monster

## Character Stats

### Player
- Max HP: 150
- Max SP: 80
- Attack: 20
- Defense: 12
- Speed: 12

### Monster (Normal)
- Max HP: 100
- Max SP: 50
- Attack: 15
- Defense: 8
- Speed: 10

### Monster Types (dapat di-extend)
- **normal**: Stats standard
- **strong**: HP 120, ATK 25, DEF 10, SPD 8
- **weak**: HP 60, ATK 12, DEF 5, SPD 14

## Efek Visual

### Particle System
- **Slash Effect**: Partikel kuning-orange untuk serangan fisik
- **Magic Effect**: Partikel biru untuk serangan magic
- **Explosion**: Partikel merah untuk hit effect
- **Hit Flash**: Karakter berflash putih saat terkena damage

### Visual Feedback
- Karakter capsule berubah warna saat hit
- Particle effects emit dari posisi attacker/target
- Camera dapat digeser untuk melihat battle dari sudut berbeda

## Extensibility

### Menambah Monster Type Baru
Edit `character.py` dalam class `Monster.__init__`:
```python
color_map = {
    "normal": (1.0, 0.2, 0.2),
    "strong": (1.0, 0.0, 0.0),
    "weak": (1.0, 0.8, 0.2),
    "custom": (0.5, 0.5, 1.0),  # Add here
}
```

### Menambah Action Type Baru
Edit `battle_system.py`:
1. Tambah ke enum `ActionType`
2. Implementasi logic di `_execute_action()`
3. Tambah keputusan AI di `_get_ai_action()` jika diperlukan

### Custom Particle Effects
Edit `particle_system.py`:
```python
def emit_custom_effect(self, pos, color):
    # Custom particle emission
    pass
```

## Teknis Implementation

### Game Loop
1. **Input Processing**: Check events (keyboard, mouse)
2. **Update**: Update scene, characters, battle logic
3. **Render**: Render 3D scene, particle effects
4. **Display**: Flip frame buffer

### Battle State Machine
```
PLAYER_TURN -> execute action -> MONSTER_TURN -> AI decision -> PLAYER_TURN
                                                      |
                                                 (repeat until battle_active = False)
```

### Particle Lifecycle
- Emit: Create particles dengan random velocity
- Update: Physics simulation (gravity, position)
- Fade: Opacity decrease over lifetime
- Remove: Delete saat lifetime expired

## Debugging

Console output menampilkan:
```
--- Turn N ---
Player: HP X/Y | SP A/B
Monster: HP X/Y | SP A/B
Current Turn: PLAYER/MONSTER
Status: ACTIVE/ENDED
```

## Requirements

- Python 3.x
- pygame
- moderngl
- pyglm
- numpy

Install: `pip install pygame moderngl pyglm numpy`

## Catatan Pengembangan

### TODO Features
- [ ] Multiple monsters di battle
- [ ] Battle cutscenes
- [ ] Sound effects
- [ ] Status effects (poison, stun, etc)
- [ ] Equipment system
- [ ] Level progression
- [ ] Save/Load system

### Known Issues
- Text overlay belum di-render ke OpenGL window (menampilkan di console saja)
- Particle effects logic ready tapi visual rendering simplified
- Camera tidak auto-track karakter

### Future Improvements
- Implementasi text rendering ke OpenGL texture
- Advanced particle shaders
- Skeletal animation untuk karakter
- Dynamic difficulty scaling
- Battle statistics UI
