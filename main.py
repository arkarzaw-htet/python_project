import tkinter as tk
from tkinter import messagebox, font, ttk
import random
import json
import os

class FlashcardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✨ Flashcard Master")
        self.geometry("600x580")
        self.configure(bg='#f0f2f5')
        self.resizable(True, True)
        
        # Configure style
        self.setup_styles()
        
        self.data_file = "flashcards.json"
        self.flashcards = self.load_flashcards()

        # Create main interface
        self.create_header()
        self.create_main_buttons()
        self.create_footer()

    def setup_styles(self):
        """Set up modern styling"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Define color scheme
        self.colors = {
            'primary': '#4f46e5',      # Indigo
            'primary_hover': '#3730a3', # Darker indigo
            'secondary': '#06b6d4',     # Cyan
            'success': '#10b981',       # Emerald
            'danger': '#ef4444',        # Red
            'warning': '#f59e0b',       # Amber
            'bg_light': '#f8fafc',      # Very light gray
            'bg_dark': '#1e293b',       # Dark slate
            'text_dark': '#1f2937',     # Dark gray
            'text_light': '#6b7280',    # Light gray
        }
        
        # Configure fonts
        self.fonts = {
            'title': font.Font(family="Helvetica", size=24, weight="bold"),
            'heading': font.Font(family="Helvetica", size=16, weight="bold"),
            'body': font.Font(family="Helvetica", size=12),
            'button': font.Font(family="Helvetica", size=14, weight="bold"),
            'small': font.Font(family="Helvetica", size=10),
        }

    def create_header(self):
        """Create the header with title and stats"""
        header_frame = tk.Frame(self, bg='#f0f2f5', pady=20)
        header_frame.pack(fill='x', padx=30)
        
        # Title
        title_label = tk.Label(
            header_frame, 
            text="✨ Flashcard Master",
            font=self.fonts['title'],
            fg=self.colors['primary'],
            bg='#f0f2f5'
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Learn smarter, not harder",
            font=self.fonts['body'],
            fg=self.colors['text_light'],
            bg='#f0f2f5'
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Stats card
        self.create_stats_card(header_frame)

    def create_stats_card(self, parent):
        """Create a modern stats card"""
        stats_frame = tk.Frame(parent, bg='white', relief='flat', bd=0)
        stats_frame.pack(pady=(20, 0), padx=20, fill='x')
        
        # Add subtle border effect
        border_frame = tk.Frame(parent, bg='#e5e7eb', height=1)
        border_frame.pack(fill='x', padx=20)
        
        inner_frame = tk.Frame(stats_frame, bg='white', pady=15)
        inner_frame.pack(fill='x')
        
        # Total cards
        self.stats_label = tk.Label(
            inner_frame,
            text=f"📚 Total Flashcards: {len(self.flashcards)}",
            font=self.fonts['heading'],
            fg=self.colors['text_dark'],
            bg='white'
        )
        self.stats_label.pack()

    def create_main_buttons(self):
        """Create main action buttons with modern design"""
        buttons_frame = tk.Frame(self, bg='#f0f2f5', pady=30)
        buttons_frame.pack(expand=True, fill='both', padx=30)
        
        # Button configurations
        buttons_config = [
            {
                'text': '➕ Add Flashcard',
                'command': self.open_add_window,
                'color': self.colors['success'],
                'hover_color': '#059669',
                'icon': '➕'
            },
            {
                'text': '✏️ Edit Flashcards',
                'command': self.open_edit_window,
                'color': self.colors['warning'],
                'hover_color': '#d97706',
                'icon': '✏️'
            },
            {
                'text': '🗑️ Delete Flashcards',
                'command': self.open_delete_window,
                'color': self.colors['danger'],
                'hover_color': '#dc2626',
                'icon': '🗑️'
            },
            {
                'text': '🎯 Practice Mode',
                'command': self.open_practice_window,
                'color': self.colors['primary'],
                'hover_color': self.colors['primary_hover'],
                'icon': '🎯'
            }
        ]
        
        for i, btn_config in enumerate(buttons_config):
            self.create_modern_button(buttons_frame, btn_config, row=i)

    def create_modern_button(self, parent, config, row):
        """Create a modern button with hover effects"""
        btn_frame = tk.Frame(parent, bg='#f0f2f5')
        btn_frame.pack(fill='x', pady=8)
        
        btn = tk.Button(
            btn_frame,
            text=config['text'],
            font=self.fonts['button'],
            bg=config['color'],
            fg='white',
            activebackground=config['hover_color'],
            activeforeground='white',
            relief='flat',
            bd=0,
            pady=15,
            cursor='hand2',
            command=config['command']
        )
        btn.pack(fill='x', padx=20)
        
        # Add hover effects
        def on_enter(e):
            btn.config(bg=config['hover_color'])
        
        def on_leave(e):
            btn.config(bg=config['color'])
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def create_footer(self):
        """Create footer with additional info"""
        footer_frame = tk.Frame(self, bg='#f0f2f5', pady=10)
        footer_frame.pack(fill='x', side='bottom')
        
        footer_label = tk.Label(
            footer_frame,
            text="💡 Tip: Regular practice leads to better retention!",
            font=self.fonts['small'],
            fg=self.colors['text_light'],
            bg='#f0f2f5'
        )
        footer_label.pack()

    def load_flashcards(self):
        """Load flashcards from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                messagebox.showwarning("Warning", f"Error loading flashcards: {e}\nStarting fresh.")
        
        # Default flashcards
        default_cards = {
            "What is the capital of France?": "Paris",
            "What does HTML stand for?": "HyperText Markup Language",
            "Who painted the Mona Lisa?": "Leonardo da Vinci"
        }
        self.save_flashcards(default_cards)
        return default_cards

    def save_flashcards(self, flashcards_dict=None):
        """Save flashcards to JSON file"""
        cards_to_save = flashcards_dict if flashcards_dict is not None else self.flashcards
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(cards_to_save, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save flashcards: {e}")

    def refresh_main_window(self):
        """Refresh the main window display"""
        self.stats_label.config(text=f"📚 Total Flashcards: {len(self.flashcards)}")

    def open_add_window(self):
        AddWindow(self, self.flashcards)

    def open_edit_window(self):
        if not self.flashcards:
            self.show_custom_warning("No flashcards to edit!", "Create some flashcards first.")
            return
        EditWindow(self, self.flashcards)

    def open_delete_window(self):
        if not self.flashcards:
            self.show_custom_warning("No flashcards to delete!", "Create some flashcards first.")
            return
        DeleteWindow(self, self.flashcards)

    def open_practice_window(self):
        if not self.flashcards:
            self.show_custom_warning("No flashcards to practice!", "Create some flashcards first.")
            return
        PracticeWindow(self, self.flashcards)

    def show_custom_warning(self, title, message):
        """Show a custom styled warning"""
        messagebox.showwarning(title, message)


# ---------------- ADD WINDOW ----------------
class AddWindow(tk.Toplevel):
    def __init__(self, parent, flashcards):
        super().__init__(parent)
        self.title("➕ Add New Flashcard")
        self.geometry("700x450")
        self.configure(bg='#f8fafc')
        self.resizable(True, True)
        
        self.flashcards = flashcards
        self.parent = parent
        
        self.setup_styles()
        self.create_interface()
        
        # Center the window
        self.center_window()

    def setup_styles(self):
        """Setup styling for add window"""
        self.fonts = {
            'title': font.Font(family="Helvetica", size=18, weight="bold"),
            'label': font.Font(family="Helvetica", size=12, weight="bold"),
            'entry': font.Font(family="Helvetica", size=11),
            'button': font.Font(family="Helvetica", size=12, weight="bold"),
        }

    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def create_interface(self):
        """Create the add flashcard interface"""
        # Header
        header_frame = tk.Frame(self, bg='#f8fafc', pady=20)
        header_frame.pack(fill='x', padx=30)
        
        tk.Label(
            header_frame,
            text="➕ Add New Flashcard",
            font=self.fonts['title'],
            fg='#059669',
            bg='#f8fafc'
        ).pack()

        # Main form
        form_frame = tk.Frame(self, bg='white', relief='flat', bd=0)
        form_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        inner_form = tk.Frame(form_frame, bg='white', padx=30, pady=30)
        inner_form.pack(fill='both', expand=True)

        # Question field
        tk.Label(
            inner_form,
            text="Question:",
            font=self.fonts['label'],
            fg='#1f2937',
            bg='white'
        ).pack(anchor='w', pady=(0, 5))
        
        self.question_text = tk.Text(
            inner_form,
            font=self.fonts['entry'],
            height=4,
            wrap='word',
            relief='solid',
            bd=1,
            highlightthickness=0
        )
        self.question_text.pack(fill='x', pady=(0, 20))

        # Answer field
        tk.Label(
            inner_form,
            text="Answer:",
            font=self.fonts['label'],
            fg='#1f2937',
            bg='white'
        ).pack(anchor='w', pady=(0, 5))
        
        self.answer_text = tk.Text(
            inner_form,
            font=self.fonts['entry'],
            height=4,
            wrap='word',
            relief='solid',
            bd=1,
            highlightthickness=0
        )
        self.answer_text.pack(fill='x', pady=(0, 30))

        # Buttons
        btn_frame = tk.Frame(inner_form, bg='white')
        btn_frame.pack(fill='x')

        # Add button
        add_btn = tk.Button(
            btn_frame,
            text="✅ Add Flashcard",
            font=self.fonts['button'],
            bg='#059669',
            fg='white',
            activebackground='#047857',
            activeforeground='white',
            relief='flat',
            bd=0,
            pady=12,
            cursor='hand2',
            command=self.add_flashcard
        )
        add_btn.pack(side='left', fill='x', expand=True, padx=(0, 10))

        # Cancel button
        cancel_btn = tk.Button(
            btn_frame,
            text="❌ Cancel",
            font=self.fonts['button'],
            bg='#6b7280',
            fg='white',
            activebackground='#4b5563',
            activeforeground='white',
            relief='flat',
            bd=0,
            pady=12,
            cursor='hand2',
            command=self.destroy
        )
        cancel_btn.pack(side='right', fill='x', expand=True, padx=(10, 0))

        # Focus on question
        self.question_text.focus()

    def add_flashcard(self):
        """Add the flashcard"""
        question = self.question_text.get("1.0", tk.END).strip()
        answer = self.answer_text.get("1.0", tk.END).strip()
        
        if question and answer:
            if question in self.flashcards:
                if messagebox.askyesno("Duplicate Found", 
                                     f"Question already exists:\n'{question[:50]}...'\n\nUpdate the answer?"):
                    self.flashcards[question] = answer
                    self.parent.save_flashcards()
                    self.parent.refresh_main_window()
                    messagebox.showinfo("✅ Success", "Flashcard updated!")
                    self.destroy()
            else:
                self.flashcards[question] = answer
                self.parent.save_flashcards()
                self.parent.refresh_main_window()
                messagebox.showinfo("✅ Success", "Flashcard added!")
                self.destroy()
        else:
            messagebox.showwarning("⚠️ Missing Information", "Both question and answer are required!")


# ---------------- EDIT WINDOW ----------------
class EditWindow(tk.Toplevel):
    def __init__(self, parent, flashcards):
        super().__init__(parent)
        self.title("✏️ Edit Flashcards")
        self.geometry("800x600")
        self.configure(bg='#f8fafc')
        self.resizable(True, True)
        
        self.flashcards = flashcards
        self.parent = parent
        self.selected_question = None
        
        self.setup_styles()
        self.create_interface()
        self.center_window()

    def setup_styles(self):
        self.fonts = {
            'title': font.Font(family="Helvetica", size=18, weight="bold"),
            'label': font.Font(family="Helvetica", size=12, weight="bold"),
            'entry': font.Font(family="Helvetica", size=11),
            'button': font.Font(family="Helvetica", size=12, weight="bold"),
            'list': font.Font(family="Helvetica", size=10),
        }

    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def create_interface(self):
        # Header
        header_frame = tk.Frame(self, bg='#f8fafc', pady=20)
        header_frame.pack(fill='x', padx=30)
        
        tk.Label(
            header_frame,
            text="✏️ Edit Flashcards",
            font=self.fonts['title'],
            fg='#d97706',
            bg='#f8fafc'
        ).pack()

        # Main content
        content_frame = tk.Frame(self, bg='white')
        content_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        inner_content = tk.Frame(content_frame, bg='white', padx=20, pady=20)
        inner_content.pack(fill='both', expand=True)

        # Left side - List
        left_frame = tk.Frame(inner_content, bg='white')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 20))
        
        tk.Label(
            left_frame,
            text="Select a flashcard to edit:",
            font=self.fonts['label'],
            fg='#1f2937',
            bg='white'
        ).pack(anchor='w', pady=(0, 10))

        self.listbox = tk.Listbox(
            left_frame,
            font=self.fonts['list'],
            selectmode='single',
            relief='solid',
            bd=1,
            highlightthickness=0
        )
        self.listbox.pack(fill='both', expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.load_selected_flashcard)
        
        self.refresh_list()

        # Right side - Edit form
        right_frame = tk.Frame(inner_content, bg='white')
        right_frame.pack(side='right', fill='both', expand=True)

        # Question field
        tk.Label(
            right_frame,
            text="Question:",
            font=self.fonts['label'],
            fg='#1f2937',
            bg='white'
        ).pack(anchor='w', pady=(0, 5))
        
        self.question_text = tk.Text(
            right_frame,
            font=self.fonts['entry'],
            height=4,
            wrap='word',
            relief='solid',
            bd=1,
            highlightthickness=0
        )
        self.question_text.pack(fill='x', pady=(0, 20))

        # Answer field
        tk.Label(
            right_frame,
            text="Answer:",
            font=self.fonts['label'],
            fg='#1f2937',
            bg='white'
        ).pack(anchor='w', pady=(0, 5))
        
        self.answer_text = tk.Text(
            right_frame,
            font=self.fonts['entry'],
            height=4,
            wrap='word',
            relief='solid',
            bd=1,
            highlightthickness=0
        )
        self.answer_text.pack(fill='x', pady=(0, 30))

        # Save button
        save_btn = tk.Button(
            right_frame,
            text="💾 Save Changes",
            font=self.fonts['button'],
            bg='#d97706',
            fg='white',
            activebackground='#b45309',
            activeforeground='white',
            relief='flat',
            bd=0,
            pady=12,
            cursor='hand2',
            command=self.save_changes
        )
        save_btn.pack(fill='x')

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for q in sorted(self.flashcards.keys()):
            display_q = q[:60] + "..." if len(q) > 60 else q
            self.listbox.insert(tk.END, display_q)

    def load_selected_flashcard(self, event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            display_question = self.listbox.get(index)
            # Find the actual question
            sorted_keys = sorted(self.flashcards.keys())
            if index < len(sorted_keys):
                question = sorted_keys[index]
                answer = self.flashcards[question]
                self.selected_question = question
                
                self.question_text.delete("1.0", tk.END)
                self.question_text.insert("1.0", question)
                self.answer_text.delete("1.0", tk.END)
                self.answer_text.insert("1.0", answer)

    def save_changes(self):
        if self.selected_question:
            new_q = self.question_text.get("1.0", tk.END).strip()
            new_a = self.answer_text.get("1.0", tk.END).strip()
            
            if new_q and new_a:
                if new_q != self.selected_question:
                    del self.flashcards[self.selected_question]
                self.flashcards[new_q] = new_a
                self.parent.save_flashcards()
                self.parent.refresh_main_window()
                messagebox.showinfo("✅ Success", "Flashcard updated!")
                self.destroy()
            else:
                messagebox.showwarning("⚠️ Missing Information", "Both fields are required!")
        else:
            messagebox.showwarning("⚠️ No Selection", "Please select a flashcard to edit!")


# ---------------- DELETE WINDOW ----------------
class DeleteWindow(tk.Toplevel):
    def __init__(self, parent, flashcards):
        super().__init__(parent)
        self.title("🗑️ Delete Flashcards")
        self.geometry("600x500")
        self.configure(bg='#f8fafc')
        self.resizable(True, True)
        
        self.flashcards = flashcards
        self.parent = parent
        
        self.setup_styles()
        self.create_interface()
        self.center_window()

    def setup_styles(self):
        self.fonts = {
            'title': font.Font(family="Helvetica", size=18, weight="bold"),
            'button': font.Font(family="Helvetica", size=12, weight="bold"),
            'list': font.Font(family="Helvetica", size=10),
        }

    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def create_interface(self):
        # Header
        header_frame = tk.Frame(self, bg='#f8fafc', pady=20)
        header_frame.pack(fill='x', padx=30)
        
        tk.Label(
            header_frame,
            text="🗑️ Delete Flashcards",
            font=self.fonts['title'],
            fg='#dc2626',
            bg='#f8fafc'
        ).pack()
        
        tk.Label(
            header_frame,
            text="⚠️ Select flashcards to delete (this cannot be undone)",
            font=font.Font(family="Helvetica", size=10),
            fg='#6b7280',
            bg='#f8fafc'
        ).pack(pady=(5, 0))

        # Content
        content_frame = tk.Frame(self, bg='white')
        content_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        inner_content = tk.Frame(content_frame, bg='white', padx=20, pady=20)
        inner_content.pack(fill='both', expand=True)

        # List
        self.listbox = tk.Listbox(
            inner_content,
            font=self.fonts['list'],
            selectmode='single',
            relief='solid',
            bd=1,
            highlightthickness=0
        )
        self.listbox.pack(fill='both', expand=True, pady=(0, 20))
        self.refresh_list()

        # Delete button
        delete_btn = tk.Button(
            inner_content,
            text="🗑️ Delete Selected",
            font=self.fonts['button'],
            bg='#dc2626',
            fg='white',
            activebackground='#b91c1c',
            activeforeground='white',
            relief='flat',
            bd=0,
            pady=12,
            cursor='hand2',
            command=self.delete_selected
        )
        delete_btn.pack(fill='x')

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for q in sorted(self.flashcards.keys()):
            display_q = q[:80] + "..." if len(q) > 80 else q
            self.listbox.insert(tk.END, display_q)

    def delete_selected(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            sorted_keys = sorted(self.flashcards.keys())
            if index < len(sorted_keys):
                question = sorted_keys[index]
                short_q = question[:50] + "..." if len(question) > 50 else question
                
                if messagebox.askyesno("🗑️ Confirm Delete", 
                                     f"Are you sure you want to delete:\n\n'{short_q}'?\n\nThis cannot be undone!"):
                    del self.flashcards[question]
                    self.parent.save_flashcards()
                    self.parent.refresh_main_window()
                    messagebox.showinfo("✅ Deleted", "Flashcard deleted successfully!")
                    self.destroy()
        else:
            messagebox.showwarning("⚠️ No Selection", "Please select a flashcard to delete!")


# ---------------- PRACTICE WINDOW ----------------
class PracticeWindow(tk.Toplevel):
    def __init__(self, parent, flashcards):
        super().__init__(parent)
        self.title("🎯 Practice Mode")
        self.geometry("800x600")
        self.configure(bg='#f8fafc')
        self.resizable(True, True)
        
        self.flashcards = list(flashcards.items())
        random.shuffle(self.flashcards)
        self.index = 0
        self.score = 0
        self.answered = False
        
        self.setup_styles()
        self.create_interface()
        self.center_window()
        self.show_question()

    def setup_styles(self):
        self.fonts = {
            'title': font.Font(family="Helvetica", size=20, weight="bold"),
            'question': font.Font(family="Helvetica", size=14, weight="bold"),
            'answer': font.Font(family="Helvetica", size=14),
            'button': font.Font(family="Helvetica", size=12, weight="bold"),
            'stats': font.Font(family="Helvetica", size=12),
        }

    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def create_interface(self):
        # Header
        header_frame = tk.Frame(self, bg='#f8fafc', pady=20)
        header_frame.pack(fill='x')
        
        tk.Label(
            header_frame,
            text="🎯 Practice Mode",
            font=self.fonts['title'],
            fg='#4f46e5',
            bg='#f8fafc'
        ).pack()

        # Stats
        self.stats_frame = tk.Frame(self, bg='#f8fafc')
        self.stats_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        stats_inner = tk.Frame(self.stats_frame, bg='white', pady=10)
        stats_inner.pack(fill='x')
        
        self.progress_label = tk.Label(
            stats_inner,
            text="",
            font=self.fonts['stats'],
            fg='#6b7280',
            bg='white'
        )
        self.progress_label.pack(side='left', padx=20)
        
        self.score_label = tk.Label(
            stats_inner,
            text="Score: 0",
            font=self.fonts['stats'],
            fg='#059669',
            bg='white'
        )
        self.score_label.pack(side='right', padx=20)

        # Card area
        card_frame = tk.Frame(self, bg='white', relief='flat', bd=0)
        card_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        inner_card = tk.Frame(card_frame, bg='white', padx=40, pady=40)
        inner_card.pack(fill='both', expand=True)

        # Question
        self.question_label = tk.Label(
            inner_card,
            text="",
            font=self.fonts['question'],
            fg='#1f2937',
            bg='white',
            wraplength=600,
            justify='left'
        )
        self.question_label.pack(pady=(0, 30))

        # Answer (hidden initially)
        self.answer_label = tk.Label(
            inner_card,
            text="",
            font=self.fonts['answer'],
            fg='#4f46e5',
            bg='white',
            wraplength=600,
            justify='left'
        )
        self.answer_label.pack(pady=(0, 40))

        # Control buttons
        btn_frame = tk.Frame(inner_card, bg='white')
        btn_frame.pack(fill='x')

        self.show_btn = tk.Button(
            btn_frame,
            text="👁️ Show Answer",
            font=self.fonts['button'],
            bg='#4f46e5',
            fg='white',
            activebackground='#3730a3',
            activeforeground='white',
            relief='flat',
            bd=0,
            pady=12,
            cursor='hand2',
            command=self.show_answer
        )
        self.show_btn.pack(fill='x', pady=(0, 10))

        # Scoring buttons
        scoring_frame = tk.Frame(inner_card, bg='white')
        scoring_frame.pack(fill='x', pady=(10, 0))

        self.correct_btn = tk.Button(
            scoring_frame,
            text="✅ Got it Right",
            font=self.fonts['button'],
            bg='#059669',
            fg='white',
            activebackground='#047857',
            activeforeground='white',
            relief='flat',
            bd=0,
            pady=12,
            cursor='hand2',
            command=self.correct_answer,
            state="disabled"
        )
        self.correct_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        self.wrong_btn = tk.Button(
            scoring_frame,
            text="❌ Got it Wrong",
            font=self.fonts['button'],
            bg='#dc2626',
            fg='white',
            activebackground='#b91c1c',
            activeforeground='white',
            relief='flat',
            bd=0,
            pady=12,
            cursor='hand2',
            command=self.wrong_answer,
            state="disabled"
        )
        self.wrong_btn.pack(side='right', fill='x', expand=True, padx=(5, 0))

        # Next button
        self.next_btn = tk.Button(
            inner_card,
            text="➡️ Next Question",
            font=self.fonts['button'],
            bg='#6b7280',
            fg='white',
            activebackground='#4b5563',
            activeforeground='white',
            relief='flat',
            bd=0,
            pady=12,
            cursor='hand2',
            command=self.next_question,
            state="disabled"
        )
        self.next_btn.pack(fill='x', pady=(20, 0))

        # Keyboard bindings
        self.bind('<space>', lambda e: self.show_answer() if self.show_btn['state'] == 'normal' else None)
        self.bind('<Return>', lambda e: self.correct_answer() if self.correct_btn['state'] == 'normal' else None)
        self.bind('<BackSpace>', lambda e: self.wrong_answer() if self.wrong_btn['state'] == 'normal' else None)
        self.bind('<Right>', lambda e: self.next_question() if self.next_btn['state'] == 'normal' else None)
        
        self.focus_set()  # Enable keyboard events

    def show_question(self):
        if self.index < len(self.flashcards):
            q, _ = self.flashcards[self.index]
            self.question_label.config(text=f"❓ {q}")
            self.answer_label.config(text="")
            self.progress_label.config(text=f"Card {self.index + 1} of {len(self.flashcards)}")
            self.answered = False
            
            # Reset button states
            self.show_btn.config(state="normal")
            self.next_btn.config(state="disabled")
            self.correct_btn.config(state="disabled")
            self.wrong_btn.config(state="disabled")
        else:
            self.show_completion()

    def show_answer(self):
        if self.index < len(self.flashcards) and not self.answered:
            _, a = self.flashcards[self.index]
            self.answer_label.config(text=f"💡 {a}")
            self.answered = True
            
            # Update button states
            self.show_btn.config(state="disabled")
            self.next_btn.config(state="normal")
            self.correct_btn.config(state="normal")
            self.wrong_btn.config(state="normal")

    def next_question(self):
        self.index += 1
        self.show_question()

    def correct_answer(self):
        self.score += 1
        self.score_label.config(text=f"Score: {self.score}")
        self.next_question()

    def wrong_answer(self):
        self.next_question()

    def show_completion(self):
        percentage = round((self.score / len(self.flashcards)) * 100, 1) if self.flashcards else 0
        
        if percentage >= 90:
            emoji = "🏆"
            message = "Outstanding!"
        elif percentage >= 75:
            emoji = "🎉"
            message = "Great job!"
        elif percentage >= 50:
            emoji = "👍"
            message = "Good effort!"
        else:
            emoji = "💪"
            message = "Keep practicing!"
        
        messagebox.showinfo("🎯 Practice Complete!", 
                          f"{emoji} {message}\n\n"
                          f"Final Score: {self.score}/{len(self.flashcards)} ({percentage}%)\n\n"
                          f"💡 Tip: Regular practice improves retention!")
        self.destroy()


# Run the app
if __name__ == "__main__":
    app = FlashcardApp()
    app.mainloop()
