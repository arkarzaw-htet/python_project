# ============================================================= #
# Python Individual Project, Year 1, Semester 1                 #
#                                                               #
# Project: Flashcard Master                                     #
#                                                               # 
# Repository: https://github.com/arkarzaw-htet/FlashcardMaster  #
# Written by: Arkar Zaw Htet(68011284)                          #
# ============================================================= #


import random
import json
import os
from abc import ABC, abstractmethod  # We import ABC tools to create an "abstract" base class

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

# --- App-wide Color & Style Constants ---
COLOR_PRIMARY_DARK = '#36394E'  
COLOR_SECONDARY = '#454866'     
COLOR_ACCENT = "#0F1BA3"        
COLOR_SUCCESS_GREEN = "#00be20" 
COLOR_TEXT_LIGHT = 'white'
COLOR_TEXT_DARK = '#2C2F43'     
COLOR_CARD_BG = "#8ece98"       


BUTTON_BORDER_WIDTH = 4 
BUTTON_RELIEF = 'groove' 

# --- Flashcard Data Class ---
# This class is a "blueprint" for our flashcard data.
# It just holds a question and an answer.
class Flashcard(object):
    """Represents a single flashcard."""
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def to_dict(self):
        """Converts the Flashcard object to a dictionary so it can be saved to JSON."""
        return {
            'question': self.question,
            'answer': self.answer
        }
    
    # We removed the from_dict classmethod.
    # The logic for loading from a dict is now in FlashcardApp.load_flashcards()

    def __repr__(self):
        """A helper for debugging. Lets us print a Flashcard object and see something useful."""
        return f"Flashcard(q='{self.question[:20]}...')"


# --- COMPOSITION: StatTracker Class ---
# This class is a good example of "Composition".
# Instead of the PracticePage trying to manage stats *and* UI,
# we "compose" it by giving it a separate, dedicated StatTracker object.
class StatTracker(object):
    def __init__(self):
        self._score = 0
        self._total_cards = 0

    def get_score(self):
        return self._score

    def get_total_cards(self):
        return self._total_cards

    def reset(self, total_cards):
        self._score = 0
        self._total_cards = total_cards

    def increment_score(self):
        self._score += 1

    def get_percentage(self):
        try:
            return round((self._score / self._total_cards) * 100, 1)
        except ZeroDivisionError:
            return 0.0

    def get_display(self):
        return f"Score: {self._score}/{self._total_cards}"


# --- Main Application Controller ---
# This class *is* the main window (it inherits from tk.Tk).
# It controls which "page" (frame) is currently visible.
class FlashcardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flashcard Master")
        self.configure(bg=COLOR_PRIMARY_DARK) 

        # --- Prevent "blank window flash" ---
        # 1. Hide the window completely before it's drawn.
        self.withdraw() 
        
        window_width = 1000 
        window_height = 900 
        
        # This makes sure Tkinter has processed initial sizes
        self.update_idletasks() 

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Simple math to center the window
        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))

        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        
        self.data_file = "flashcards.json"
        # self.flashcards is NOW A LIST of Flashcard objects
        self.flashcards = self.load_flashcards() 
        
        self.title_font = font.Font(family="Helvetica", size=28, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=14, weight="bold")
        
        # --- Frame Management ---
        # This 'container' frame holds all our "pages".
        # We will stack all pages in here and then use .tkraise() to show one.
        container = tk.Frame(self, bg=COLOR_SECONDARY) 
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Create all the pages (frames) and store them in the self.frames dictionary
        main_menu = MainMenu(parent=container, controller=self)
        self.frames["MainMenu"] = main_menu
        main_menu.grid(row=0, column=0, sticky="nsew")
 
 
        add_page = AddPage(parent=container, controller=self)
        self.frames["AddPage"] = add_page
        add_page.grid(row=0, column=0, sticky="nsew")
 
 
        edit_page = EditPage(parent=container, controller=self)
        self.frames["EditPage"] = edit_page
        edit_page.grid(row=0, column=0, sticky="nsew")
 
 
        delete_page = DeletePage(parent=container, controller=self)
        self.frames["DeletePage"] = delete_page
        delete_page.grid(row=0, column=0, sticky="nsew")
 
 
        practice_page = PracticePage(parent=container, controller=self)
        self.frames["PracticePage"] = practice_page
        practice_page.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")
        
        # 2. Now that everything is built and ready, un-hide the window.
        self.deiconify()
        
    def show_frame(self, page_name):
        """Shows the frame with the given page_name."""
        frame = self.frames[page_name]
        # Call the page's own 'refresh' method *before* showing it
        frame.refresh() 
        # This brings the desired frame to the front of the stack
        frame.tkraise()

    def show_frame_if_cards(self, page_name):
        # A simple check to stop users from practicing/editing/deleting 0 cards
        if not self.flashcards:
            messagebox.showwarning("No Cards", "Create flashcards first.")
            return
        self.show_frame(page_name)

    def refresh_main_menu_count(self):
        # A helper method to make sure the main menu card count is always accurate
        main_menu_frame = self.frames.get("MainMenu")
        if main_menu_frame:
            main_menu_frame.refresh()

    def get_default_cards(self):
        """Returns a list of dictionaries for creating Flashcard objects."""
        return [
            {"question": "What is the capital of France?", "answer": "Paris"},
            {"question": "What does HTML stand for?", "answer": "HyperText Markup Language"},
            {"question": "Who painted the Mona Lisa?", "answer": "Leonardo da Vinci"}
        ]

    def load_flashcards(self):
        """
        Loads flashcards from JSON.
        - Logic from the old `from_dict` method is now here.
        - Automatically migrates old dict-based {q: a} format.
        """
        if not os.path.exists(self.data_file):
            # No file, create defaults from list of dicts
            default_data = self.get_default_cards()
            
            # Manually create Flashcard objects
            loaded_cards = []
            for item in default_data:
                # item.get() is safer than item[] as it won't crash if a key is missing
                loaded_cards.append(
                    Flashcard(
                        question=item.get('question', ''),
                        answer=item.get('answer', '')
                    )
                )
            self.save_flashcards(loaded_cards) # Save the new list[Flashcard] format
            return loaded_cards
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            loaded_cards = []
            migrated = False

            if isinstance(data, dict):
                # --- MIGRATION LOGIC ---
                # This handles the old {question: answer} format
                loaded_cards = [Flashcard(q, a) for q, a in data.items()]
                migrated = True
            elif isinstance(data, list):
                # This handles the new format (a list of dicts)
                # We manually do the work of creating Flashcard objects
                for item in data:
                    loaded_cards.append(
                        Flashcard(
                            question=item.get('question', ''),
                            answer=item.get('answer', '')
                        )
                    )
            else:
                # File is corrupt or in a format we don't recognize
                messagebox.showerror("Load Error", "Unrecognized file format. Loading defaults.")
                raise json.JSONDecodeError("Data is not a valid list or dict", "", 0)

            if migrated:
                # If we migrated the old format, save the file back in the *new* format
                messagebox.showinfo("Migration", "Your flashcards have been updated to the new format.")
                self.save_flashcards(loaded_cards) 

            return loaded_cards

        except (json.JSONDecodeError, IOError, Exception) as e:
            messagebox.showerror("Load Error", f"Failed to read '{self.data_file}'. Error: {e}. Loading defaults.")
            # If anything fails, load defaults so the app doesn't crash
            default_data = self.get_default_cards()
            loaded_cards = []
            for item in default_data:
                loaded_cards.append(
                    Flashcard(
                        question=item.get('question', ''),
                        answer=item.get('answer', '')
                    )
                )
            self.save_flashcards(loaded_cards) # Save defaults
            return loaded_cards


    def save_flashcards(self, cards=None):
        """Saves the given list of Flashcard objects to the JSON file."""
        cards_to_save = cards if cards is not None else self.flashcards
        
        # Convert our list[Flashcard] back into a list[dict]
        # The 'card.to_dict()' method comes from our Flashcard class
        data_to_save = [card.to_dict() for card in cards_to_save]
        
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                # json.dump writes the data to the file
                # indent=2 makes the file human-readable (pretty-prints it)
                json.dump(data_to_save, f, indent=2, ensure_ascii=False)
        except PermissionError:
            messagebox.showerror("Save Error", f"Failed to save flashcards to '{self.data_file}'. Check file permissions.")
        except IOError as e:
            messagebox.showerror("Save Error", f"File I/O error occurred during save: {e}")
        except Exception as e:
             messagebox.showerror("Save Error", f"An unexpected error occurred during save: {e}")


# --- Abstract Base Page ---
# This is an "abstract" class, like a template for our other pages.
# It says: "Any class that inherits from me *must* be a tk.Frame
# and *must* have a 'refresh' method."
class BasePage(tk.Frame, ABC):
    """Abstract base class for all pages, requires a refresh method."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_SECONDARY) 
        self.controller = controller

    @abstractmethod
    def refresh(self):
        """Called by the controller when the frame is shown."""
        pass


# --- Mixin Class ---
# A "Mixin" is a class that adds a specific piece of functionality.
# It's not meant to be used on its own.
# This one adds a `create_form_fields` method to any class that inherits it.
# Notice AddPage and EditPage both use this to stay consistent.
class FormMixin(object):
    """Mixin to create standard Question and Answer text fields with internal padding."""
    def create_form_fields(self, parent_frame):
        tk.Label(parent_frame, text="Question:", font=('Helvetica', 12, 'bold'),
                bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK).pack(anchor='w', padx=30, pady=(20, 5)) 
        
        q_text = tk.Text(parent_frame, height=5, font=('Helvetica', 11), bg=COLOR_CARD_BG, 
                         fg=COLOR_TEXT_DARK, padx=10, pady=10, borderwidth=1, relief="solid")
        q_text.pack(fill='x', padx=30)
        
        tk.Label(parent_frame, text="Answer:", font=('Helvetica', 12, 'bold'),
                bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK).pack(anchor='w', padx=30, pady=(20, 5)) 
        
        a_text = tk.Text(parent_frame, height=5, font=('Helvetica', 11), bg=COLOR_CARD_BG, 
                         fg=COLOR_TEXT_DARK, padx=10, pady=10, borderwidth=1, relief="solid")
        a_text.pack(fill='x', padx=30, pady=(0, 30)) 
        
        return q_text, a_text

# --- Page Classes ---

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
        # This is called by show_frame() to update the card count
        count = len(self.controller.flashcards)
        self.count_label.config(text=f"Total Cards: {count}")

# AddPage inherits from BasePage and our FormMixin
class AddPage(BasePage, FormMixin):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        tk.Label(self, text="Add New Flashcard", font=('Helvetica', 20, 'bold'), 
                fg=COLOR_TEXT_LIGHT, bg=COLOR_SECONDARY).pack(pady=30) 
        
        frame = tk.Frame(self, bg=COLOR_CARD_BG) 
        frame.pack(fill='both', expand=True, padx=80, pady=30) 
        
        # Use the Mixin to create the Q/A text boxes
        self.q_text, self.a_text = self.create_form_fields(frame)
        
        self.btn_frame = tk.Frame(frame, bg=COLOR_CARD_BG) 
        self.btn_frame.pack(fill='x', padx=30, side='bottom', pady=(0, 30)) 
        
        self.add_button = tk.Button(self.btn_frame, text="Add", font=('Helvetica', 13, 'bold'), bg=COLOR_SUCCESS_GREEN,
                 fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=12, command=self.add) 
        
        self.back_button = tk.Button(self.btn_frame, text="Back", font=('Helvetica', 13, 'bold'), bg='#6b7280',
                 fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=12, 
                 command=lambda: controller.show_frame("MainMenu")) 
        
        self.threshold = 400 
        self.is_horizontal = None # Used to track button layout state
        
        # --- Responsive Resize Logic ---
        # 1. Bind the "<Configure>" event (which fires on resize) to our on_resize method
        self.bind("<Configure>", self.on_resize)
        # 2. Schedule trigger_resize to run *after* the window is fully drawn
        self.after(100, self.trigger_resize)
        
    def trigger_resize(self):
        # This helper function just fakes an 'event' object
        # It's needed to run the resize logic when the page first loads
        self.on_resize(type('Event', (), {'width': self.winfo_width(), 'height': self.winfo_height()})())
        
    def on_resize(self, event):
        # This method is called every time the window is resized
        if event.width == 1 and event.height == 1:
            return # Ignore the initial tiny "1x1" event
        
        width = event.width
        
        # If the window is narrow and buttons aren't already stacked...
        if width < self.threshold and self.is_horizontal is not False:
            self.add_button.pack_forget()
            self.back_button.pack_forget()
            # Stack them vertically
            self.add_button.pack(side='top', fill='x', pady=(0, 8))
            self.back_button.pack(side='top', fill='x', pady=(8, 0))
            self.is_horizontal = False
        
        # If window is wide and buttons aren't already side-by-side...
        elif width >= self.threshold and self.is_horizontal is not True:
            self.add_button.pack_forget()
            self.back_button.pack_forget()
            # Place them side-by-side
            self.add_button.pack(side='left', fill='x', expand=True, padx=(0, 8))
            self.back_button.pack(side='right', fill='x', expand=True, padx=(8, 0))
            self.is_horizontal = True

    def refresh(self):
        self.q_text.delete("1.0", tk.END)
        self.a_text.delete("1.0", tk.END)
        self.is_horizontal = None # Reset layout state
        self.after(50, self.trigger_resize) # Re-run resize check when page is shown
        
    def add(self):
        """Creates a Flashcard object and appends it to the main list."""
        try:
            q = self.q_text.get("1.0", tk.END).strip()
            a = self.a_text.get("1.0", tk.END).strip()
            if q and a:
                # Create a new Flashcard object
                new_card = Flashcard(question=q, answer=a)
                # Append it to the controller's main list
                self.controller.flashcards.append(new_card)
                
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
        self.selected_card = None # Stores the actual Flashcard object being edited
        
        # --- Listbox-to-Object Mapping ---
        # This is the key to not needing UUIDs.
        # This list will store the *actual* Flashcard objects
        # in the *exact same order* as they appear in the listbox.
        self.displayed_cards = [] 
        
        tk.Label(self, text="Edit Flashcards", font=('Helvetica', 20, 'bold'),
                fg=COLOR_TEXT_LIGHT, bg=COLOR_SECONDARY).pack(pady=30)
        
        frame = tk.Frame(self, bg=COLOR_CARD_BG)
        frame.pack(fill='both', expand=True, padx=80, pady=30)
        
        self.listbox = tk.Listbox(frame, font=('Helvetica', 12), borderwidth=1, relief="solid", bg="#f7f7f7", fg=COLOR_TEXT_DARK)
        self.listbox.pack(side='left', fill='both', expand=True, padx=(30, 15), pady=30)
        # Bind the listbox selection event to our 'load' method
        self.listbox.bind("<<ListboxSelect>>", self.load)

        right = tk.Frame(frame, bg=COLOR_CARD_BG)
        right.pack(side='right', fill='both', expand=True, padx=(15, 30), pady=30)
        
        # Use the Mixin to create the Q/A text boxes
        self.q_text, self.a_text = self.create_form_fields(right)

        self.btn_frame = tk.Frame(right, bg=COLOR_CARD_BG)
        self.btn_frame.pack(fill='x', side='bottom', pady=(0, 30))
        
        self.save_button = tk.Button(self.btn_frame, text="Save", font=('Helvetica', 13, 'bold'), bg='#f59e0b',
                 fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=12, command=self.save)

        self.back_button = tk.Button(self.btn_frame, text="Back", font=('Helvetica', 13, 'bold'), bg='#6b7280',
                 fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=12, 
                 command=lambda: controller.show_frame("MainMenu"))
        
        # This page uses the same responsive resize logic as AddPage
        self.threshold = 400
        self.is_horizontal = None
        self.bind("<Configure>", self.on_resize)
        self.after(100, self.trigger_resize)

    def on_resize(self, event):
        # This logic is identical to AddPage's resize
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
        """Populates listbox and the self.displayed_cards mapping list."""
        self.listbox.delete(0, tk.END)
        self.q_text.delete("1.0", tk.END)
        self.a_text.delete("1.0", tk.END)
        self.selected_card = None
        self.displayed_cards = [] # Clear the mapping
        
        # Sort cards by question to give the user a consistent order
        sorted_cards = sorted(self.controller.flashcards, key=lambda card: card.question)
        
        for card in sorted_cards:
            # Add card to our internal list
            self.displayed_cards.append(card)
            # Add *only* the question text to the *visible* listbox
            q = card.question
            self.listbox.insert(tk.END, q[:60] + ("..." if len(q) > 60 else ""))

        self.is_horizontal = None
        self.after(50, self.trigger_resize)
        
    def load(self, event):
        """Gets the Flashcard object from the selected index."""
        try:
            sel_index = self.listbox.curselection()[0]
            
            # --- This is the mapping in action ---
            # Get the actual Flashcard object from our internal list
            # using the index from the visible listbox.
            self.selected_card = self.displayed_cards[sel_index]
            
            # Now, populate the text boxes with the object's data
            self.q_text.config(state=tk.NORMAL)
            self.q_text.delete("1.0", tk.END)
            self.q_text.insert("1.0", self.selected_card.question)
            
            self.a_text.config(state=tk.NORMAL)
            self.a_text.delete("1.0", tk.END)
            self.a_text.insert("1.0", self.selected_card.answer)
        except IndexError:
            pass # Ignore clicks on an empty list
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load card for editing: {e}")

    def save(self):
        """Updates the attributes of the selected Flashcard object."""
        try:
            if self.selected_card:
                new_q = self.q_text.get("1.0", tk.END).strip()
                new_a = self.a_text.get("1.0", tk.END).strip()
                if not (new_q and new_a):
                    messagebox.showwarning("Error", "Both fields required!")
                    return
                    
                # --- This is the new, simple logic ---
                # We just update the object's attributes.
                # Since the controller's list holds this *exact* object,
                # the changes are saved automatically when we call save_flashcards().
                self.selected_card.question = new_q
                self.selected_card.answer = new_a
                
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
        
        # This page uses the same listbox-to-object mapping as EditPage
        self.displayed_cards = [] 

        tk.Label(self, text="Delete Flashcards", font=('Helvetica', 20, 'bold'),
                fg=COLOR_TEXT_LIGHT, bg=COLOR_SECONDARY).pack(pady=30)
        
        frame = tk.Frame(self, bg=COLOR_CARD_BG)
        frame.pack(fill='both', expand=True, padx=100, pady=30) 
        
        self.listbox = tk.Listbox(frame, font=('Helvetica', 12), borderwidth=1, relief="solid", bg="#f7f7f7", fg=COLOR_TEXT_DARK) 
        self.listbox.pack(fill='both', expand=True, padx=30, pady=(30, 15)) 
        
        btn_frame = tk.Frame(frame, bg=COLOR_CARD_BG)
        btn_frame.pack(fill='x', padx=30, pady=(15, 30)) 
        
        tk.Button(btn_frame, text="Delete All", font=('Helvetica', 10),
                 bg='#ef4444', fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=20, 
                 command=self.delete_all).pack(side='left', padx=(0, 8), anchor='s')
        
        main_btns_frame = tk.Frame(btn_frame, bg=COLOR_CARD_BG)
        main_btns_frame.pack(side='right', fill='x', expand=True)

        tk.Button(main_btns_frame, text="Delete Selected", font=('Helvetica', 13, 'bold'),
                 bg='#ef4444', fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=14, 
                 command=self.delete).pack(side='left', fill='x', expand=True, padx=(0, 8))

        tk.Button(main_btns_frame, text="Back", font=('Helvetica', 13, 'bold'),
                 bg='#6b7280', fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=14, 
                 command=lambda: controller.show_frame("MainMenu")).pack(side='right', fill='x', expand=True, padx=(8, 0))

    def refresh(self):
        """Populates listbox and the self.displayed_cards mapping list."""
        self.listbox.delete(0, tk.END)
        self.displayed_cards = [] # Clear the mapping
        
        sorted_cards = sorted(self.controller.flashcards, key=lambda card: card.question)
        
        for card in sorted_cards:
            self.displayed_cards.append(card)
            q = card.question
            self.listbox.insert(tk.END, q[:70] + ("..." if len(q) > 70 else ""))

    def delete(self):
        """Finds the Flashcard object by index and removes it."""
        try:
            sel_index = self.listbox.curselection()[0]
            # Get the actual Flashcard object to delete using the index
            card_to_delete = self.displayed_cards[sel_index]
            
            q_preview = card_to_delete.question[:50]
            
            if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete this card?\n{q_preview}...?"):
                # We can remove the object directly from the controller's list
                # because `card_to_delete` is a reference to that *exact* object.
                self.controller.flashcards.remove(card_to_delete)
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
            self.controller.flashcards.clear() # .clear() is a standard list method
            self.controller.save_flashcards()
            self.controller.refresh_main_menu_count()
            messagebox.showinfo("Success", f"Successfully deleted all {card_count} flashcards.")
            self.controller.show_frame("MainMenu")
        else:
            messagebox.showinfo("Canceled", "Deletion of all flashcards canceled.")
            
class PracticePage(BasePage):
    # --- STATE CONSTANTS ---
    # Using constants makes the state machine logic easier to read
    QUESTION_STATE = 0
    ANSWER_STATE = 1
    
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # This page "has a" StatTracker. (Composition)
        self.stats = StatTracker()
        self.current_state = self.QUESTION_STATE
        
        self.cards = [] # This will be a list of Flashcard objects
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
        
        # --- pack_propagate(False) ---
        # This is a key command!
        # It tells the 'q_frame' NOT to shrink to fit its contents (the Text widget).
        # Instead, the frame will *force* its own height (180px)
        # and the Text widget will have to fit inside it (which is why we need the scrollbar).
        q_frame.pack_propagate(False) 
        
        q_scrollbar = tk.Scrollbar(q_frame)
        q_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
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
        # We use pack_propagate(False) here too for the same reason.
        a_frame.pack_propagate(False) 
        a_scrollbar = tk.Scrollbar(a_frame)
        a_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
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
        
        self.skip_btn = tk.Button(bottom_controls, text="Skip Card", font=('Helvetica', 13, 'bold'),
                                 bg='#6b7280', fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=14,
                                 command=self.wrong) # Skip just calls wrong()
        self.skip_btn.pack(fill='x', pady=10)
        
        tk.Button(bottom_controls, text="Quit Practice", font=('Helvetica', 13, 'bold'),
                 bg=COLOR_PRIMARY_DARK, fg=COLOR_TEXT_LIGHT, relief=BUTTON_RELIEF, bd=BUTTON_BORDER_WIDTH, pady=14,
                 command=lambda: controller.show_frame("MainMenu")).pack(fill='x')
        
        # This page also uses the responsive resize logic
        self.threshold = 400
        self.is_horizontal = None
        self.bind("<Configure>", self.on_resize)
        self.after(100, self.trigger_resize)

    def trigger_resize(self):
        self.on_resize(type('Event', (), {'width': self.winfo_width(), 'height': self.winfo_height()})())
        
    def on_resize(self, event):
        # This resize logic only affects the 'Correct' and 'Wrong' buttons
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
        # We have to set state to NORMAL to change the text...
        text_widget.config(state=tk.NORMAL)
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0", content)
        # ...and then set it back to DISABLED so the user can't type in it.
        text_widget.config(state=tk.DISABLED)
        # Scroll to top
        text_widget.yview_moveto(0)

    def _set_controls(self, state):
        """
        This is a simple "State Machine".
        It manages the UI based on whether we are in QUESTION_STATE or ANSWER_STATE.
        """
        self.current_state = state
        
        if state == self.QUESTION_STATE:
            # User is looking at a question
            self.show_btn.config(state="normal", text="Show Answer")
            self.skip_btn.config(state="normal", text="Skip Card")
            self.correct_btn.config(state="disabled")
            self.wrong_btn.config(state="disabled")
        
        elif state == self.ANSWER_STATE:
            # User is looking at the answer
            self.show_btn.config(state="disabled", text="Answer Shown")
            self.skip_btn.config(state="disabled") # Can't skip after seeing answer
            self.correct_btn.config(state="normal")
            self.wrong_btn.config(state="normal")
        
    def refresh(self):
        """Creates a shuffled copy of the list of Flashcard objects."""
        # Start a new session
        # `list()` creates a new *shallow copy* of the controller's list.
        # This is important so `random.shuffle` doesn't mess up the original list.
        self.cards = list(self.controller.flashcards) 
        random.shuffle(self.cards)
        self.index = 0
        
        self.stats.reset(len(self.cards)) # Reset the stat tracker
        self.score_lbl.config(text=self.stats.get_display())
        
        self.show_card()
        self.is_horizontal = None
        self.after(50, self.trigger_resize)
        
    def show_card(self):
        """Pulls question from the Flashcard object."""
        if self.index < len(self.cards):
            # Get the Flashcard object for the current index
            card = self.cards[self.index]
            
            self._set_text(self.question, card.question) # Get question from object
            self._set_text(self.answer, "") # Clear previous answer
            self.progress.config(text=f"Card {self.index + 1} of {len(self.cards)}")
            self._set_controls(self.QUESTION_STATE) # Set buttons for question state
        else:
            self.finish() # No more cards!

    def show_answer(self):
        """Pulls answer from the Flashcard object."""
        if self.current_state == self.QUESTION_STATE:
            card = self.cards[self.index]
            self._set_text(self.answer, card.answer) # Get answer from object
            self._set_controls(self.ANSWER_STATE) # Set buttons for answer state

    def next_card(self):
        """Moves to the next card index and shows it."""
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
        # This function works for both "Wrong" and "Skip"
        self.next_card()

    def finish(self):
        """Ends the practice session."""
        pct = self.stats.get_percentage()
        score = self.stats.get_score()
        total = self.stats.get_total_cards()
            
        messagebox.showinfo("Practice Complete!", 
                          f"You finished your session!\nScore: {score}/{total} ({pct}%)")
        self.controller.show_frame("MainMenu")

# --- Run the Application ---
# This is a standard Python convention.
# The code inside this `if` block will only run
# if this file is executed directly (not if it's imported by another file).
if __name__ == "__main__":
    app = FlashcardApp()
    app.mainloop() # This starts the Tkinter event loop