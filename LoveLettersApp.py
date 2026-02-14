# LoveLettersApp.py
# ----------------------------------
# App de cartas por mood (GUI)
# ----------------------------------

import os
import random
import customtkinter as ctk
from PIL import Image

print("EJECUTANDO LoveLettersApp.py ✅")

# ----------------------------
# Configuración general
# ----------------------------
ctk.set_appearance_mode("dark")        # modo oscuro para fondo más agradable
ctk.set_default_color_theme("blue")

APP_TITLE = "Love Letters ❤️"
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
# Detectar carpeta de cartas en minúsculas o mayúsculas
LETTERS_DIR = os.path.join(BASE_DIR, "letters")
if not os.path.isdir(LETTERS_DIR):
    _letters_alt = os.path.join(BASE_DIR, "Letters")
    if os.path.isdir(_letters_alt):
        LETTERS_DIR = _letters_alt
FAVORITES_FILE = os.path.join(BASE_DIR, "Favoritas.txt")

# Mapeo de nombre de mood -> nombre de carpeta
MOOD_DIR_MAP = {
    "Feliz": "Feliz",
    "Triste": "Triste",
    "Ansiosa": "Ansiosa",
    "Enamorada": "Enamorada",
    "Cansada": "Cansada",
    "Extrañándome": "Extrañandome",
    "Extrañandome": "Extrañandome",
}

# Cartas de ejemplo (fallback si no hay archivos en /letters/<mood>/)
DEFAULT_LETTERS = {
    "Feliz": [
        "Hoy me siento inmensamente feliz por tenerte en mi vida.",
        "Tu sonrisa ilumina cualquier día, gracias por existir."
    ],
    "Triste": [
        "Cuando te sientas triste, recuerda que aquí estoy contigo.",
        "Aun en los días grises, mi amor por ti es sol."
    ],
    "Ansiosa": [
        "Respira profundo; paso a paso, todo estará bien.",
        "Te abrazo con calma, mi corazón late despacio contigo."
    ],
    "Enamorada": [
        "Estoy perdidamente enamorado de ti, hoy y siempre.",
        "Cada detalle tuyo me enamora un poco más."
    ],
    "Cansada": [
        "Descansa, te lo mereces. Yo cuido el mundo por ti hoy.",
        "Cerrar los ojos y sentir mi abrazo: tu refugio."
    ],
    "Extrañandome": [
        "Aunque no esté cerca, mi amor te acompaña.",
        "Piensa en nosotros: el tiempo pasa, el cariño crece."
    ],
    "Extrañándome": [
        "Aunque no esté cerca, mi amor te acompaña.",
        "Piensa en nosotros: el tiempo pasa, el cariño crece."
    ],
}

# Colores de acento por mood (usados en UI)
MOOD_ACCENT_COLORS = {
    "Feliz": "#1f4d1f",          # verde oscuro
    "Triste": "#1f3b5b",         # azul profundo
    "Ansiosa": "#4d3a1f",        # ámbar oscuro
    "Enamorada": "#4d1f2f",      # burdeos oscuro
    "Cansada": "#2f2f2f",        # gris oscuro
    "Extrañándome": "#2f1f4d",   # morado oscuro
    "Extrañandome": "#2f1f4d"    # variante sin acento
}


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
        self.moods_frame = None
        self.favorites_frame = None
        self.favorites_list = None
        self.about_frame = None
        self.letters_cache = {}
        self._last_letter_index = {}
        self.favorites = []
        # Cerrar guardando favoritos
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        # Cargar favoritos desde archivo (si existe)
        self._load_favorites_from_file()


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
        self.main = ctk.CTkFrame(self, corner_radius=0, fg_color="#1e1e1e")
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
        # Centrado vertical: filas vacías arriba y abajo
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_rowconfigure(2, weight=1)

        # Introducción para Home
        intro_text = (
            "Bienvenida a tu App de Letras de Amor <3\n"
            "Siéntete bienvenida de abrir esta app cada que te sientas Feliz/Mal/Triste y muchos moods más.\n"
            "Espero te guste <3<3<3"
        )
        self.intro_label = ctk.CTkLabel(
            self.content,
            text=intro_text,
            font=ctk.CTkFont(size=16),
            justify="center",
            wraplength=720
        )
        # Posicionar el texto en la fila central para centrar verticalmente
        self.intro_label.grid(row=1, column=0, columnspan=3, padx=4, pady=(0, 10))

        # Status
        self.status = ctk.CTkLabel(
            self.main,
            text="Welcome <3",
            font=ctk.CTkFont(size=13)
        )
        self.status.grid(row=2, column=0, sticky="sw", padx=18, pady=(0, 14))

    def _tint(self, hex_color, factor=1.15):
        try:
            c = hex_color.lstrip('#')
            r = int(c[0:2], 16)
            g = int(c[2:4], 16)
            b = int(c[4:6], 16)
            r = max(0, min(255, int(r * factor)))
            g = max(0, min(255, int(g * factor)))
            b = max(0, min(255, int(b * factor)))
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            return hex_color

    # (Se removió la lógica de fondos para simplificar la app)

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

    def _ensure_moods_section(self):
        if self.moods_frame is not None:
            return
        self.moods_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.moods_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=8, pady=8)
        # Configurar grid 3x2 dentro de la sección de moods
        self.moods_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.moods_frame.grid_rowconfigure((0, 1), weight=1)
        # Fondo removido

        moods = [
            "Feliz",
            "Triste",
            "Ansiosa",
            "Enamorada",
            "Cansada",
            "Extrañandome"
        ]

        mood_symbols = {
            "Feliz": "😄",
            "Triste": "😢",
            "Ansiosa": "😰",
            "Enamorada": "❤️",
            "Cansada": "😴",
            "Extrañándome": "🥺",
            "Extrañandome": "🥺"
        }

        for i, mood in enumerate(moods):
            r, c = divmod(i, 3)  # 2 filas (0-1), 3 columnas (0-2)
            block = ctk.CTkFrame(
                self.moods_frame,
                corner_radius=10,
                fg_color=MOOD_ACCENT_COLORS.get(mood, "#2b2b2b")
            )
            block.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")

            # Símbolo relacionado al mood encima del nombre
            symbol = mood_symbols.get(mood, "💌")
            symbol_lbl = ctk.CTkLabel(block, text=symbol, font=ctk.CTkFont(size=28), text_color="white")
            symbol_lbl.pack(padx=12, pady=(14, 6))

            lbl = ctk.CTkLabel(block, text=mood, font=ctk.CTkFont(size=16, weight="bold"), text_color="white")
            lbl.pack(padx=12, pady=(0, 8))

            btn = ctk.CTkButton(block, text="Revelar Carta", command=lambda m=mood: self.open_letter(m))
            btn.pack(padx=12, pady=(0, 12), fill="x")

    def _ensure_favorites_section(self):
        if self.favorites_frame is not None:
            return
        # Contenedor de favoritos
        self.favorites_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.favorites_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=8, pady=8)
        self.favorites_frame.grid_columnconfigure(0, weight=1)
        self.favorites_frame.grid_rowconfigure(0, weight=1)
        # Fondo removido

        # Lista desplazable de favoritos
        self.favorites_list = ctk.CTkScrollableFrame(self.favorites_frame, corner_radius=10)
        self.favorites_list.grid(row=0, column=0, sticky="nsew")

        self._refresh_favorites_ui()

    def _refresh_favorites_ui(self):
        # Limpiar lista y rellenar
        if self.favorites_list is None:
            return
        for w in self.favorites_list.winfo_children():
            w.destroy()
        # Mostrar mensaje cuando no hay favoritos
        if not self.favorites:
            placeholder = ctk.CTkLabel(
                self.favorites_list,
                text="Marca una carta como favoritos y miralas aca despues <3",
                font=ctk.CTkFont(size=15),
                justify="center",
                wraplength=620,
                text_color="white"
            )
            # Centrar verticalmente dentro del área disponible
            placeholder.pack(expand=True, padx=12, pady=16)
            return
        for fav in self.favorites:
            row = ctk.CTkFrame(self.favorites_list, corner_radius=8)
            row.pack(fill="x", padx=8, pady=6)
            # Sobre grande sin rectángulo de fondo
            icon = ctk.CTkLabel(row, text="✉️", font=ctk.CTkFont(size=40))
            icon.pack(side="left", padx=(10, 8), pady=8)
            # Abrir la carta guardada al hacer clic en el símbolo
            icon.bind("<Button-1>", lambda e, fav=fav: self._open_favorite(fav))
            # Mostrar cursor de mano al pasar sobre el símbolo
            icon.bind("<Enter>", lambda e, w=icon: w.configure(cursor="hand2"))
            icon.bind("<Leave>", lambda e, w=icon: w.configure(cursor=""))
            mood_lbl = ctk.CTkLabel(row, text=fav['mood'], font=ctk.CTkFont(size=16, weight="bold"))
            mood_lbl.pack(side="left", padx=4, pady=8)
            # Eliminar favorito
            del_btn = ctk.CTkButton(row, text="Eliminar", command=lambda f=fav: self._remove_favorite(f))
            del_btn.pack(side="right", padx=8, pady=8)

    def _ensure_about_section(self):
        if self.about_frame is not None:
            return
        # Contenedor de About
        self.about_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.about_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=8, pady=8)
        # Centrado vertical dentro del frame (spacers arriba/abajo)
        self.about_frame.grid_columnconfigure(0, weight=1)
        self.about_frame.grid_rowconfigure(0, weight=1)
        self.about_frame.grid_rowconfigure(2, weight=1)
        # Fondo removido

        about_text = "Hecho con mucho amor, espero te guste <3"
        lbl = ctk.CTkLabel(
            self.about_frame,
            text=about_text,
            font=ctk.CTkFont(size=16),
            justify="center",
            wraplength=720
        )
        lbl.grid(row=1, column=0, padx=4, pady=(0, 10))

    def _open_favorite(self, fav):
        mood = fav.get('mood')
        index = fav.get('index')
        letters = self.get_letters(mood)
        if letters and isinstance(index, int) and 0 <= index < len(letters):
            text = letters[index]
        else:
            text = fav.get('text') or "(Carta no disponible)"

        popup = ctk.CTkToplevel(self)
        popup.title(f"Favorito - {mood}")
        # Quitar barra de control para que solo se cierre con el botón
        try:
            popup.overrideredirect(True)
            popup.protocol("WM_DELETE_WINDOW", lambda: None)
        except Exception:
            pass
        self._center_window(popup, 520, 360)
        try:
            popup.attributes("-topmost", True)
        except Exception:
            pass
        popup.lift()
        popup.focus_force()

        title_lbl = ctk.CTkLabel(popup, text=f"Mood: {mood}", font=ctk.CTkFont(size=18, weight="bold"))
        title_lbl.pack(padx=16, pady=(16, 8))

        body = ctk.CTkTextbox(popup, width=480, height=220)
        body.pack(padx=16, pady=8, fill="both")
        body.insert("1.0", text)
        body.configure(state="disabled")

        close_btn = ctk.CTkButton(popup, text="Cerrar", command=popup.destroy)
        close_btn.pack(padx=16, pady=(8, 16))

    # ----------------------------
    # Acciones
    # ----------------------------
    def set_section(self, name):
        self.section_label.configure(text=name)
        # Mostrar/Ocultar introducción según sección
        if name == "Home":
            self.intro_label.grid()
            if self.moods_frame is not None:
                self.moods_frame.grid_remove()
            if self.favorites_frame is not None:
                self.favorites_frame.grid_remove()
            if self.about_frame is not None:
                self.about_frame.grid_remove()
        elif name == "Moods":
            self.intro_label.grid_remove()
            self._ensure_moods_section()
            self.moods_frame.grid()
            if self.favorites_frame is not None:
                self.favorites_frame.grid_remove()
            if self.about_frame is not None:
                self.about_frame.grid_remove()
        elif name == "Favoritos":
            self.intro_label.grid_remove()
            if self.moods_frame is not None:
                self.moods_frame.grid_remove()
            self._ensure_favorites_section()
            self.favorites_frame.grid()
            if self.about_frame is not None:
                self.about_frame.grid_remove()
        elif name == "About":
            self.intro_label.grid_remove()
            if self.moods_frame is not None:
                self.moods_frame.grid_remove()
            if self.favorites_frame is not None:
                self.favorites_frame.grid_remove()
            self._ensure_about_section()
            self.about_frame.grid()
        else:
            self.intro_label.grid_remove()
            if self.moods_frame is not None:
                self.moods_frame.grid_remove()
            if self.favorites_frame is not None:
                self.favorites_frame.grid_remove()
            if self.about_frame is not None:
                self.about_frame.grid_remove()

    def open_letter(self, mood):
        self.section_label.configure(text=f"Mood: {mood}")
        self.intro_label.grid_remove()
        self.status.configure(text=f"Abriste una carta para: {mood} ❤️")

        # Obtener cartas desde carpeta /letters/<mood>/ o fallback
        letters = self.get_letters(mood)
        if letters:
            idx = self._pick_letter(mood, letters)
            text = letters[idx]
        else:
            idx = None
            text = "Aún no hay cartas para este mood."

        # Mostrar en una ventana modal simple
        popup = ctk.CTkToplevel(self)
        popup.title(f"Carta - {mood}")
        # Quitar barra de control para que solo se cierre con el botón
        try:
            popup.overrideredirect(True)
            popup.protocol("WM_DELETE_WINDOW", lambda: None)
        except Exception:
            pass
        # Centrar el panel respecto a la ventana padre
        self._center_window(popup, 520, 360)
        # Mantener al frente respecto a la ventana padre
        try:
            popup.attributes("-topmost", True)
        except Exception:
            pass
        popup.lift()
        popup.focus_force()

        title_lbl = ctk.CTkLabel(popup, text=f"Mood: {mood}", font=ctk.CTkFont(size=18, weight="bold"))
        title_lbl.pack(padx=16, pady=(16, 8))

        body = ctk.CTkTextbox(popup, width=480, height=220)
        body.pack(padx=16, pady=8, fill="both")
        body.insert("1.0", text)
        body.configure(state="disabled")

        actions = ctk.CTkFrame(popup)
        actions.pack(padx=16, pady=(8, 16), fill="x")
        fav_btn = ctk.CTkButton(actions, text="Agregar a favoritos", command=lambda: self._add_to_favorites(mood, text, idx))
        fav_btn.pack(side="left")
        close_btn = ctk.CTkButton(actions, text="Cerrar", command=popup.destroy)
        close_btn.pack(side="right")

    def _pick_letter(self, mood, letters):
        # Evitar repetir la misma carta consecutivamente para el mismo mood
        last_idx = self._last_letter_index.get(mood)
        n = len(letters)
        if n <= 1:
            idx = 0
        else:
            if last_idx is None or last_idx < 0 or last_idx >= n:
                idx = random.randrange(n)
            else:
                choices = [i for i in range(n) if i != last_idx]
                idx = random.choice(choices)
        self._last_letter_index[mood] = idx
        return idx

    def _center_window(self, win, width, height):
        # Asegurar medidas actualizadas del padre
        self.update_idletasks()
        px = self.winfo_rootx()
        py = self.winfo_rooty()
        pw = self.winfo_width()
        ph = self.winfo_height()

        x = px + (pw - width) // 2
        y = py + (ph - height) // 2
        win.geometry(f"{width}x{height}+{x}+{y}")

    def _add_to_favorites(self, mood, text, index):
        # Evitar duplicados exactos
        exists = any(f['mood'] == mood and f['text'] == text for f in self.favorites)
        if not exists:
            self.favorites.append({'mood': mood, 'text': text, 'index': index})
            # Actualizar UI si la pestaña está creada
            if self.favorites_frame is not None:
                self._refresh_favorites_ui()
            # Persistir en archivo
            self._save_favorites_to_file()
        # Feedback ligero
        self.status.configure(text=f"Favorito agregado: {mood} ✉️")

    def _remove_favorite(self, fav):
        try:
            self.favorites.remove(fav)
            self._save_favorites_to_file()
            if self.favorites_frame is not None:
                self._refresh_favorites_ui()
            self.status.configure(text=f"Favorito eliminado: {fav.get('mood','')} 🗑️")
        except ValueError:
            pass

    def get_letters(self, mood):
        # Cachear resultados por rendimiento
        if mood in self.letters_cache:
            return self.letters_cache[mood]

        dir_name = MOOD_DIR_MAP.get(mood, mood)
        mood_dir = os.path.join(LETTERS_DIR, dir_name)
        letters = []

        if os.path.isdir(mood_dir):
            # Ordenar por nombre de archivo con clave homogénea
            # (numérico si aplica; si no, ordena por texto)
            def _key(fname):
                stem = os.path.splitext(fname)[0]
                try:
                    return (0, int(stem))
                except Exception:
                    return (1, stem.lower())
            for fname in sorted(os.listdir(mood_dir), key=_key):
                if fname.lower().endswith(".txt"):
                    fpath = os.path.join(mood_dir, fname)
                    try:
                        with open(fpath, "r", encoding="utf-8") as f:
                            content = f.read().strip()
                            if content:
                                letters.append(content)
                    except Exception:
                        pass

        if not letters:
            letters = DEFAULT_LETTERS.get(mood) or DEFAULT_LETTERS.get(dir_name) or []

        self.letters_cache[mood] = letters
        return letters

    def _save_favorites_to_file(self):
        try:
            with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
                for fav in self.favorites:
                    mood = fav.get('mood')
                    idx = fav.get('index')
                    if mood is None or idx is None:
                        continue
                    f.write(f"{mood}:{idx}\n")
        except Exception:
            pass

    def _load_favorites_from_file(self):
        if not os.path.isfile(FAVORITES_FILE):
            return
        try:
            with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or ":" not in line:
                        continue
                    mood, idx_str = line.split(":", 1)
                    try:
                        idx = int(idx_str)
                    except Exception:
                        idx = None
                    # Recuperar texto si posible
                    letters = self.get_letters(mood)
                    text = None
                    if letters and isinstance(idx, int) and 0 <= idx < len(letters):
                        text = letters[idx]
                    # Evitar duplicados
                    if text is not None and not any(f['mood'] == mood and f['text'] == text for f in self.favorites):
                        self.favorites.append({'mood': mood, 'text': text, 'index': idx})
        except Exception:
            pass

    def _on_close(self):
        # Guardar antes de cerrar
        self._save_favorites_to_file()
        self.destroy()


# ----------------------------
# Punto de entrada
# ----------------------------
if __name__ == "__main__":
    app = App()
    app.mainloop()
