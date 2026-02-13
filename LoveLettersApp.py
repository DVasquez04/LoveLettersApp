# LoveLettersApp.py
# ----------------------------------
# App de cartas por mood (GUI)
# ----------------------------------

import os
import customtkinter as ctk
from PIL import Image

print("EJECUTANDO LoveLettersApp.py ✅")

# ----------------------------
# Configuración general
# ----------------------------
ctk.set_appearance_mode("light")        # "dark" si quieres
ctk.set_default_color_theme("blue")

APP_TITLE = "Love Letters ❤️"
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")


def load_icon(filename, size=(80, 80)):
    path = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(path):
        return None
    img = Image.open(path).convert("RGBA")
    return ctk.CTkImage(light_image=img, dark_image=img, size=size)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Ventana principal
        self.title(APP_TITLE)
        self.geometry("980x560")
        self.minsize(900, 520)

        # Layout principal
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main()

    # ----------------------------
    # Sidebar (izquierda)
    # ----------------------------
    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_rowconfigure(9, weight=1)

        self.sidebar.configure(fg_color="#8b0f14")  # rojo oscuro

        title = ctk.CTkLabel(
            self.sidebar,
            text="Love App",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="white"
        )
        title.grid(row=0, column=0, padx=18, pady=(18, 6), sticky="w")

        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Cartas por mood",
            font=ctk.CTkFont(size=13),
            text_color="white"
        )
        subtitle.grid(row=1, column=0, padx=18, pady=(0, 18), sticky="w")

        self._sidebar_button("Home", 2)
        self._sidebar_button("Moods", 3)
        self._sidebar_button("Favoritos", 4)
        self._sidebar_button("Historial", 5)

        self._sidebar_button("About", 10)

    def _sidebar_button(self, text, row):
        btn = ctk.CTkButton(
            self.sidebar,
            text=f" {text}",
            anchor="w",
            fg_color="#8b0f14",
            hover_color="#a5151b",
            text_color="white",
            command=lambda t=text: self.set_section(t)
        )
        btn.grid(row=row, column=0, padx=14, pady=6, sticky="ew")

    # ----------------------------
    # Área principal
    # ----------------------------
    def _build_main(self):
        self.main = ctk.CTkFrame(self, corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)

        # Top bar
        self.topbar = ctk.CTkFrame(
            self.main,
            height=54,
            corner_radius=0,
            fg_color="#f39c12"  # naranja
        )
        self.topbar.grid(row=0, column=0, sticky="new")

        self.section_label = ctk.CTkLabel(
            self.topbar,
            text="Home",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        )
        self.section_label.pack(side="left", padx=18, pady=14)

        # Contenido
        self.content = ctk.CTkFrame(self.main, fg_color="transparent")
        self.content.grid(row=1, column=0, sticky="nsew", padx=18, pady=18)
        self.content.grid_columnconfigure((0, 1, 2), weight=1)
        self.content.grid_rowconfigure((0, 1), weight=1)

        moods = [
            "Triste",
            "Ansiosa",
            "Enamorada",
            "Cansada",
            "Feliz",
            "Extrañándome"
        ]

        for i, mood in enumerate(moods):
            self._create_card(self.content, i // 3, i % 3, mood)

        # Status
        self.status = ctk.CTkLabel(
            self.main,
            text="Cartas restantes hoy: 2",
            font=ctk.CTkFont(size=13)
        )
        self.status.grid(row=2, column=0, sticky="se", padx=18, pady=(0, 14))

    def _create_card(self, parent, row, col, title):
        frame = ctk.CTkFrame(parent, corner_radius=14)
        frame.grid(row=row, column=col, padx=14, pady=14, sticky="nsew")

        placeholder = ctk.CTkFrame(
            frame, width=92, height=92, corner_radius=10, fg_color="#d9d9d9"
        )
        placeholder.pack(pady=(18, 10))
        placeholder.pack_propagate(False)

        lbl = ctk.CTkLabel(
            frame, text=title, font=ctk.CTkFont(size=15, weight="bold")
        )
        lbl.pack(pady=(0, 12))

        btn = ctk.CTkButton(
            frame,
            text="Abrir carta",
            command=lambda t=title: self.open_letter(t)
        )
        btn.pack(pady=(0, 16), padx=16, fill="x")

    # ----------------------------
    # Acciones
    # ----------------------------
    def set_section(self, name):
        self.section_label.configure(text=name)

    def open_letter(self, mood):
        self.section_label.configure(text=f"Mood: {mood}")
        self.status.configure(text=f"Abriste una carta para: {mood} ❤️")


# ----------------------------
# Punto de entrada
# ----------------------------
if __name__ == "__main__":
    app = App()
    app.mainloop()
