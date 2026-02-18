# --- אזור כפתורי הניווט (מרכוז והחלפה) ---
        nav_container = tk.Frame(self.root)
        nav_container.pack(side="bottom", fill="x", pady=20)
        
        # פריים פנימי למרכוז הכפתורים
        center_nav = tk.Frame(nav_container)def setup_navigation(self):
        # יצירת קונטיינר תחתון
        nav_container = tk.Frame(self.root)
        nav_container.pack(side="bottom", fill="x", pady=20)
        
        # פריים פנימי למרכוז הכפתורים
        center_nav = tk.Frame(nav_container)
        center_nav.pack(expand=True)

        # כפתור 'הקודם' - בצד שמאל
        self.btn_prev = tk.Button(center_nav, text="< הקודם", width=12, command=self.handle_prev)
        self.btn_prev.pack(side="left", padx=20)

        # כפתור 'הבא' - בצד ימין
        self.btn_next = tk.Button(center_nav, text="הבא >", width=12, command=self.handle_next)
        self.btn_next.pack(side="left", padx=20)
        center_nav.pack(expand=True)

        # כפתור 'הקודם' - עובר לצד שמאל (מבחינת סדר ה-pack)
        self.btn_prev = tk.Button(center_nav, text="< הקודם", width=12, command=self.handle_prev)
        self.btn_prev.pack(side="left", padx=20)

        # כפתור 'הבא' - עובר לצד ימין
        self.btn_next = tk.Button(center_nav, text="הבא >", width=12, command=self.handle_next)
        self.btn_next.pack(side="left", padx=20)
