# Bird Image Guide

## How to Add a Custom Bird Image

1. **Place your bird image** in this directory (`assets/images/`)
2. **Name it `bird.png`** (or update the path in `game/constants.py`)
3. **Supported formats:**
   - PNG (recommended - supports transparency)
   - JPG/JPEG
   - GIF
   - BMP

## Image Requirements

- **Recommended size:** 40x30 pixels (or similar aspect ratio)
- The image will be automatically scaled to fit the bird size defined in `game/constants.py`
- **Transparency:** PNG format with alpha channel is recommended for best results
- **Orientation:** The bird should face right (or you can rotate it in the code if needed)

## Tips

- Use PNG format for best quality and transparency support
- Keep the image size reasonable (under 100KB recommended)
- The image will be scaled to `BIRD_WIDTH` x `BIRD_HEIGHT` (currently 40x30 pixels)
- If the image doesn't load, the game will fall back to the default drawn bird

## Example

Place your image file as:
```
assets/images/bird.png
```

The game will automatically load it when you run it!

