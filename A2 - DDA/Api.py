import tkinter as tk
from tkinter import messagebox
import requests
import random
import html

class TriviaQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Trivia Quiz")
        self.questions = []
        self.current_index = 0
        self.correct_answers = 0

        # UI setup
        self.question_label = tk.Label(root, text="", font=("Helvetica", 14), wraplength=400)
        self.question_label.pack(pady=20)

        self.answer_frame = tk.Frame(root)
        self.answer_frame.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Quiz", command=self.start_quiz)
        self.start_button.pack(pady=20)

    def fetch_trivia(self):
        try:
            response = requests.get('https://opentdb.com/api.php?amount=10&type=multiple')
            response.raise_for_status()
            data = response.json()
            return data['results'] if data['response_code'] == 0 else None
        except requests.RequestException as e:
            print(f"Error fetching trivia: {e}")
            return None

    def start_quiz(self):
        self.questions = self.fetch_trivia()
        self.current_index = 0
        self.correct_answers = 0

        if self.questions:
            self.start_button.pack_forget()
            self.show_question()
        else:
            messagebox.showerror("Error", "Failed to fetch trivia questions.")

    def show_question(self):
        self.clear_answers()
        if self.current_index < len(self.questions):
            q_data = self.questions[self.current_index]
            question_text = html.unescape(q_data['question'])
            correct = html.unescape(q_data['correct_answer'])
            choices = [html.unescape(ans) for ans in q_data['incorrect_answers']] + [correct]
            random.shuffle(choices)

            self.question_label.config(text=f"Q{self.current_index + 1}: {question_text}")
            for choice in choices:
                btn = tk.Button(self.answer_frame, text=choice,
                                command=lambda c=choice, corr=correct: self.check_answer(c, corr))
                btn.pack(pady=5, fill='x')
        else:
            self.end_quiz()

    def check_answer(self, selected, correct):
        for widget in self.answer_frame.winfo_children():
            widget.config(state=tk.DISABLED)

        if selected == correct:
            self.correct_answers += 1
            messagebox.showinfo("Correct", "Well done! Your answer is correct.")
        else:
            messagebox.showinfo("Incorrect", f"Oops! The correct answer was: {correct}")

        self.current_index += 1
        self.root.after(500, self.show_question)

    def clear_answers(self):
        for widget in self.answer_frame.winfo_children():
            widget.destroy()

    def end_quiz(self):
        score_msg = f"You answered {self.correct_answers} out of {len(self.questions)} questions correctly."
        messagebox.showinfo("Quiz Complete", score_msg)
        self.start_button.config(text="Restart Quiz")
        self.start_button.pack(pady=20)
        self.question_label.config(text="")
        self.clear_answers()

if __name__ == "__main__":
    root = tk.Tk()
    app = TriviaQuiz(root)
    root.mainloop()
