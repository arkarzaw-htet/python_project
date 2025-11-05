import tkinter as tk
from tkinter import font

class FlashcardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✨ Flashcard Master")
        self.geometry("600x500")
        self.configure(bg='#f0f2f5')
        
        # Sample data
        self.flashcard = {"What is the capital of France?": "Paris"}
        
        # Fonts
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.body_font = font.Font(family="Helvetica", size=12)
        
        self.create_interface()

    def create_interface(self):
        # Header
        header_frame = tk.Frame(self, bg='#f0f2f5', pady=30)
        header_frame.pack(fill='x')
        
        tk.Label(
            header_frame,
            text="✨ Flashcard Master",
            font=self.title_font,
            fg='#4f46e5',
            bg='#f0f2f5'
        ).pack()
        
        tk.Label(
            header_frame,
            text="Learn smarter, not harder",
            font=self.body_font,
            fg='#6b7280',
            bg='#f0f2f5'
        ).pack(pady=(5, 0))

        # Stats
        stats_frame = tk.Frame(self, bg='white', pady=15)
        stats_frame.pack(fill='x', padx=30, pady=20)
        
        tk.Label(
            stats_frame,
            text=f"📚 Total Flashcards: {len(self.flashcard)}",
            font=font.Font(family="Helvetica", size=16, weight="bold"),
            fg='#1f2937',
            bg='white'
        ).pack()

        # Buttons
        buttons_frame = tk.Frame(self, bg='#f0f2f5', pady=20)
        buttons_frame.pack(fill='both', expand=True, padx=30)

        # Add button
        add_btn = tk.Button(
            buttons_frame,
            text="➕ Add Flashcard",
            font=self.button_font,
            bg='#10b981',
            fg='white',
            relief='flat',
            pady=15,
            command=self.show_add_window
        )
        add_btn.pack(fill='x', pady=5)

        # Edit button
        edit_btn = tk.Button(
            buttons_frame,
            text="✏️ Edit Flashcards",
            font=self.button_font,
            bg='#f59e0b',
            fg='white',
            relief='flat',
            pady=15,
            command=self.show_edit_window
        )
        edit_btn.pack(fill='x', pady=5)

        # Delete button
        delete_btn = tk.Button(
            buttons_frame,
            text="🗑️ Delete Flashcards",
            font=self.button_font,
            bg='#ef4444',
            fg='white',
            relief='flat',
            pady=15,
            command=self.show_delete_window
        )
        delete_btn.pack(fill='x', pady=5)

        # Practice button
        practice_btn = tk.Button(
            buttons_frame,
            text="🎯 Practice Mode",
            font=self.button_font,
            bg='#4f46e5',
            fg='white',
            relief='flat',
            pady=15,
            command=self.show_practice_window
        )
        practice_btn.pack(fill='x', pady=5)

    def show_add_window(self):
        AddWindow(self)

    def show_edit_window(self):
        EditWindow(self)

    def show_delete_window(self):
        DeleteWindow(self)

    def show_practice_window(self):
        PracticeWindow(self)


class AddWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("➕ Add New Flashcard")
        self.geometry("600x500")  # Made taller
        self.configure(bg='#f8fafc')
        
        # Header
        header_frame = tk.Frame(self, bg='#f8fafc')
        header_frame.pack(fill='x', pady=20)
        
        tk.Label(
            header_frame,
            text="➕ Add New Flashcard",
            font=font.Font(family="Helvetica", size=18, weight="bold"),
            fg='#059669',
            bg='#f8fafc'
        ).pack()

        # Form
        form_frame = tk.Frame(self, bg='white', padx=30, pady=30)
        form_frame.pack(fill='both', expand=True, padx=30, pady=20)

        tk.Label(
            form_frame,
            text="Question:",
            font=font.Font(family="Helvetica", size=12, weight="bold"),
            fg='#1f2937',
            bg='white'
        ).pack(anchor='w', pady=(0, 5))

        question_text = tk.Text(form_frame, height=3, font=font.Font(family="Helvetica", size=11))
        question_text.pack(fill='x', pady=(0, 15))
        question_text.insert("1.0", "What is the capital of Spain?")

        tk.Label(
            form_frame,
            text="Answer:",
            font=font.Font(family="Helvetica", size=12, weight="bold"),
            fg='#1f2937',
            bg='white'
        ).pack(anchor='w', pady=(0, 5))

        answer_text = tk.Text(form_frame, height=3, font=font.Font(family="Helvetica", size=11))
        answer_text.pack(fill='x', pady=(0, 20))
        answer_text.insert("1.0", "Madrid")

        # Button in separate frame to ensure visibility
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.pack(fill='x', pady=10)
        
        tk.Button(
            button_frame,
            text="✅ Add Flashcard",
            font=font.Font(family="Helvetica", size=12, weight="bold"),
            bg='#059669',
            fg='white',
            relief='flat',
            pady=15,
            command=self.destroy
        ).pack(fill='x')


class EditWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("✏️ Edit Flashcards")
        self.geometry("700x500")
        self.configure(bg='#f8fafc')
        
        # Header
        tk.Label(
            self,
            text="✏️ Edit Flashcards",
            font=font.Font(family="Helvetica", size=18, weight="bold"),
            fg='#d97706',
            bg='#f8fafc'
        ).pack(pady=30)

        # Content
        content_frame = tk.Frame(self, bg='white', padx=30, pady=30)
        content_frame.pack(fill='both', expand=True, padx=30, pady=20)

        # Left side - List
        left_frame = tk.Frame(content_frame, bg='white')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 20))
        
        tk.Label(
            left_frame,
            text="Select flashcard:",
            font=font.Font(family="Helvetica", size=12, weight="bold"),
            fg='#1f2937',
            bg='white'
        ).pack(anchor='w', pady=(0, 10))

        listbox = tk.Listbox(left_frame, font=font.Font(family="Helvetica", size=10))
        listbox.pack(fill='both', expand=True)
        listbox.insert(0, "What is the capital of France?")

        # Right side - Edit form
        right_frame = tk.Frame(content_frame, bg='white')
        right_frame.pack(side='right', fill='both', expand=True)

        tk.Label(
            right_frame,
            text="Question:",
            font=font.Font(family="Helvetica", size=12, weight="bold"),
            fg='#1f2937',
            bg='white'
        ).pack(anchor='w', pady=(0, 5))

        question_text = tk.Text(right_frame, height=4, font=font.Font(family="Helvetica", size=11))
        question_text.pack(fill='x', pady=(0, 20))
        question_text.insert("1.0", "What is the capital of France?")

        tk.Label(
            right_frame,
            text="Answer:",
            font=font.Font(family="Helvetica", size=12, weight="bold"),
            fg='#1f2937',
            bg='white'
        ).pack(anchor='w', pady=(0, 5))

        answer_text = tk.Text(right_frame, height=4, font=font.Font(family="Helvetica", size=11))
        answer_text.pack(fill='x', pady=(0, 30))
        answer_text.insert("1.0", "Paris")

        tk.Button(
            right_frame,
            text="💾 Save Changes",
            font=font.Font(family="Helvetica", size=12, weight="bold"),
            bg='#d97706',
            fg='white',
            relief='flat',
            pady=12,
            command=self.destroy
        ).pack(fill='x')


class DeleteWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("🗑️ Delete Flashcards")
        self.geometry("500x400")
        self.configure(bg='#f8fafc')
        
        # Header
        tk.Label(
            self,
            text="🗑️ Delete Flashcards",
            font=font.Font(family="Helvetica", size=18, weight="bold"),
            fg='#dc2626',
            bg='#f8fafc'
        ).pack(pady=30)

        # Content
        content_frame = tk.Frame(self, bg='white', padx=30, pady=30)
        content_frame.pack(fill='both', expand=True, padx=30, pady=20)

        listbox = tk.Listbox(content_frame, font=font.Font(family="Helvetica", size=10))
        listbox.pack(fill='both', expand=True, pady=(0, 20))
        listbox.insert(0, "What is the capital of France?")

        tk.Button(
            content_frame,
            text="🗑️ Delete Selected",
            font=font.Font(family="Helvetica", size=12, weight="bold"),
            bg='#dc2626',
            fg='white',
            relief='flat',
            pady=12,
            command=self.destroy
        ).pack(fill='x')


class PracticeWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("🎯 Practice Mode")
        self.geometry("700x500")
        self.configure(bg='#f8fafc')
        
        # Header
        tk.Label(
            self,
            text="🎯 Practice Mode",
            font=font.Font(family="Helvetica", size=20, weight="bold"),
            fg='#4f46e5',
            bg='#f8fafc'
        ).pack(pady=30)

        # Stats
        stats_frame = tk.Frame(self, bg='white', pady=15)
        stats_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        tk.Label(
            stats_frame,
            text="Card 1 of 1",
            font=font.Font(family="Helvetica", size=12),
            fg='#6b7280',
            bg='white'
        ).pack(side='left', padx=20)
        
        tk.Label(
            stats_frame,
            text="Score: 0",
            font=font.Font(family="Helvetica", size=12),
            fg='#059669',
            bg='white'
        ).pack(side='right', padx=20)

        # Card
        card_frame = tk.Frame(self, bg='white', padx=50, pady=50)
        card_frame.pack(fill='both', expand=True, padx=30, pady=20)

        tk.Label(
            card_frame,
            text="❓ What is the capital of France?",
            font=font.Font(family="Helvetica", size=14, weight="bold"),
            fg='#1f2937',
            bg='white'
        ).pack(pady=(0, 30))

        tk.Label(
            card_frame,
            text="💡 Paris",
            font=font.Font(family="Helvetica", size=14),
            fg='#4f46e5',
            bg='white'
        ).pack(pady=(0, 40))

        # Buttons
        tk.Button(
            card_frame,
            text="✅ Got it Right",
            font=font.Font(family="Helvetica", size=12, weight="bold"),
            bg='#059669',
            fg='white',
            relief='flat',
            pady=12,
            command=self.destroy
        ).pack(fill='x', pady=5)

        tk.Button(
            card_frame,
            text="❌ Got it Wrong",
            font=font.Font(family="Helvetica", size=12, weight="bold"),
            bg='#dc2626',
            fg='white',
            relief='flat',
            pady=12,
            command=self.destroy
        ).pack(fill='x', pady=5)


if __name__ == "__main__":
    app = FlashcardApp()
    app.mainloop()