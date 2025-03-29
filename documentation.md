# The Bad Elementals - Game Documentation

## Project Structure

```
project_root/
├── assets/         # Contains all game images
├── src/            # Source code modules
│   ├── __init__.py
│   ├── constants.py
│   ├── button.py
│   ├── game_state.py
│   ├── screens.py
│   └── utils.py
├── main.py         # Main game loop and initialization
└── documentation.md
```

## Module Descriptions

### 1. constants.py
Contains all game constants and configuration values:
- `CELL_SIZE`: Size of each grid cell (50 pixels)
- `GRID_SIZE`: Number of cells in grid (10x10)
- `WINDOW_SIZE`: Total window size (CELL_SIZE * GRID_SIZE)
- Color definitions (WHITE, BLACK, GRAY, etc.)
- `MESSAGE_DURATION`: How long messages display (2 seconds)

### 2. button.py
Implements the Button class for interactive UI elements:
- `__init__(x, y, width, height, text, color)`: Creates a new button
- `draw(surface)`: Renders the button with hover effect
- `is_clicked(pos)`: Checks if button was clicked

### 3. game_state.py
Manages the game's state and logic:
- `__init__()`: Initializes game state
- `reset_game()`: Resets all game variables to starting state
- `next_level()`: Advances to next level, resetting necessary variables
- `show_message(text)`: Displays a message to the player
- `is_message_active()`: Checks if a message should still be displayed

### 4. screens.py
Handles rendering of different game screens:

`draw_start_screen(screen, start_button, title_font, controls_font)`:
- Displays game title
- Shows controls and objectives
- Renders start button

`draw_game_over_screen(screen, victory, try_again_button, exit_button, floor_img, title_font, message_font)`:
- Shows victory or game over message
- Displays semi-transparent overlay
- Renders try again and exit buttons
- Shows appropriate end-game message

`draw_message(screen, message, message_font)`:
- Handles message display with text wrapping
- Creates background box for message
- Splits long messages into two lines if needed

### 5. utils.py
Utility functions for the game:
- `load_image(name, size)`: Loads and scales game images
- `get_random_position()`: Generates random grid positions
- `get_door_position()`: Places door on grid edges

### 6. main.py
Main game file that ties everything together:

Initialization:
- Pygame setup
- Font initialization
- Asset loading
- Button creation
- Game state initialization

Game Loop:
1. Event Handling:
   - Quit game
   - Button clicks
   - Game state transitions

2. Game Logic:
   - Player movement (WASD controls)
   - Item collection (key, swords)
   - Enemy encounters
   - Level progression

3. Rendering:
   - Floor tiles
   - Grid lines
   - Game objects (player, enemies, items)
   - UI elements (inventory, messages)

## Game Mechanics

### Levels
The game has three levels, each featuring:
1. Grass Level: Green monster, requires grass sword
2. Fire Level: Fire monster, requires fire sword
3. Water Level: Water monster, requires water sword

### Gameplay Flow
1. Find the key
2. Open the chest to get elemental sword
3. Defeat the level's monster
4. Reach the door to progress
5. Complete all three levels to win

### Controls
- W: Move Up
- A: Move Left
- S: Move Down
- D: Move Right

### Items
- Key: Required to open chests
- Swords: Each type effective against specific monster
- Chest: Contains level-specific sword

## Visual Elements
- Custom sprites for all game elements
- Fallback emoji if images unavailable
- Inventory display
- Message system
- Grid-based movement
- Level indicator
- Start and game over screens 

## Dictionary Implementation

The game uses Python dictionaries to store and manage game data, demonstrating the use of this data structure. The dictionaries are implemented in `src/game_data.py`:

### Monster Dictionary
```python
MONSTERS = {
    'grass_monster': {
        'name': 'Grass Monster',
        'type': 'grass',
        'weakness': 'grass_sword',
        'description': 'A nature elemental creature',
        'defeat_message': 'The grass monster withers away!',
        'image': 'Grass Monster.png',
        'emoji': '🌿'
    },
    # ... other monsters
}
```

### Sword Dictionary
```python
SWORDS = {
    'grass_sword': {
        'name': 'Grass Sword',
        'type': 'grass',
        'description': 'A sword imbued with nature\'s power',
        'image': 'Grass Sword.png',
        'emoji': '🌿'
    },
    # ... other swords
}
```

### Item Dictionary
```python
ITEMS = {
    'key': {
        'name': 'Magic Key',
        'description': 'A mystical key that can open any chest',
        'image': 'key.png',
        'emoji': '🔑'
    },
    # ... other items
}
```

### Dictionary Usage Examples:
1. **Retrieving Monster Information**:
   ```python
   monster_info = get_monster_info(level)
   description = monster_info['description']
   ```

2. **Getting Sword Details**:
   ```python
   sword_info = get_sword_info('grass_sword')
   name = sword_info['name']
   ```

3. **Accessing Item Data**:
   ```python
   key_info = get_item_info('key')
   description = key_info['description']
   ```

The dictionary implementation provides several benefits:
- Organized data structure for game content
- Easy access to game information
- Centralized management of game assets
- Flexible system for adding new items and monsters
- Consistent data format across the game 

## Custom Character Feature

The game includes a custom character upload feature that allows players to personalize their gaming experience:

### Upload Button
- Located on the start screen
- Allows players to select their own character image
- Supports PNG format images
- Automatically scales images to match game dimensions

### Implementation Details
```python
def handle_image_upload():
    # Opens file dialog for PNG selection
    file_path = filedialog.askopenfilename(
        title="Select Character Image",
        filetypes=[("PNG files", "*.png")]
    )
    
    # Loads and scales the image
    custom_image = load_image(file_path)
    if custom_image:
        game_state.set_custom_player_image(custom_image)
```

### Features
1. **Image Selection**:
   - Uses tkinter file dialog
   - Filters for PNG files only
   - Provides user-friendly interface

2. **Image Processing**:
   - Automatic scaling to game cell size
   - Fallback to default character if loading fails
   - Error handling with user feedback

3. **State Management**:
   - Stores custom image in game state
   - Persists until game reset
   - Default character fallback system

4. **User Feedback**:
   - Success/failure messages
   - Visual confirmation of image loading
   - Clear error messages if something goes wrong

### Usage
1. Click "Upload Character" on the start screen
2. Select a PNG image file
3. The image will be loaded and used as your character
4. If the upload fails, the default character will be used

### Technical Implementation
- Uses `pygame.transform.scale()` for image resizing
- Implements error handling for file operations
- Maintains aspect ratio while fitting game dimensions
- Provides fallback to default character sprite 