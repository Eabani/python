import pyautogui
import pytesseract
import tkinter as tk
import pyperclip

# Configure the path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ScreenCaptureApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main tkinter window
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.screenshot = None

    def select_area(self):
        self.root.deiconify()  # Show the main tkinter window
        self.root.attributes("-alpha", 0.3)  # Make the window semi-transparent
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Button-1>", self.on_button_press)
        self.root.bind("<B1-Motion>", self.on_move_press)
        self.root.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.root.mainloop()

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_move_press(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        self.end_x, self.end_y = (event.x, event.y)
        self.root.destroy()
        self.capture_screen()

    def capture_screen(self):
        x1 = min(self.start_x, self.end_x)
        y1 = min(self.start_y, self.end_y)
        x2 = max(self.start_x, self.end_x)
        y2 = max(self.start_y, self.end_y)
        width = x2 - x1
        height = y2 - y1
        self.screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
        self.screenshot.save("selected_area.png")
        self.extract_text_from_image()

    def extract_text_from_image(self):
        text = pytesseract.image_to_string(self.screenshot)
        pyperclip.copy(text)
        print("Extracted Text:")
        print(text)

if __name__ == "__main__":
    app = ScreenCaptureApp()
    app.select_area()
