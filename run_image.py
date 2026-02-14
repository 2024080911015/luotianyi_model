#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, "src")

try:
    from desktop_pet_image import DesktopPetImage

    print("Starting Luotianyi Desktop Pet (Image Version)...")
    print("Press ESC to exit")

    pet = DesktopPetImage(use_animation=False)
    pet.run()

except Exception as e:
    print(f"Failed to start: {e}")
    print("Please check:")
    print("1. All dependencies installed")
    print("2. Run as administrator")
    print("3. Image format correct")
    input("Press Enter to exit...")
