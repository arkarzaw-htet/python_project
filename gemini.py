import tkinter as tk
from tkinter import messagebox, font
import random
import json
import os
from abc import ABC, abstractmethod  # --- ADDED: For abstraction ---

class FlashcardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flashcard Master")
        self.geometry("700x550")
        self.configure(bg='#4255ff')
        
        self.data_file = "flashcards.json"
        self.flashcards = self.load_flashcards()
        
        self.title_font = font.Font(family="Helvetica", size=28, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=14, weight="bold")
        
        container = tk.Frame(self, bg='#4255ff')
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        # --- CHANGED: Pages are now classes, not strings ---
        for F in (MainMenu, AddPage, EditPage, DeletePage, PracticePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        """Shows the frame with the given page_name."""
        frame = self.frames[page_name]
        # --- CHANGED: All frames MUST have refresh(), per BasePage ABC ---
        frame.refresh() 
        frame.tkraise()

    def show_frame_if_cards(self, page_name):
        if not self.flashcards:
            messagebox.showwarning("No Cards", "Create flashcards first.")
            return
        self.show_frame(page_name)

    def refresh_main_menu_count(self):
        main_menu_frame = self.frames.get("MainMenu")
        if main_menu_frame:
            main_menu_frame.refresh() # Its refresh method updates the count

    # --- HELPER: Centralized default cards ---
    def get_default_cards(self):
        return {
            "What is the capital of France?": "Paris",
            "What does HTML stand for?": "HyperText Markup Language",
            "Who painted the Mona Lisa?": "Leonardo da Vinci"
        }

    # --- CHANGED: Added robust try...except blocks ---
    def load_flashcards(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                messagebox.showerror("Load Error", f"Failed to read '{self.data_file}'. File may be corrupt. Loading defaults.")
                return self.get_default_cards()
            except Exception as e:
                messagebox.showerror("Load Error", f"An unexpected error occurred: {e}")
                return self.get_default_cards()
        
        # File doesn't exist, create it with defaults
        default = self.get_default_cards()
        self.save_flashcards(default) # Save will show its own errors if it fails
        return default

    # --- CHANGED: Added robust try...except blocks ---
    def save_flashcards(self, cards=None):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(cards or self.flashcards, f, indent=2, ensure_ascii=False)
        except PermissionError:
            messagebox.showerror("Save Error", f"Failed to save flashcards to '{self.data_file}'. Check file permissions.")
        except Exception as e:
             messagebox.showerror("Save Error", f"An unexpected error occurred during save: {e}")


# --- NEW: Abstract Base Class for all pages ---
class BasePage(tk.Frame, ABC):
    """Abstract base class for all pages, requires a refresh method."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#4255ff')
        self.controller = controller

    @abstractmethod
    def refresh(self):
        """Called by the controller when the frame is shown."""
        pass

# --- NEW: Mixin for abstracting form field creation ---
class FormMixin:
    """Mixin to create standard Question and Answer text fields."""
    def create_form_fields(self, parent_frame):
        tk.Label(parent_frame, text="Question:", font=('Helvetica', 12, 'bold'),
                bg='white').pack(anchor='w', padx=20, pady=(20, 5))
        q_text = tk.Text(parent_frame, height=4, font=('Helvetica', 11))
        q_text.pack(fill='x', padx=20)
        
        tk.Label(parent_frame, text="Answer:", font=('Helvetica', 12, 'bold'),
                bg='white').pack(anchor='w', padx=20, pady=(20, 5))
        a_text = tk.Text(parent_frame, height=4, font=('Helvetica', 11))
        a_text.pack(fill='x', padx=20, pady=(0, 20))
        
        return q_text, a_text


# --- CHANGED: Inherits from BasePage ---
class MainMenu(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        tk.Label(self, text="Flashcard Master", font=controller.title_font, 
                fg='white', bg='#4255ff').pack(pady=40)
        
        self.count_label = tk.Label(self, text="", 
                font=('Helvetica', 14), fg='white', bg='#4255ff')
        self.count_label.pack(pady=10)
        
        buttons = [
            ("Add Flashcard", lambda: controller.show_frame("AddPage"), '#10b981'),
            ("Edit Flashcards", lambda: controller.show_frame_if_cards("EditPage"), '#f59e0b'),
            ("Delete Flashcards", lambda: controller.show_frame_if_cards("DeletePage"), '#ef4444'),
            ("Practice Mode", lambda: controller.show_frame_if_cards("PracticePage"), '#ffffff')
        ]
        
        for text, cmd, color in buttons:
            btn = tk.Button(self, text=text, font=controller.button_font, bg=color,
                          fg='#4255ff' if color == '#ffffff' else 'white',
                          relief='flat', bd=0, pady=15, cursor='hand2', command=cmd)
            btn.pack(fill='x', padx=60, pady=8)

    # --- IMPLEMENTED from BasePage ---
    def refresh(self):
        count = len(self.controller.flashcards)
        self.count_label.config(text=f"Total Cards: {count}")


# --- CHANGED: Inherits from BasePage and FormMixin ---
# --- Inherits from BasePage and FormMixin ---
class AddPage(BasePage, FormMixin):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        tk.Label(self, text="Add New Flashcard", font=('Helvetica', 18, 'bold'),
                fg='white', bg='#4255ff').pack(pady=20)
        
        frame = tk.Frame(self, bg='white')
        frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # --- Use the FormMixin to create fields ---
        self.q_text, self.a_text = self.create_form_fields(frame)
        
        # --- CHANGED: Renamed to self.btn_frame ---
        self.btn_frame = tk.Frame(frame, bg='white')
        self.btn_frame.pack(fill='x', padx=20, side='bottom', pady=(0, 20))
        
        # --- CHANGED: Stored buttons as attributes ---
        self.add_button = tk.Button(self.btn_frame, text="Add", font=('Helvetica', 12, 'bold'), bg='#10b981',
                 fg='white', relief='flat', pady=10, command=self.add)
        
        self.back_button = tk.Button(self.btn_frame, text="Back", font=('Helvetica', 12, 'bold'), bg='#6b7280',
                 fg='white', relief='flat', pady=10, 
                 command=lambda: controller.show_frame("MainMenu"))
        
        # --- NEW: Resize logic ---
        self.threshold = 350 # Pixel width to stack
        self.is_horizontal = None # Track layout state
        self.bind("<Configure>", self.on_resize)

    # --- NEW: Handles responsive button layout ---
    def on_resize(self, event):
        # Ignore initial event when widget hasn't drawn
        if event.width == 1 and event.height == 1:
            return 
        
        width = event.width
        
        # Stack vertically if narrow
        if width < self.threshold and self.is_horizontal is not False:
            self.add_button.pack_forget()
            self.back_button.pack_forget()
            self.add_button.pack(side='top', fill='x', pady=(0, 5))
            self.back_button.pack(side='top', fill='x', pady=(5, 0))
            self.is_horizontal = False
        
        # Place horizontally if wide
        elif width >= self.threshold and self.is_horizontal is not True:
            self.add_button.pack_forget()
            self.back_button.pack_forget()
            self.add_button.pack(side='left', fill='x', expand=True, padx=(0, 5))
            self.back_button.pack(side='right', fill='x', expand=True, padx=(5, 0))
            self.is_horizontal = True

    # --- IMPLEMENTED from BasePage ---
    def refresh(self):
        self.q_text.delete("1.0", tk.END)
        self.a_text.delete("1.0", tk.END)
        # Force redraw on refresh
        self.is_horizontal = None
        self.after(50, lambda: self.on_resize(tk.Event())) # Fake event to trigger layout

    def add(self):
        q = self.q_text.get("1.0", tk.END).strip()
        a = self.a_text.get("1.0", tk.END).strip()
        if q and a:
            self.controller.flashcards[q] = a
            self.controller.save_flashcards()
            self.controller.refresh_main_menu_count() 
            messagebox.showinfo("Success", "Flashcard added!")
            self.controller.show_frame("MainMenu")
        else:
            messagebox.showwarning("Error", "Both fields required!")
# --- CHANGED: Inherits from BasePage and FormMixin ---
# --- Inherits from BasePage and FormMixin ---
class EditPage(BasePage, FormMixin):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.selected = None
        
        tk.Label(self, text="Edit Flashcards", font=('Helvetica', 18, 'bold'),
                fg='white', bg='#4255ff').pack(pady=20)
        
        frame = tk.Frame(self, bg='white')
        frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        self.listbox = tk.Listbox(frame, font=('Helvetica', 10))
        self.listbox.pack(side='left', fill='both', expand=True, padx=(20, 10), pady=20)
        self.listbox.bind("<<ListboxSelect>>", self.load)
        
        right = tk.Frame(frame, bg='white')
        right.pack(side='right', fill='both', expand=True, padx=(10, 20), pady=20)
        
        # --- Use the FormMixin to create fields ---
        self.q_text, self.a_text = self.create_form_fields(right)
        
        # --- CHANGED: Renamed to self.btn_frame ---
        self.btn_frame = tk.Frame(right, bg='white')
        self.btn_frame.pack(fill='x', side='bottom', pady=(0, 20))
        
        # --- CHANGED: Stored buttons as attributes ---
        self.save_button = tk.Button(self.btn_frame, text="Save", font=('Helvetica', 11, 'bold'), bg='#f59e0b',
                 fg='white', relief='flat', pady=10, command=self.save)

        self.back_button = tk.Button(self.btn_frame, text="Back", font=('Helvetica', 11, 'bold'), bg='#6b7280',
                 fg='white', relief='flat', pady=10, 
                 command=lambda: controller.show_frame("MainMenu"))
        
        # --- NEW: Resize logic ---
        self.threshold = 350 # Pixel width to stack
        self.is_horizontal = None # Track layout state
        self.bind("<Configure>", self.on_resize)

    # --- NEW: Handles responsive button layout ---
    def on_resize(self, event):
        if event.width == 1 and event.height == 1:
            return 
        
        width = event.width
        
        if width < self.threshold and self.is_horizontal is not False:
            self.save_button.pack_forget()
            self.back_button.pack_forget()
            self.save_button.pack(side='top', fill='x', pady=(0, 5))
            self.back_button.pack(side='top', fill='x', pady=(5, 0))
            self.is_horizontal = False
        
        elif width >= self.threshold and self.is_horizontal is not True:
            self.save_button.pack_forget()
            self.back_button.pack_forget()
            self.save_button.pack(side='left', fill='x', expand=True, padx=(0, 5))
            self.back_button.pack(side='right', fill='x', expand=True, padx=(5, 0))
            self.is_horizontal = True

    # --- IMPLEMENTED from BasePage ---
    def refresh(self):
        self.listbox.delete(0, tk.END)
        self.q_text.delete("1.0", tk.END)
        self.a_text.delete("1.0", tk.END)
        self.selected = None
        for q in sorted(self.controller.flashcards.keys()):
            self.listbox.insert(tk.END, q[:60])
        # Force redraw on refresh
        self.is_horizontal = None
        self.after(50, lambda: self.on_resize(tk.Event()))

    def load(self, event):
        try:
            sel_index = self.listbox.curselection()[0]
            keys = sorted(self.controller.flashcards.keys())
            self.selected = keys[sel_index]
            
            self.q_text.delete("1.0", tk.END)
            self.q_text.insert("1.0", self.selected)
            self.a_text.delete("1.0", tk.END)
            self.a_text.insert("1.0", self.controller.flashcards[self.selected])
        except IndexError:
            pass 

    def save(self):
        if self.selected:
            new_q = self.q_text.get("1.0", tk.END).strip()
            new_a = self.a_text.get("1.0", tk.END).strip()
            if not (new_q and new_a):
                messagebox.showwarning("Error", "Both fields required!")
                return
                
            if new_q != self.selected:
                del self.controller.flashcards[self.selected]
            self.controller.flashcards[new_q] = new_a
            self.controller.save_flashcards()
            messagebox.showinfo("Success", "Updated!")
            self.controller.show_frame("MainMenu")
# --- CHANGED: Inherits from BasePage ---
class DeletePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        tk.Label(self, text="Delete Flashcards", font=('Helvetica', 18, 'bold'),
                fg='white', bg='#4255ff').pack(pady=20)
        
        frame = tk.Frame(self, bg='white')
        frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        self.listbox = tk.Listbox(frame, font=('Helvetica', 10))
        self.listbox.pack(fill='both', expand=True, padx=20, pady=(20, 10))
        
        btn_frame = tk.Frame(frame, bg='white')
        btn_frame.pack(fill='x', padx=20, pady=(10, 20))
        
        tk.Button(btn_frame, text="Delete Selected", font=('Helvetica', 12, 'bold'),
                 bg='#ef4444', fg='white', relief='flat', pady=12,
                 command=self.delete).pack(side='left', fill='x', expand=True, padx=(0, 5))

        tk.Button(btn_frame, text="Back", font=('Helvetica', 12, 'bold'),
                 bg='#6b7280', fg='white', relief='flat', pady=12,
                 command=lambda: controller.show_frame("MainMenu")).pack(side='right', fill='x', expand=True, padx=(5, 0))

    # --- IMPLEMENTED from BasePage ---
    def refresh(self):
        self.listbox.delete(0, tk.END)
        for q in sorted(self.controller.flashcards.keys()):
            self.listbox.insert(tk.END, q[:70])

    def delete(self):
        try:
            sel_index = self.listbox.curselection()[0]
            keys = sorted(self.controller.flashcards.keys())
            q = keys[sel_index]
            
            if messagebox.askyesno("Confirm", f"Delete:\n{q[:50]}?"):
                del self.controller.flashcards[q]
                self.controller.save_flashcards()
                self.controller.refresh_main_menu_count()
                messagebox.showinfo("Success", "Deleted!")
                self.controller.show_frame("MainMenu") # Go back to menu
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a card to delete.")


# --- CHANGED: Inherits from BasePage ---
# --- Inherits from BasePage ---
class PracticePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.cards = []
        self.index = 0
        self.score = 0
        self.answered = False
        
        tk.Label(self, text="Practice Mode", font=('Helvetica', 20, 'bold'),
                fg='white', bg='#4255ff').pack(pady=20)
        
        stat_frame = tk.Frame(self, bg='white')
        stat_frame.pack(fill='x', padx=40, pady=(0, 10))
        
        self.progress = tk.Label(stat_frame, text="", font=('Helvetica', 11), bg='white')
        self.progress.pack(side='left', padx=20, pady=10)
        
        self.score_lbl = tk.Label(stat_frame, text="Score: 0", font=('Helvetica', 11),
                                  fg='#10b981', bg='white')
        self.score_lbl.pack(side='right', padx=20, pady=10)
        
        card = tk.Frame(self, bg='white')
        card.pack(fill='both', expand=True, padx=40, pady=20)
        
        bottom_controls = tk.Frame(card, bg='white')
        bottom_controls.pack(side='bottom', fill='x', padx=40, pady=(10, 20))

        main_content = tk.Frame(card, bg='white')
        main_content.pack(side='top', fill='both', expand=True)

        self.question = tk.Label(main_content, text="Question", font=('Helvetica', 14, 'bold'),
                                bg='white', wraplength=600)
        self.question.pack(pady=(30, 20), fill='both', expand=True)
        
        self.answer = tk.Label(main_content, text="Answer", font=('Helvetica', 13),
                              fg='#4255ff', bg='white', wraplength=600)
        self.answer.pack(pady=(0, 30), fill='both', expand=True)
        
        self.show_btn = tk.Button(bottom_controls, text="Show Answer", font=('Helvetica', 12, 'bold'),
                                 bg='#4255ff', fg='white', relief='flat', pady=12,
                                 command=self.show_answer)
        self.show_btn.pack(fill='x', pady=(0, 10))
        
        # --- CHANGED: Renamed to self.btn_frame ---
        self.btn_frame = tk.Frame(bottom_controls, bg='white')
        self.btn_frame.pack(fill='x')
        
        # --- CHANGED: Stored buttons as attributes ---
        self.correct_btn = tk.Button(self.btn_frame, text="Correct", font=('Helvetica', 11, 'bold'),
                                     bg='#10b981', fg='white', relief='flat', pady=10,
                                     command=self.correct, state="disabled")
        
        self.wrong_btn = tk.Button(self.btn_frame, text="Wrong", font=('Helvetica', 11, 'bold'),
                                   bg='#ef4444', fg='white', relief='flat', pady=10,
                                   command=self.wrong, state="disabled")
        
        self.next_btn = tk.Button(bottom_controls, text="Next (Marked Wrong)", font=('Helvetica', 12, 'bold'),
                                 bg='#6b7280', fg='white', relief='flat', pady=12,
                                 command=self.next_q, state="disabled")
        self.next_btn.pack(fill='x', pady=10)
        
        tk.Button(bottom_controls, text="Quit Practice", font=('Helvetica', 12, 'bold'),
                 bg='#aaa', fg='white', relief='flat', pady=10,
                 command=lambda: controller.show_frame("MainMenu")).pack(fill='x')
        
        # --- NEW: Resize logic ---
        self.threshold = 350 # Pixel width to stack
        self.is_horizontal = None # Track layout state
        self.bind("<Configure>", self.on_resize)

    # --- NEW: Handles responsive button layout ---
    def on_resize(self, event):
        if event.width == 1 and event.height == 1:
            return 
        
        width = event.width
        
        # Stack vertically if narrow
        if width < self.threshold and self.is_horizontal is not False:
            self.correct_btn.pack_forget()
            self.wrong_btn.pack_forget()
            self.correct_btn.pack(side='top', fill='x', pady=(0, 5))
            self.wrong_btn.pack(side='top', fill='x', pady=(5, 0))
            self.is_horizontal = False
        
        # Place horizontally if wide
        elif width >= self.threshold and self.is_horizontal is not True:
            self.correct_btn.pack_forget()
            self.wrong_btn.pack_forget()
            self.correct_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))
            self.wrong_btn.pack(side='right', fill='x', expand=True, padx=(5, 0))
            self.is_horizontal = True

    # --- IMPLEMENTED from BasePage ---
    def refresh(self):
        self.cards = list(self.controller.flashcards.items())
        random.shuffle(self.cards)
        self.index = 0
        self.score = 0
        self.answered = False
        self.score_lbl.config(text=f"Score: {self.score}")
        self.show_question()
        # Force redraw on refresh
        self.is_horizontal = None
        self.after(50, lambda: self.on_resize(tk.Event())) # Fake event to trigger layout

    def show_question(self):
        if self.index < len(self.cards):
            q, _ = self.cards[self.index]
            self.question.config(text=q)
            self.answer.config(text="")
            self.progress.config(text=f"Card {self.index + 1} of {len(self.cards)}")
            self.answered = False
            self.show_btn.config(state="normal", text="Show Answer")
            self.next_btn.config(state="disabled")
            self.correct_btn.config(state="disabled")
            self.wrong_btn.config(state="disabled")
        else:
            self.finish()

    def show_answer(self):
        if not self.answered:
            _, a = self.cards[self.index]
            self.answer.config(text=a)
            self.answered = True
            self.show_btn.config(state="disabled", text="Answer Shown")
            self.next_btn.config(state="normal")
            self.correct_btn.config(state="normal")
            self.wrong_btn.config(state="normal")

    def next_q(self):
        self.wrong() 

    def correct(self):
        self.score += 1
        self.score_lbl.config(text=f"Score: {self.score}")
        self.index += 1
        self.show_question()

    def wrong(self):
        self.index += 1
        self.show_question()

    def finish(self):
        try:
            pct = round((self.score / len(self.cards)) * 100, 1)
        except ZeroDivisionError:
            pct = 0.0
            
        messagebox.showinfo("Complete!", 
                          f"Score: {self.score}/{len(self.cards)} ({pct}%)")
        self.controller.show_frame("MainMenu")

if __name__ == "__main__":
    app = FlashcardApp()
    app.mainloop()