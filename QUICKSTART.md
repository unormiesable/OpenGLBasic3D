# QUICK START GUIDE

## Setup & Installation

### 1. Install Dependencies
```bash
pip install pygame moderngl pyglm numpy
```

### 2. Run Game Manual
```bash
python main.py
```
Anda akan melihat window OpenGL dengan Player (biru) dan Monster (merah) dalam arena battle.

### 3. Run Auto-Demo
```bash
python auto_demo.py
```
Battle akan berjalan otomatis dengan AI player yang melakukan aksi berulang.

---

## Gameplay

### Battle Controls (Main Mode)

| Tombol | Fungsi |
|--------|--------|
| **1** | Normal Attack - Serangan fisik standar |
| **2** | Magic Attack - Serangan magic (cost 20 SP) |
| **3** | Defend - Bertahan untuk mengurangi damage |
| **4** | Skill - Powerful attack (cost 30 SP, damage x1.5) |
| **TAB** | Toggle camera orbit mode |
| **Mouse Wheel** | Zoom in/out (saat orbit mode aktif) |
| **~** | Toggle mouse cursor visibility |
| **R** | Reset battle (buat battle baru) |
| **ESC** | Exit game |

### Battle Mechanics

1. **Turn System**: Player dan Monster bergiliran melakukan aksi
   - Player speed 12 > Monster speed 10 → Player jalan duluan
   
2. **Resource Management**:
   - HP: Health Points (saat = 0, karakter dikalahkan)
   - SP: Skill Points (untuk magic attack dan skill)
   
3. **Action Types**:
   - **Normal Attack**: Damage standard, no SP cost
   - **Magic Attack**: 20% lebih besar damage, cost 20 SP
   - **Defend**: Kurangi damage yang diterima next turn
   - **Skill**: Damage x1.5, cost 30 SP, powerful burst

4. **AI Monster**:
   - Gunakan Skill jika HP < 30%
   - Gunakan Magic jika SP ≥ 20 (40% chance)
   - Default: Normal Attack

---

## Game Loop Flow

```
┌─────────────────┐
│  Player's Turn  │
│  Press 1-4      │
└────────┬────────┘
         │
         ↓
┌──────────────────┐     
│ Monster's Turn   │     
│ AI Decides       │
│ (Auto ~3 sec)    │
└────────┬─────────┘
         │
         ↓
  [Check Battle Status]
    ↙          ↘
[VICTORY]   [CONTINUE]
             │
             ↓
        [Back to Player Turn]
```

---

## Console Output

Setiap action akan di-log ke console dengan format:
```
[ACTION] Player uses Normal Attack on Monster! Damage: 18
→ Monster takes 18 damage! HP: 82
```

### Battle Status Display:
```
============================================================
TURN 5
============================================================

Player       │ HP: [██████████████████░░] 140/150 (93%)
             │ SP: 60/80

Monster      │ HP: [████████░░░░░░░░░░░░]  45/100 (45%)
             │ SP: 38/50

============================================================
```

---

## Example Battle Sequence

```
Turn 1: Player vs Monster
[INIT] Battle Started! Player vs Shadow

--- Turn 0 ---
Player HP: 150/150 | SP: 80/80
Monster HP: 100/100 | SP: 50/50
Current Turn: PLAYER
Status: ACTIVE

> Player presses 1 (Normal Attack)

============================================================
TURN 0
============================================================
[ACTION] Player uses Normal Attack on Monster! Damage: 18
→ Monster takes 18 damage! HP: 82

---

> Monster's AI decides...

============================================================
TURN 1
============================================================
[ACTION] Monster uses Normal Attack on Player! Damage: 12
→ Player takes 12 damage! HP: 138
```

---

## Quick Testing

### Test 1: Run Auto-Demo
```bash
python auto_demo.py
```
- Battle akan berjalan otomatis hingga selesai
- Lihat console output untuk battle log

### Test 2: Manual Play
```bash
python main.py
```
- Press 1,2,3,4 untuk berbagai aksi
- Amati monster AI response
- Press R untuk reset battle

### Test 3: Multiple Battles
```bash
python main.py
```
- Play beberapa turn
- Press R untuk reset
- Play lagi dengan strategi berbeda

---

## Tips & Tricks

### Winning Strategy:
1. Save SP untuk Magic Attack (more damage than normal)
2. Gunakan Skill saat HP monster rendah untuk finishing
3. Monitor monster HP - set pace serangan sesuai

### Monster AI Behavior:
- **Low HP Aggressive**: Saat HP < 30%, monster akan gunakan Skill
- **SP Management**: Monster recover 8 SP per turn (faster than player 5 SP)
- **Balanced Play**: Tidak terlalu aggressive, mix antara normal dan magic

---

## File Structure untuk Reference

```
├── main.py                 # Entry point
├── auto_demo.py           # Auto-play demo
├── character.py           # Player & Monster classes
├── battle_system.py       # Battle logic
├── battle_logger.py       # Console logging
├── particle_system.py     # Particle effects
├── scene.py               # Scene management
├── model.py               # 3D models
├── camera.py              # Camera control
└── shaders/
    ├── default_color.vert
    └── default_color.frag
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'moderngl'"
**Solution**: `pip install moderngl moderngltools`

### Issue: "AttributeError: 'Camera' has no attribute..."
**Solution**: Pastikan file camera.py dari template original ada

### Issue: Window tidak muncul
**Solution**: 
- Check GPU driver
- Try run: `python -c "import moderngl; print(moderngl.__version__)"`

### Issue: Battle tidak jalan
**Solution**:
- Pastikan semua file di workspace (character.py, battle_system.py, etc)
- Check console output untuk error messages
- Try run auto_demo.py untuk validate setup

---

## Next Steps

1. **Run the game**: `python main.py`
2. **Try different actions**: Press 1,2,3,4
3. **Observe AI**: Lihat monster decision making
4. **Reset & replay**: Press R untuk new battle
5. **Check logs**: Console menampilkan semua events

Enjoy your Battle Simulation!
