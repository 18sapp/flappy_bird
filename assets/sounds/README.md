# Sound Effects Guide

## How to Add Sound Effects

1. **Place your sound file** in this directory (`assets/sounds/`)
2. **Name it `coin.wav`** (or update the path in `game/constants.py`)
3. **Supported formats:**
   - **WAV** (recommended - best compatibility)
   - **OGG** (good compression)
   - **MP3** (may require additional setup)

## File Requirements

- **Format:** WAV is recommended for best compatibility
- **File name:** `coin.wav` (or update `COIN_SOUND_PATH` in `game/constants.py`)
- **Location:** `assets/sounds/coin.wav`

## Example

Place your sound file as:
```
assets/sounds/coin.wav
```

The game will automatically load and play it when you collect a coin!

## Tips

- Keep sound files small (under 1MB recommended)
- Short sounds work best (1-2 seconds)
- WAV format is most reliable across platforms
- If the sound doesn't load, check the console for error messages

## Testing

Run the game and collect a coin - you should hear the sound effect play!

