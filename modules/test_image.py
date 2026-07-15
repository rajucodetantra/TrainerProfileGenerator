from pathlib import Path
from image_handler import ImageHandler

print("=" * 50)
print("Current Working Directory:")
print(Path.cwd())
print("=" * 50)

handler = ImageHandler("data/CTImages")

print("Image Folder:")
print(handler.image_folder)
print("Folder Exists:", handler.image_folder.exists())

if handler.image_folder.exists():
    print("\nFiles in folder:")
    for file in handler.image_folder.iterdir():
        print(file.name)
        break   # Print only the first file

empid = "CT0755"

print("\nSearching for:", empid)

path = handler.get_image_path(empid)

if path:
    print("\n✅ Image Found")
    print(path)
else:
    print("\n❌ Image Not Found")