"""
Analyze PNG report images to understand the structure
"""
from PIL import Image
import os

def analyze_images():
    output_dir = "outputsample"
    
    png_files = [
        "1.png",
        "2-1.png", 
        "2-2.png",
        "3.png",
        "4-1.png",
        "4-2.png",
        "4-3.png"
    ]
    
    print("=" * 80)
    print("ANALYZING REPORT IMAGES")
    print("=" * 80)
    print()
    
    for png_file in png_files:
        filepath = os.path.join(output_dir, png_file)
        if os.path.exists(filepath):
            try:
                img = Image.open(filepath)
                print(f"📄 {png_file}")
                print(f"   Size: {img.size[0]} x {img.size[1]} pixels")
                print(f"   Mode: {img.mode}")
                print(f"   Format: {img.format}")
                
                # Try to extract text if possible (basic OCR would be needed)
                print(f"   Description: ", end="")
                
                if png_file == "1.png":
                    print("Page 1 - Cover/Title Page")
                elif png_file.startswith("2-"):
                    print("Page 2 - Subject Property & Comparables")
                elif png_file == "3.png":
                    print("Page 3 - Analysis/Details")
                elif png_file.startswith("4-"):
                    print("Page 4 - Additional Information")
                else:
                    print("Unknown section")
                
                print()
            except Exception as e:
                print(f"   Error: {e}")
                print()
    
    print("=" * 80)
    print("REPORT STRUCTURE INFERENCE:")
    print("=" * 80)
    print()
    print("Based on file names, the report appears to have:")
    print("1. Page 1: Cover page (1.png)")
    print("2. Page 2: Two sections (2-1.png, 2-2.png)")
    print("3. Page 3: Single section (3.png)")
    print("4. Page 4: Three sections (4-1.png, 4-2.png, 4-3.png)")
    print()
    print("Total: 4 pages with 7 distinct sections")

if __name__ == '__main__':
    analyze_images()
