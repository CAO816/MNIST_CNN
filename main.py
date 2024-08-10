import tkinter as tk
from tkinter import *
import numpy as np
from PIL import ImageGrab, Image, ImageOps
import tensorflow as tf

# Load the CNN model
model = tf.keras.models.load_model('model.h5')

def predict_digit(img):
    # Resize the image to 28x28 pixels (MNIST size)
    img = img.resize((28, 28))
    img = img.convert('L')  # Convert to grayscale
    img = np.array(img)
    img = (255-img)/255.0
    img = img.reshape(1, 28, 28, 1)
    
    # Predict the digit
    res = model.predict([img])[0]
    return np.argmax(res), max(res)

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.x = self.y = 0

        # Create elements
        self.canvas = tk.Canvas(self, width=300, height=300, bg='white', cursor='cross')
        self.label = tk.Label(self, text="Thinking..", font=("Helvetica", 48))
        self.classify_btn = tk.Button(self, text="Recognize", command=self.classify_handwriting)
        self.button_clear = tk.Button(self, text="Clear", command=self.clear_canvas)

        # Grid structure
        self.canvas.grid(row=0, column=0, pady=2, sticky=W)
        self.label.grid(row=0, column=1, pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)

        # Canvas binding
        self.canvas.bind("<B1-Motion>", self.paint)

    def clear_canvas(self):
        self.canvas.delete("all")

    def paint(self, event):
        self.x = event.x
        self.y = event.y
        r = 4
        self.canvas.create_rectangle(self.x - r, self.y - r, self.x + r, self.y + r, fill='black')

    def classify_handwriting(self):
        # Capture the canvas as an image
        x = self.winfo_rootx() + self.canvas.winfo_x() + 80
        y = self.winfo_rooty() + self.canvas.winfo_y() + 80
        x1 = x + self.canvas.winfo_width() + 100
        y1 = y + self.canvas.winfo_height() + 100

        img = ImageGrab.grab().crop((x, y, x1, y1))

        # Predict the digit
        digit, acc = predict_digit(img)
        self.label.configure(text=str(digit) + ', ' + str(int(acc*100)) + '%')

# Create the main window
app = App()
app.mainloop()
