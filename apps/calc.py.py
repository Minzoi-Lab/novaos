import tkinter as tk
import math, array, os, pygame
from PIL import Image, ImageTk, ImageDraw

class GlassmorphicCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Glassmorphic Audio Calculator")
        self.root.geometry("380x640")
        self.root.resizable(False, False)
        self.root.configure(bg="#e4e9f2") 
        self.logo_image = None
        self.is_muted = False
        pygame.mixer.init(frequency=22050, size=-16, channels=1)
        self.init_click_sound()

        self.canvas = tk.Canvas(root, bg="#e4e9f2", borderwidth=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.expression = ""
        self.equation_text = "0"

        self.GLASS_WHITE, self.GLASS_WHITE_HOVER = "#f3f6fa", "#e5edf7"
        self.GLASS_GRAY, self.GLASS_GRAY_HOVER = "#e1e6ee", "#d2dae6"
        self.GLASS_ORANGE, self.GLASS_ORANGE_HOVER = "#ffa61a", "#f0960f"
        self.TEXT_DARK, self.TEXT_LIGHT = "#2d3436", "#ffffff"

        self.draw_ambient_background()
        self.draw_calculator_card()
        self.load_large_blender_logo()
        self.create_buttons()
        self.update_display()

    def add_rounded_corners_to_image(self, pil_img, radius):
        """Applies smooth rounded corners directly onto the Blender PNG asset."""
        mask = Image.new("L", pil_img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0) + pil_img.size, radius, fill=255)
        rounded_img = pil_img.copy()
        rounded_img.putalpha(mask)
        return rounded_img

    def load_large_blender_logo(self):
        downloads_dir = os.path.join(os.environ.get("USERPROFILE", ""), "Downloads")
        ico_file = os.path.join(downloads_dir, "calculator_icon.ico")
        found_file = None
        if os.path.exists(downloads_dir):
            for file in os.listdir(downloads_dir):
                if "image_xt2zgo" in file.lower():
                    found_file = os.path.join(downloads_dir, file)
                    break
        if found_file and os.path.exists(found_file):
            try:
                # 1. Standard application header icon shortcut assignment
                img_ico = Image.open(found_file)
                img_ico.save(ico_file, format='ICO', sizes=[(32, 32)])
                self.root.iconbitmap(ico_file)
                
                # 2. Open, resize, and add rounded corners for the layout frame
                img_logo = Image.open(found_file).convert("RGBA")
                img_logo = img_logo.resize((60, 60), Image.Resampling.LANCZOS) # Resized slightly to look cleaner as a header logo
                img_logo = self.add_rounded_corners_to_image(img_logo, radius=12)
                
                self.logo_image = ImageTk.PhotoImage(img_logo)
                # Position coordinates targeted to the Top-Left corner layout area
                self.canvas.create_image(65, 65, image=self.logo_image)
                
                # 3. Add the "Mcalculator" text directly after the rounded image layout
                self.canvas.create_text(110, 65, text="Mcalculator", fill=self.TEXT_DARK, font=("Arial", 18, "bold"), anchor="w")
            except Exception as e:
                print(f"Logo Err: {e}")

    def init_click_sound(self):
        sr = 22050
        num_samples = int(0.04 * sr)
        buf = array.array('h', [int(16000 * math.sin(2 * math.pi * 1200 * i / sr) * (1 - i / num_samples)) for i in range(num_samples)])
        self.click_sound = pygame.mixer.Sound(buffer=buf)

    def draw_ambient_background(self):
        self.canvas.create_oval(220, -50, 420, 150, outline="#ff9f0a", width=6)
        self.canvas.create_oval(-30, 450, 120, 600, outline="#ffb03a", width=3)

    def draw_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        p = [x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1]
        return self.canvas.create_polygon(p, smooth=True, **kwargs)

    def draw_calculator_card(self):
        self.draw_rounded_rect(20, 20, 360, 620, 35, fill="#f8fafc", outline="#ffffff", width=2)
        self.canvas.create_oval(315, 45, 335, 65, fill="#e1e6ee", outline="", tags="mute_bg")
        self.canvas.create_text(325, 54, text="🔈", fill="#7f8c8d", font=("Arial", 11), tags="mute_icon")
        self.canvas.tag_bind("mute_bg", "<Button-1>", lambda e: self.toggle_mute())
        self.canvas.tag_bind("mute_icon", "<Button-1>", lambda e: self.toggle_mute())

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        if self.is_muted:
            self.canvas.create_line(318, 48, 332, 62, fill="#ff3b30", width=2, tags="mute_line")
        else:
            self.canvas.delete("mute_line")
            self.click_sound.play()

    def create_buttons(self):
        layout = [
            ('C', 0, 0, 1, self.GLASS_GRAY, self.TEXT_DARK, self.GLASS_GRAY_HOVER),
            ('+/-', 0, 1, 1, self.GLASS_GRAY, self.TEXT_DARK, self.GLASS_GRAY_HOVER),
            ('%', 0, 2, 1, self.GLASS_GRAY, self.TEXT_DARK, self.GLASS_GRAY_HOVER),
            ('/', 0, 3, 1, self.GLASS_ORANGE, self.TEXT_LIGHT, self.GLASS_ORANGE_HOVER),
            ('7', 1, 0, 1, self.GLASS_WHITE, self.TEXT_DARK, self.GLASS_WHITE_HOVER),
            ('7', 1, 0, 1, self.GLASS_WHITE, self.TEXT_DARK, self.GLASS_WHITE_HOVER),
            ('8', 1, 1, 1, self.GLASS_WHITE, self.TEXT_DARK, self.GLASS_WHITE_HOVER),
            ('9', 1, 2, 1, self.GLASS_WHITE, self.TEXT_DARK, self.GLASS_WHITE_HOVER),
            ('*', 1, 3, 1, self.GLASS_ORANGE, self.TEXT_LIGHT, self.GLASS_ORANGE_HOVER),
            ('4', 2, 0, 1, self.GLASS_WHITE, self.TEXT_DARK, self.GLASS_WHITE_HOVER),
            ('5', 2, 1, 1, self.GLASS_WHITE, self.TEXT_DARK, self.GLASS_WHITE_HOVER),
            ('6', 2, 2, 1, self.GLASS_WHITE, self.TEXT_DARK, self.GLASS_WHITE_HOVER),
            ('-', 2, 3, 1, self.GLASS_ORANGE, self.TEXT_LIGHT, self.GLASS_ORANGE_HOVER),
            ('1', 3, 0, 1, self.GLASS_WHITE, self.TEXT_DARK, self.GLASS_WHITE_HOVER),
            ('2', 3, 1, 1, self.GLASS_WHITE, self.TEXT_DARK, self.GLASS_WHITE_HOVER),
            ('3', 3, 2, 1, self.GLASS_WHITE, self.TEXT_DARK, self.GLASS_WHITE_HOVER),
            ('+', 3, 3, 1, self.GLASS_ORANGE, self.TEXT_LIGHT, self.GLASS_ORANGE_HOVER),
            ('0', 4, 0, 2, self.GLASS_WHITE, self.TEXT_DARK, self.GLASS_WHITE_HOVER),
            ('.', 4, 2, 1, self.GLASS_WHITE, self.TEXT_DARK, self.GLASS_WHITE_HOVER),
            ('=', 4, 3, 1, self.GLASS_ORANGE, self.TEXT_LIGHT, self.GLASS_ORANGE_HOVER)
        ]
        start_x, start_y, btn_w, btn_h, gap = 42, 230, 66, 66, 14
        for text, row, col, span, bg, fg, h_bg in layout:
            x1 = start_x + col * (btn_w + gap)
            y1 = start_y + row * (btn_h + gap)
            x2 = x1 + btn_w if span == 1 else x1 + (btn_w * 2) + gap
            y2 = y1 + btn_h
            t = f"btn_{row}_{col}"
            self.draw_rounded_rect(x1, y1, x2, y2, 22, fill=bg, outline="#ffffff" if bg != self.GLASS_ORANGE else "", width=1, tags=(t, "button"))
            self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=text, fill=fg, font=("Arial", 18, "bold"), tags=(t, "text"))
            self.canvas.tag_bind(t, "<Enter>", lambda e, tag=t, h=h_bg: self.canvas.itemconfig(f"{tag} && button", fill=h))
            self.canvas.tag_bind(t, "<Leave>", lambda e, tag=t, b=bg: self.canvas.itemconfig(f"{tag} && button", fill=b))
            self.canvas.tag_bind(t, "<Button-1>", lambda e, txt=text: self.on_click(txt))

    def update_display(self):
        self.canvas.delete("display")
        self.canvas.create_text(335, 175, text=self.equation_text, fill=self.TEXT_DARK, font=("Arial", 38), anchor="e", tags="display")
        prev = self.expression.replace('*', '×').replace('/', '÷') if self.expression else ""
        self.canvas.create_text(335, 125, text=prev, fill="#7f8c8d", font=("Arial", 16), anchor="e", tags="display")

    def on_click(self, text):
        if not self.is_muted: self.click_sound.play()
        if text == 'C':
            self.expression, self.equation_text = "", "0"
        elif text == '=':
            try:
                self.equation_text = str(eval(self.expression))
                self.expression = self.equation_text
            except:
                self.expression, self.equation_text = "", "Error"
        elif text == '+/-':
            if self.expression:
                self.expression = self.expression[1:] if self.expression.startswith('-') else '-' + self.expression
                self.equation_text = self.expression
        elif text == '%':
            try:
                self.equation_text = str(eval(self.expression) / 100)
                self.expression = self.equation_text
            except:
                self.expression, self.equation_text = "", "Error"
        else:
            if self.equation_text in ["0", "Error"] and text not in ['+', '-', '*', '/', '.']: self.equation_text = ""
            self.expression += text
            self.equation_text = self.expression.split('*')[-1].split('/')[-1].split('+')[-1].split('-')[-1]
            if not self.equation_text: self.equation_text = text
        self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = GlassmorphicCalculator(root)
    root.mainloop()
