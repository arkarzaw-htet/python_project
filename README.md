Here is the updated README file, now including the instructions for cloning the repository.

-----

# 🎯 Flashcard Master

This is a simple, no-fuss flashcard app built with Python.

It's designed to be a straightforward, digital version of traditional index cards for studying. The best part? It runs **100% locally** on your computer. You don't need an internet connection, and you don't have to worry about a web server losing your data. Your flashcards are always safe and accessible right on your machine.

## ✨ Features

  * **Add & Save:** Quickly create new flashcards with a question and an answer.
  * **Edit:** Easily fix typos or update your existing cards.
  * **Delete:** Clean up your deck by deleting old cards one by one (or all at once\!).
  * **Practice Mode:** A built-in study session\! Cards are shuffled, and you can track your score as you go.
  * **Persistent Storage:** All your cards are automatically saved to a `flashcards.json` file in the same folder, so you'll never lose your deck.

## 🚀 Getting Started (How to Run)

To run this application, all you need is **Python 3**. (The `tkinter` library it uses is included with most Python installations).

### Option 1: Clone the Repository (Recommended)

If you have [Git](https://git-scm.com/) installed, you can clone this repository.

1.  Open your terminal or command prompt.

2.  Navigate to the directory where you want to save the project.

3.  Run the following command:

    ```bash
    git clone https://github.com/arkarzaw-htet/FlashcardMaster.git
    ```

4.  This will create a new `FlashcardMaster` folder. Move into it:

    ```bash
    cd FlashcardMaster
    ```

### Option 2: Download the Code

If you don't use Git, you can just save the `main.py` (or `flashcard_app.py`) file from this repository onto your computer.

### How to Run the App

After you have the files (from cloning or downloading):

1.  Open your terminal (if you're not already there).

2.  Make sure you are in the project's directory.

3.  Run the application using Python:

    ```bash
    python flashcard_app.py
    ```

The app window should pop right up, and you're ready to go\! A `flashcards.json` file will be automatically created in the same folder to store your cards.

## 📚 How to Use the App

The app is built around the **Main Menu**. From here, you can navigate to all the other sections.

### Adding a New Card

1.  From the Main Menu, click **"Add Flashcard"**.
2.  Type your question into the top "Question:" box.
3.  Type your answer into the bottom "Answer:" box.
4.  Click the **"Add"** button.
5.  You'll be taken back to the Main Menu, and the "Total Cards" count will be updated.

### Practice Mode (The Fun Part\!)

1.  Click **"Practice Mode"**.
2.  The app will shuffle your entire deck and show you the first question.
3.  Think of the answer, then click **"Show Answer"**.
4.  Be honest\! Click **"Correct"** or **"Wrong"** based on your answer.
      * You can also click **"Skip Card"** before revealing the answer, which counts as wrong.
5.  Your score is tracked in the green text at the top.
6.  When you've gone through all the cards, a popup will show your final score, and you'll be returned to the Main Menu.

### Editing a Card

1.  Click **"Edit Flashcards"**.
2.  On the left, you'll see a list of all your questions. **Click the card** you want to edit.
3.  The card's current question and answer will appear in the text boxes on the right.
4.  Make your changes directly in the boxes.
5.  Click the **"Save"** button.

### Deleting Cards

1.  Click **"Delete Flashcards"**.
2.  You'll see a list of all your cards.
3.  **Click the card** you want to remove.
4.  Click the **"Delete Selected"** button.
5.  A confirmation box will pop up. Click "Yes" to permanently delete it.

> **⚠️ Be Careful:** There is also a **"Delete All"** button. This will wipe out your *entire* deck. It will ask you to confirm, but once they're gone, they're gone\!