import os
from tkinter import Tk, Label, Button
from collections import Counter
from PIL import Image

INPUT_DIR = "input"
OUTPUT_DIR = "output"

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_dominant_color(image):
    image = image.convert('RGB')
    pixels = list(image.getdata())
    return Counter(pixels).most_common(1)[0][0]

def remove_color(image, color_to_remove, tolerance=30):
    image = image.convert("RGBA")
    datas = image.getdata()
    newData = []

    for item in datas:
        r, g, b, a = item
        if abs(r - color_to_remove[0]) < tolerance and \
                abs(g - color_to_remove[1]) < tolerance and \
                abs(b - color_to_remove[2]) < tolerance:
            newData.append((r, g, b, 0))
        else:
            newData.append(item)

    image.putdata(newData)
    return image

def process_images():
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    if not files:
        status.config(text="❌ There are no images in the folder 'input'", fg="red")
        return

    for filename in files:
        path = os.path.join(INPUT_DIR, filename)
        try:
            img = Image.open(path)
            dominant_color = get_dominant_color(img)
            img_no_bg = remove_color(img, dominant_color)

            out_path = os.path.join(OUTPUT_DIR, filename.rsplit('.', 1)[0] + ".png")
            img_no_bg.save(out_path)
            os.remove(path)
        except Exception as e:
            print(f"Ошибка: {filename}: {e}")
            continue

    status.config(text="✅ Ready! Images in 'output/'", fg="green")

# GUI
root = Tk()
root.title("Removing the background")
root.geometry("400x180")
root.resizable(False, False)

Label(root, text="Click the button to remove the background\nall images from the folder 'input'", font=("Segoe UI", 11)).pack(pady=20)
Button(root, text="🚀 Removing the background", command=process_images, font=("Segoe UI", 10)).pack()
status = Label(root, text="", font=("Segoe UI", 9))
status.pack(pady=10)

root.mainloop()
