
# ============================================================= #
# Python Individual Project, Year 1, Semester 1                 #
#                                                               #
#                                                               #
# Program: Software Engineering Program                         #
# University: Faculty of Engineering, KMITL                     #
#                                                               #
# Project: Flashcard Master                                     #                                            
# Repository: https://github.com/arkarzaw-htet/FlashcardMaster  #
# Written by: Arkar Zaw Htet(68011284)                          #
# ============================================================= #


import random
import json
import os
from abc import ABC, abstractmethod

# --- Robust Tkinter Import ---
try:
    import tkinter as tk
    from tkinter import messagebox, font
except ImportError:
    try:
        # Fallback for Python 2
        import Tkinter as tk
        import tkMessageBox as messagebox
        import tkFont as font
    except ImportError:
        print("Error: Tkinter/Tkinter module not found. The application cannot run.")
        exit()

COLOR_PRIMARY_DARK = '#36394E'  
COLOR_SECONDARY = '#454866'     
COLOR_ACCENT = "#0F1BA3"        
COLOR_SUCCESS_GREEN = "#00be20" 
COLOR_TEXT_LIGHT = 'white'
COLOR_TEXT_DARK = '#2C2F43'     
COLOR_CARD_BG = "#8ece98"       


BUTTON_BORDER_WIDTH = 4 
BUTTON_RELIEF = 'groove' 

# --- COMPOSITION: StatTracker Class ---
class StatTracker:
    """Manages and calculates statistics for the PracticePage."""
    def __init__(self):
        self._score = 0
        self._total_cards = 0

    def get_score(self):
        """Returns the current score."""
        return self._score

    def get_total_cards(self):
        """Returns the total number of cards in the session."""
        return self._total_cards

    def reset(self, total_cards):
        """Rests stats for a new practice session."""
        self._score = 0
        self._total_cards = total_cards

    def increment_score(self):
        """Adds one point to the score."""
        self._score += 1

    def get_percentage(self):
        """Calculates the score percentage."""
        try:
            return round((self._score / self._total_cards) * 100, 1)
        except ZeroDivisionError:
            return 0.0

    def get_display(self):
        """Returns the score string for display (e.g., 'Score: 5/10')."""
        return f"Score: {self._score}/{self._total_cards}"


class FlashcardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flashcard Master")
        self.configure(bg=COLOR_PRIMARY_DARK) 
        
        # Prevent the blank window flash
        self.withdraw() 
        
        # --- WINDOW CENTERING CALCULATION ---
        window_width = 1000 
        window_height = 900 
        
        self.update_idletasks() 

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))

        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        
        self.data_file = "flashcards.json"
        self.flashcards = self.load_flashcards()
        
        self.title_font = font.Font(family="Helvetica", size=28, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=14, weight="bold")
        
        container = tk.Frame(self, bg=COLOR_SECONDARY) 
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        for F in (MainMenu, AddPage, EditPage, DeletePage, PracticePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")
        
        # Show the window only after it's fully configured
        self.deiconify()
        
    def show_frame(self, page_name):
        """Shows the frame with the given page_name."""
        frame = self.frames[page_name]
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
            main_menu_frame.refresh()

    def get_default_cards(self):
        return {
            "What is the capital of France?": "Paris",
            "What does HTML stand for?": "HyperText Markup Language",
            "Who painted the Mona Lisa?": "Leonardo da Vinci"
        }

    def load_flashcards(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                messagebox.showerror("Load Error", f"Failed to read '{self.data_file}'. File may be corrupt. Loading defaults.")
                return self.get_default_cards()
            except IOError as e:
                messagebox.showerror("Load Error", f"File I/O error occurred: {e}. Loading defaults.")
                return self.get_default_cards()
            except Exception as e:
                messagebox.showerror("Load Error", f"An unexpected error occurred: {e}. Loading defaults.")
                return self.get_default_cards()
        
        default = self.get_default_cards()
        self.save_flashcards(default)
        return default

    def save_flashcards(self, cards=None):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(cards or self.flashcards, f, indent=2, ensure_ascii=False)
        except PermissionError:
            messagebox.showerror("Save Error", f"Failed to save flashcards to '{self.data_file}'. Check file permissions.")
        except IOError as e:
            messagebox.showerror("Save Error", f"File I/O error occurred during save: {e}")
        except Exception as e:
             messagebox.showerror("Save Error", f"An unexpected error occurred during save: {e}")


class BasePage(tk.Frame, ABC):
    """Abstract base class for all pages, requires a refresh method."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_SECONDARY) 
        self.controller = controller

    @abstractmethod
    def refresh(self):
        """Called by the controller when the frame is shown."""
        pass

class FormMixin:
    """Mixin to create standard Question and Answer text fields with internal padding."""
    def create_form_fields(self, parent_frame):
        # Increased background color to match COLOR_CARD_BG
        tk.Label(parent_frame, text="Question:", font=('Helvetica', 12, 'bold'),
                bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK).pack(anchor='w', padx=30, pady=(20, 5)) 
        
        # ADDED padx and pady inside the Text widget
        q_text = tk.Text(parent_frame, height=5, font=('Helvetica', 11), bg=COLOR_CARD_BG, 
                         fg=COLOR_TEXT_DARK, padx=10, pady=10, borderwidth=1, relief="solid")
        q_text.pack(fill='x', padx=30)
        
        tk.Label(parent_frame, text="Answer:", font=('Helvetica', 12, 'bold'),
                bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK).pack(anchor='w', padx=30, pady=(20, 5)) 
        
        # ADDED padx and pady inside the Text widget
        a_text = tk.Text(parent_frame, height=5, font=('Helvetica', 11), bg=COLOR_CARD_BG, 
                         fg=COLOR_TEXT_DARK, padx=10, pady=10, borderwidth=1, relief="solid")
        a_text.pack(fill='x', padx=30, pady=(0, 30)) 
        
        return q_text, a_text

class MainMenu(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        tk.Label(self, text="Flashcard Master", font=controller.title_font, 
                fg=COLOR_TEXT_LIGHT, bg=COLOR_SECONDARY).pack(pady=60) 
        
        self.count_label = tk.Label(self, text="", 
                font=('Helvetica', 16), fg=COLOR_TEXT_LIGHT, bg=COLOR_SECONDARY) 
        self.count_label.pack(pady=20) 
        
        buttons = [
            ("Add Flashcard", lambda: controller.show_frame("AddPage"), COLOR_SUCCESS_GREEN),  
            ("Edit Flashcards", lambda: controller.show_frame_if_cards("EditPage"), '#f59e0b'), 
            ("Delete Flashcards", lambda: controller.show_frame_if_cards("DeletePage"), '#ef4444'), 
            ("Practice Mode", lambda: controller.show_frame_if_cards("PracticePage"), COLOR_ACCENT) 
        ]
        
        for text, cmd, color in buttons:
            btn = tk.Button(self, text=text, font=controller.button_font, bg=color,
                          fg=COLOR_TEXT_LIGHT if color != COLOR_CARD_BG else COLOR_TEXT_DARK,
                          relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=18, cursor='hand2', command=cmd) 
            btn.pack(fill='x', padx=100, pady=10) 

    def refresh(self):
        count = len(self.controller.flashcards)
        self.count_label.config(text=f"Total Cards: {count}")

class AddPage(BasePage, FormMixin):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        tk.Label(self, text="Add New Flashcard", font=('Helvetica', 20, 'bold'), 
                fg=COLOR_TEXT_LIGHT, bg=COLOR_SECONDARY).pack(pady=30) 
        
        frame = tk.Frame(self, bg=COLOR_CARD_BG) 
        frame.pack(fill='both', expand=True, padx=80, pady=30) 
        
        self.q_text, self.a_text = self.create_form_fields(frame)
        
        self.btn_frame = tk.Frame(frame, bg=COLOR_CARD_BG) 
        self.btn_frame.pack(fill='x', padx=30, side='bottom', pady=(0, 30)) 
        
        self.add_button = tk.Button(self.btn_frame, text="Add", font=('Helvetica', 13, 'bold'), bg=COLOR_SUCCESS_GREEN, # Use new green
                 fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=12, command=self.add) 
        
        self.back_button = tk.Button(self.btn_frame, text="Back", font=('Helvetica', 13, 'bold'), bg='#6b7280',
                 fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=12, 
                 command=lambda: controller.show_frame("MainMenu")) 
        
        self.threshold = 400 
        self.is_horizontal = None
        self.bind("<Configure>", self.on_resize)
        self.after(100, self.trigger_resize)
        
    def trigger_resize(self):
        self.on_resize(type('Event', (), {'width': self.winfo_width(), 'height': self.winfo_height()})())
        
    def on_resize(self, event):
        if event.width == 1 and event.height == 1:
            return 
        
        width = event.width
        
        if width < self.threshold and self.is_horizontal is not False:
            self.add_button.pack_forget()
            self.back_button.pack_forget()
            self.add_button.pack(side='top', fill='x', pady=(0, 8))
            self.back_button.pack(side='top', fill='x', pady=(8, 0))
            self.is_horizontal = False
        
        elif width >= self.threshold and self.is_horizontal is not True:
            self.add_button.pack_forget()
            self.back_button.pack_forget()
            self.add_button.pack(side='left', fill='x', expand=True, padx=(0, 8))
            self.back_button.pack(side='right', fill='x', expand=True, padx=(8, 0))
            self.is_horizontal = True

    def refresh(self):
        self.q_text.delete("1.0", tk.END)
        self.a_text.delete("1.0", tk.END)
        self.is_horizontal = None
        self.after(50, self.trigger_resize)
        
    def add(self):
        try:
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
        except Exception as e:
            messagebox.showerror("Add Error", f"Failed to add card: {e}")

class EditPage(BasePage, FormMixin):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.selected = None
        
        tk.Label(self, text="Edit Flashcards", font=('Helvetica', 20, 'bold'),
                fg=COLOR_TEXT_LIGHT, bg=COLOR_SECONDARY).pack(pady=30)
        
        frame = tk.Frame(self, bg=COLOR_CARD_BG)
        frame.pack(fill='both', expand=True, padx=80, pady=30)
        
        self.listbox = tk.Listbox(frame, font=('Helvetica', 12), borderwidth=1, relief="solid", bg="#f7f7f7", fg=COLOR_TEXT_DARK) # Added bg/fg
        self.listbox.pack(side='left', fill='both', expand=True, padx=(30, 15), pady=30)
        self.listbox.bind("<<ListboxSelect>>", self.load)
        
        right = tk.Frame(frame, bg=COLOR_CARD_BG)
        right.pack(side='right', fill='both', expand=True, padx=(15, 30), pady=30)
        
        self.q_text, self.a_text = self.create_form_fields(right)
        
        self.btn_frame = tk.Frame(right, bg=COLOR_CARD_BG)
        self.btn_frame.pack(fill='x', side='bottom', pady=(0, 30))
        
        self.save_button = tk.Button(self.btn_frame, text="Save", font=('Helvetica', 13, 'bold'), bg='#f59e0b',
                 fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=12, command=self.save)

        self.back_button = tk.Button(self.btn_frame, text="Back", font=('Helvetica', 13, 'bold'), bg='#6b7280',
                 fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=12, 
                 command=lambda: controller.show_frame("MainMenu"))
        
        self.threshold = 400
        self.is_horizontal = None
        self.bind("<Configure>", self.on_resize)
        self.after(100, self.trigger_resize)

    def on_resize(self, event):
        if event.width == 1 and event.height == 1:
            return 
        
        width = event.width
        
        if width < self.threshold and self.is_horizontal is not False:
            self.save_button.pack_forget()
            self.back_button.pack_forget()
            self.save_button.pack(side='top', fill='x', pady=(0, 8))
            self.back_button.pack(side='top', fill='x', pady=(8, 0))
            self.is_horizontal = False
        
        elif width >= self.threshold and self.is_horizontal is not True:
            self.save_button.pack_forget()
            self.back_button.pack_forget()
            self.save_button.pack(side='left', fill='x', expand=True, padx=(0, 8))
            self.back_button.pack(side='right', fill='x', expand=True, padx=(8, 0))
            self.is_horizontal = True
            
    def trigger_resize(self):
        self.on_resize(type('Event', (), {'width': self.winfo_width(), 'height': self.winfo_height()})())
        
    def refresh(self):
        self.listbox.delete(0, tk.END)
        self.q_text.delete("1.0", tk.END)
        self.a_text.delete("1.0", tk.END)
        self.selected = None
        for q in sorted(self.controller.flashcards.keys()):
            self.listbox.insert(tk.END, q[:60] + ("..." if len(q) > 60 else ""))
        self.is_horizontal = None
        self.after(50, self.trigger_resize)
        
    def load(self, event):
        try:
            sel_index = self.listbox.curselection()[0]
            keys = sorted(self.controller.flashcards.keys())
            self.selected = keys[sel_index]
            
            self.q_text.config(state=tk.NORMAL)
            self.q_text.delete("1.0", tk.END)
            self.q_text.insert("1.0", self.selected)
            self.q_text.config(state=tk.NORMAL) # Must be normal to allow editing
            
            self.a_text.config(state=tk.NORMAL)
            self.a_text.delete("1.0", tk.END)
            self.a_text.insert("1.0", self.controller.flashcards[self.selected])
            self.a_text.config(state=tk.NORMAL) # Must be normal to allow editing
        except IndexError:
            pass 
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load card for editing: {e}")

    def save(self):
        try:
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
            else:
                messagebox.showwarning("No Selection", "Please select a card to save.")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save card: {e}")

class DeletePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        tk.Label(self, text="Delete Flashcards", font=('Helvetica', 20, 'bold'),
                fg=COLOR_TEXT_LIGHT, bg=COLOR_SECONDARY).pack(pady=30)
        
        frame = tk.Frame(self, bg=COLOR_CARD_BG)
        frame.pack(fill='both', expand=True, padx=100, pady=30) 
        
        self.listbox = tk.Listbox(frame, font=('Helvetica', 12), borderwidth=1, relief="solid", bg="#f7f7f7", fg=COLOR_TEXT_DARK) 
        self.listbox.pack(fill='both', expand=True, padx=30, pady=(30, 15)) 
        
        btn_frame = tk.Frame(frame, bg=COLOR_CARD_BG)
        btn_frame.pack(fill='x', padx=30, pady=(15, 30)) 
        
        # --- NEW Delete All Button (Rounded) ---
        tk.Button(btn_frame, text="Delete All", font=('Helvetica', 10),
                 bg='#ef4444', fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=20, 
                 command=self.delete_all).pack(side='left', padx=(0, 8), anchor='s')
        
        # Separator frame to group the main buttons on the right
        main_btns_frame = tk.Frame(btn_frame, bg=COLOR_CARD_BG)
        main_btns_frame.pack(side='right', fill='x', expand=True)

        tk.Button(main_btns_frame, text="Delete Selected", font=('Helvetica', 13, 'bold'),
                 bg='#ef4444', fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=14, 
                 command=self.delete).pack(side='left', fill='x', expand=True, padx=(0, 8))

        tk.Button(main_btns_frame, text="Back", font=('Helvetica', 13, 'bold'),
                 bg='#6b7280', fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=14, 
                 command=lambda: controller.show_frame("MainMenu")).pack(side='right', fill='x', expand=True, padx=(8, 0))

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for q in sorted(self.controller.flashcards.keys()):
            self.listbox.insert(tk.END, q[:70] + ("..." if len(q) > 70 else ""))

    def delete(self):
        try:
            sel_index = self.listbox.curselection()[0]
            keys = sorted(self.controller.flashcards.keys())
            q = keys[sel_index]
            
            if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete this card?\n{q[:50]}...?"):
                del self.controller.flashcards[q]
                self.controller.save_flashcards()
                self.controller.refresh_main_menu_count()
                messagebox.showinfo("Success", "Card Deleted!")
                self.controller.show_frame("MainMenu")
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a card to delete.")
        except Exception as e:
            messagebox.showerror("Delete Error", f"Failed to delete card: {e}")

    def delete_all(self):
        """Deletes all flashcards after a strong confirmation."""
        card_count = len(self.controller.flashcards)
        if card_count == 0:
            messagebox.showinfo("Empty", "There are no flashcards to delete.")
            return

        confirm_msg = (
            f"⚠️ WARNING! You are about to delete ALL {card_count} flashcards. "
            "This action cannot be undone. Are you absolutely sure?"
        )
        
        if messagebox.askyesno("CONFIRM DELETE ALL", confirm_msg):
            self.controller.flashcards.clear()
            self.controller.save_flashcards()
            self.controller.refresh_main_menu_count()
            messagebox.showinfo("Success", f"Successfully deleted all {card_count} flashcards.")
            self.controller.show_frame("MainMenu")
        else:
            messagebox.showinfo("Canceled", "Deletion of all flashcards canceled.")
            
class PracticePage(BasePage):
    # --- STATE CONSTANTS ---
    QUESTION_STATE = 0
    ANSWER_STATE = 1
    
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.stats = StatTracker()
        self.current_state = self.QUESTION_STATE
        
        self.cards = []
        self.index = 0
        
        tk.Label(self, text="Practice Mode", font=('Helvetica', 20, 'bold'),
                fg=COLOR_TEXT_LIGHT, bg=COLOR_SECONDARY).pack(pady=30)
        
        stat_frame = tk.Frame(self, bg=COLOR_CARD_BG)
        stat_frame.pack(fill='x', padx=80, pady=(0, 15)) 
        
        self.progress = tk.Label(stat_frame, text="", font=('Helvetica', 12), bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK)
        self.progress.pack(side='left', padx=25, pady=12) 
        
        self.score_lbl = tk.Label(stat_frame, text="Score: 0", font=('Helvetica', 12, 'bold'),
                                  fg=COLOR_SUCCESS_GREEN, bg=COLOR_CARD_BG)
        self.score_lbl.pack(side='right', padx=25, pady=12) 
        
        card = tk.Frame(self, bg=COLOR_CARD_BG)
        card.pack(fill='both', expand=True, padx=80, pady=(0, 30))
        
        bottom_controls = tk.Frame(card, bg=COLOR_CARD_BG)
        bottom_controls.pack(side='bottom', fill='x', padx=40, pady=(15, 30)) 

        main_content = tk.Frame(card, bg=COLOR_CARD_BG)
        main_content.pack(side='top', fill='both', expand=True)

        # --- SCROLLABLE QUESTION TEXT ---
        tk.Label(main_content, text="Question:", font=('Helvetica', 14, 'bold'), bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK).pack(anchor='w', padx=20, pady=(20, 5))
        q_frame = tk.Frame(main_content, height=180, bg=COLOR_CARD_BG) 
        q_frame.pack(fill='x', padx=20)
        q_frame.pack_propagate(False) 
        q_scrollbar = tk.Scrollbar(q_frame)
        q_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ADDED padx and pady inside the Text widget
        self.question = tk.Text(q_frame, height=5, font=('Helvetica', 14, 'bold'), 
                                state=tk.DISABLED, wrap=tk.WORD, bg='#f7f7f7', fg=COLOR_TEXT_DARK,
                                yscrollcommand=q_scrollbar.set, borderwidth=1, relief="flat", highlightthickness=0,
                                padx=10, pady=10)
        self.question.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        q_scrollbar.config(command=self.question.yview)

        # --- SCROLLABLE ANSWER TEXT ---
        tk.Label(main_content, text="Answer:", font=('Helvetica', 14, 'bold'), bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK).pack(anchor='w', padx=20, pady=(20, 5))
        a_frame = tk.Frame(main_content, height=180, bg=COLOR_CARD_BG) 
        a_frame.pack(fill='x', padx=20, pady=(0, 20))
        a_frame.pack_propagate(False) 
        a_scrollbar = tk.Scrollbar(a_frame)
        a_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ADDED padx and pady inside the Text widget
        self.answer = tk.Text(a_frame, height=5, font=('Helvetica', 13), 
                              fg=COLOR_ACCENT, state=tk.DISABLED, wrap=tk.WORD, bg='#f7f7f7',
                              yscrollcommand=a_scrollbar.set, borderwidth=1, relief="flat", highlightthickness=0,
                              padx=10, pady=10)
        self.answer.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        a_scrollbar.config(command=self.answer.yview)
        
        # --- Controls ---
        
        self.show_btn = tk.Button(bottom_controls, text="Show Answer", font=('Helvetica', 13, 'bold'),
                                 bg=COLOR_ACCENT, fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=14,
                                 command=self.show_answer)
        self.show_btn.pack(fill='x', pady=(0, 10))
        
        self.btn_frame = tk.Frame(bottom_controls, bg=COLOR_CARD_BG)
        self.btn_frame.pack(fill='x')
        
        self.correct_btn = tk.Button(self.btn_frame, text="Correct", font=('Helvetica', 12, 'bold'),
                                     bg=COLOR_SUCCESS_GREEN, fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=12,
                                     command=self.correct)
        
        self.wrong_btn = tk.Button(self.btn_frame, text="Wrong", font=('Helvetica', 12, 'bold'),
                                   bg='#ef4444', fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=12,
                                   command=self.wrong)
        
        # Renamed next_btn to skip_btn for clarity in QUESTION_STATE
        self.skip_btn = tk.Button(bottom_controls, text="Skip Card", font=('Helvetica', 13, 'bold'),
                                 bg='#6b7280', fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=14,
                                 command=self.wrong) # Skips count as wrong/not correct
        self.skip_btn.pack(fill='x', pady=10)
        
        tk.Button(bottom_controls, text="Quit Practice", font=('Helvetica', 13, 'bold'),
                 bg=COLOR_PRIMARY_DARK, fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=14,
                 command=lambda: controller.show_frame("MainMenu")).pack(fill='x')
        
        self.threshold = 400
        self.is_horizontal = None
        self.bind("<Configure>", self.on_resize)
        self.after(100, self.trigger_resize)

    def trigger_resize(self):
        self.on_resize(type('Event', (), {'width': self.winfo_width(), 'height': self.winfo_height()})())
        
    def on_resize(self, event):
        if event.width == 1 and event.height == 1:
            return 
        
        width = event.width
        
        if width < self.threshold and self.is_horizontal is not False:
            self.correct_btn.pack_forget()
            self.wrong_btn.pack_forget()
            self.correct_btn.pack(side='top', fill='x', pady=(0, 8))
            self.wrong_btn.pack(side='top', fill='x', pady=(8, 0))
            self.is_horizontal = False
        
        elif width >= self.threshold and self.is_horizontal is not True:
            self.correct_btn.pack_forget()
            self.wrong_btn.pack_forget()
            self.correct_btn.pack(side='left', fill='x', expand=True, padx=(0, 8))
            self.wrong_btn.pack(side='right', fill='x', expand=True, padx=(8, 0))
            self.is_horizontal = True

    def _set_text(self, text_widget, content):
        """Helper to safely insert text into a read-only Text widget."""
        text_widget.config(state=tk.NORMAL)
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0", content)
        text_widget.config(state=tk.DISABLED)
        # Scroll to top
        text_widget.yview_moveto(0)

    def _set_controls(self, state):
        """State Machine: Configures buttons based on the current practice state."""
        self.current_state = state
        
        if state == self.QUESTION_STATE:
            # Only 'Show Answer' and 'Skip' are active before answering
            self.show_btn.config(state="normal", text="Show Answer")
            self.skip_btn.config(state="normal", text="Skip Card")
            self.correct_btn.config(state="disabled")
            self.wrong_btn.config(state="disabled")
        
        elif state == self.ANSWER_STATE:
            # Only 'Correct' and 'Wrong' are active after the answer is shown
            self.show_btn.config(state="disabled", text="Answer Shown")
            self.skip_btn.config(state="disabled", text="Skip Card") # Disable skip after answer is revealed
            self.correct_btn.config(state="normal")
            self.wrong_btn.config(state="normal")
        
    def refresh(self):
        # Start a new session
        self.cards = list(self.controller.flashcards.items())
        random.shuffle(self.cards)
        self.index = 0
        
        self.stats.reset(len(self.cards))
        self.score_lbl.config(text=self.stats.get_display())
        
        self.show_card()
        self.is_horizontal = None
        self.after(50, self.trigger_resize)
        
    def show_card(self):
        """Presents the next question card."""
        if self.index < len(self.cards):
            q, _ = self.cards[self.index]
            self._set_text(self.question, q) 
            self._set_text(self.answer, "") # Clear previous answer
            self.progress.config(text=f"Card {self.index + 1} of {len(self.cards)}")
            self._set_controls(self.QUESTION_STATE) # Set buttons for QUESTION_STATE
        else:
            self.finish()

    def show_answer(self):
        """Transitions from QUESTION_STATE to ANSWER_STATE."""
        if self.current_state == self.QUESTION_STATE:
            _, a = self.cards[self.index]
            self._set_text(self.answer, a)
            self._set_controls(self.ANSWER_STATE) # Set buttons for ANSWER_STATE

    def next_card(self):
        """Moves to the next card, regardless of whether it was correct or wrong."""
        self.index += 1
        self.show_card()

    def correct(self):
        """Handles a correct answer and moves to the next card."""
        if self.current_state == self.ANSWER_STATE:
            self.stats.increment_score()
            self.score_lbl.config(text=self.stats.get_display())
            self.next_card()

    def wrong(self):
        """Handles a wrong or skipped answer and moves to the next card."""
        # This function can be called from QUESTION_STATE (via Skip) or ANSWER_STATE (via Wrong)
        self.next_card()

    def finish(self):
        """Ends the practice session."""
        pct = self.stats.get_percentage()
        score = self.stats.get_score()
        total = self.stats.get_total_cards()
            
        messagebox.showinfo("Practice Complete!", 
                          f"You finished your session!\nScore: {score}/{total} ({pct}%)")
        self.controller.show_frame("MainMenu")

if __name__ == "__main__":
    app = FlashcardApp()
    app.mainloop()