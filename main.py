# FILE-ID: C-01
# VERSION-ANCHOR: 1218-G2
# DESCRIPTION: Main UI for Exam System - Navigation Fix (Next on Right) & Active Sidebar

import tkinter as tk
from logic import ExamLogic

class ExamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("מערכת בחינות - C-01")
        self.root.geometry("800x600")
        
        # אתחול הלוגיקה (מזהה עוגן 1218-G2)
        self.logic = ExamLogic()
        
        # בניית הממשק
        self.setup_ui()

    def setup_ui(self):
        # 1. אזור הטיימר (בראש המסך)
        self.timer_label = tk.Label(self.root, text=self.logic.get_time_string(), font=("Arial", 20, "bold"))
        self.timer_label.pack(pady=15)

        # 2. קונטיינר ראשי (תוכן + סיידבר)
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=20)

        # סיידבר ניווט (צד ימין)
        self.sidebar_frame = tk.Frame(self.main_container, width=150, bg="#f8f9fa")
        self.sidebar_frame.pack(side="right", fill="y", padx=10)
        
        # אזור הצגת השאלה (מרכז)
        self.question_frame = tk.Frame(self.main_container, bg="white", relief="groove", bd=2)
        self.question_frame.pack(side="right", fill="both", expand=True)
        
        self.question_text = tk.Label(self.question_frame, text="מוכן להתחיל? לחץ על אחד הכפתורים.", 
                                     font=("Arial", 14), wraplength=500, bg="white")
        self.question_text.pack(pady=100)

        # 3. כפתורי ניווט (תחתית המסך - ממורכזים)
        self.setup_navigation()
        
        # רינדור ראשוני של הסיידבר
        self.update_sidebar()

    def setup_navigation(self):
        """יצירת כפתורי הבא/הקודם כשהם ממורכזים והבא בצד ימין"""
        nav_container = tk.Frame(self.root)
        nav_container.pack(side="bottom", fill="x", pady=20)
        
        center_nav = tk.Frame(nav_container)
        center_nav.pack(expand=True)

        # כפתור 'הקודם' - בצד שמאל (נארז ראשון)
        self.btn_prev = tk.Button(center_nav, text="< הקודם", width=15, height=2, 
                                 command=self.handle_prev, bg="#e0e0e0")
        self.btn_prev.pack(side="left", padx=20)

        # כפתור 'הבא' - בצד ימין (נארז
