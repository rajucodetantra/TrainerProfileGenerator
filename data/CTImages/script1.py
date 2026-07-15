import os

folder = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(folder):
    if filename.lower().endswith(".jpg"):
        new_name = filename

        # Replace file name prefixes
        new_name = new_name.replace("MR.", "Mr.")
        new_name = new_name.replace("MR ", "Mr. ")
        new_name = new_name.replace("MISS ", "Ms. ")
        new_name = new_name.replace("MISS.", "Ms.")

        if new_name != filename:
            os.rename(
                os.path.join(folder, filename),
                os.path.join(folder, new_name)
            )
            print(f"Renamed: {filename} -> {new_name}")

print("\nDone!")
