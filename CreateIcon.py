#!/usr/bin/env python3
"""
Generate a simple icon for the Human Detection Camera app
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Create a 512x512 image with a gradient background
    size = 512
    img = Image.new('RGB', (size, size), color='#2196F3')
    draw = ImageDraw.Draw(img)
    
    # Draw a camera shape
    # Camera body
    camera_color = '#FFFFFF'
    draw.rounded_rectangle(
        [(100, 150), (412, 362)],
        radius=30,
        fill=camera_color,
        outline='#1976D2',
        width=8
    )
    
    # Lens
    lens_center = (256, 256)
    lens_radius = 80
    draw.ellipse(
        [
            (lens_center[0] - lens_radius, lens_center[1] - lens_radius),
            (lens_center[0] + lens_radius, lens_center[1] + lens_radius)
        ],
        fill='#1976D2',
        outline='#0D47A1',
        width=6
    )
    
    # Inner lens
    inner_radius = 50
    draw.ellipse(
        [
            (lens_center[0] - inner_radius, lens_center[1] - inner_radius),
            (lens_center[0] + inner_radius, lens_center[1] + inner_radius)
        ],
        fill='#0D47A1'
    )
    
    # Flash
    draw.ellipse([(350, 180), (390, 220)], fill='#FFC107')
    
    # Human detection indicator (person silhouette in corner)
    # Simple stick figure
    person_x, person_y = 160, 220
    # Head
    draw.ellipse([(person_x-10, person_y-10), (person_x+10, person_y+10)], fill='#4CAF50')
    # Body
    draw.line([(person_x, person_y+10), (person_x, person_y+40)], fill='#4CAF50', width=4)
    # Arms
    draw.line([(person_x-15, person_y+25), (person_x+15, person_y+25)], fill='#4CAF50', width=4)
    # Legs
    draw.line([(person_x, person_y+40), (person_x-10, person_y+60)], fill='#4CAF50', width=4)
    draw.line([(person_x, person_y+40), (person_x+10, person_y+60)], fill='#4CAF50', width=4)
    
    # Save the icon
    img.save('icon.png')
    print("✓ Icon created: icon.png")
    
    # Also create smaller sizes for different contexts
    for size in [256, 128, 64, 48, 32, 16]:
        small = img.resize((size, size), Image.Resampling.LANCZOS)
        small.save(f'icon_{size}.png')
        print(f"✓ Created: icon_{size}.png")

if __name__ == '__main__':
    try:
        create_icon()
    except ImportError:
        print("Error: PIL (Pillow) not installed")
        print("Install with: pip install Pillow")
        print("\nAlternatively, create a 512x512 PNG icon manually")
