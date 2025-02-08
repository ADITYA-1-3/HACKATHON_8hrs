from PyQt5 import QtWidgets, QtCore
import sys
import pyttsx3
import speech_recognition as sr
import sqlite3
from datetime import datetime
import re
from PyQt5.QtCore import QDate

class ToDoApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        self.create_table()
        self.initUI()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT,
                date TEXT,
                time TEXT,
                deadline TEXT,
                completed INTEGER
            )
        """)
        self.conn.commit()

    def initUI(self):
        self.setWindowTitle("Voice-Enabled To-Do List")
        self.setGeometry(100, 100, 500, 500)

        # Main Layout
        layout = QtWidgets.QVBoxLayout()

        # Title Label Styling
        self.title_label = QtWidgets.QLabel("To-Do List")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFFFFF; background-color: #007BFF; padding: 10px;")
        layout.addWidget(self.title_label)

        # Task Entry Styling
        self.task_entry = QtWidgets.QLineEdit()
        self.task_entry.setPlaceholderText("Enter a task or use voice input...")
        self.task_entry.setStyleSheet("padding: 10px; border: 2px solid #007BFF; border-radius: 5px; font-size: 14px;")
        layout.addWidget(self.task_entry)

        # Voice Input Button Styling
        self.voice_button = QtWidgets.QPushButton("Voice Input")
        self.voice_button.setStyleSheet("background-color: #28A745; color: white; padding: 10px; border-radius: 5px; font-size: 14px;")
        self.voice_button.clicked.connect(self.voice_input)
        layout.addWidget(self.voice_button)

        # Voice Date Search Button Styling
        self.voice_date_button = QtWidgets.QPushButton("Voice Date Search")
        self.voice_date_button.setStyleSheet("background-color: #FFC107; color: white; padding: 10px; border-radius: 5px; font-size: 14px;")
        self.voice_date_button.clicked.connect(self.voice_date_search)
        layout.addWidget(self.voice_date_button)

        # Calendar Widget Styling
        self.calendar = QtWidgets.QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: #F8F9FA;
                border: 1px solid #007BFF;
                border-radius: 5px;
            }
            QCalendarWidget QAbstractItemView {
                background-color: #FFFFFF;
                selection-background-color: #007BFF;
                selection-color: white;
                font-size: 14px;
            }
            QCalendarWidget::item {
                font-size: 14px;
                color: #333333;
            }
            QCalendarWidget QWidget {
                font-size: 16px;
                color: #333333;
            }
            QCalendarWidget QToolButton {
                background-color: #007BFF;
                color: white;
                padding: 5px;
                border-radius: 5px;
                font-weight: bold;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #0056b3;
            }
            QCalendarWidget QToolButton:pressed {
                background-color: #003f6a;
            }
        """)
        self.calendar.selectionChanged.connect(self.load_tasks)
        layout.addWidget(self.calendar)

        # Deadline Label Styling
        self.deadline_label = QtWidgets.QLabel("Deadline:")
        self.deadline_label.setStyleSheet("font-size: 14px; color: #333333; padding: 5px;")
        layout.addWidget(self.deadline_label)

        # Deadline DateEdit Styling
        self.deadline_input = QtWidgets.QDateEdit()
        self.deadline_input.setCalendarPopup(True)
        self.deadline_input.setDate(QtCore.QDate.currentDate())
        self.deadline_input.setStyleSheet("padding: 10px; border: 2px solid #007BFF; border-radius: 5px; font-size: 14px;")
        layout.addWidget(self.deadline_input)

        # Buttons Layout Styling
        button_layout = QtWidgets.QHBoxLayout()

        # Add Task Button Styling
        self.add_button = QtWidgets.QPushButton("Add")
        self.add_button.setStyleSheet("background-color: #007BFF; color: white; padding: 10px; border-radius: 5px; font-size: 14px;")
        self.add_button.clicked.connect(self.add_task)
        button_layout.addWidget(self.add_button)

        # Delete Task Button Styling
        self.delete_button = QtWidgets.QPushButton("Delete")
        self.delete_button.setStyleSheet("background-color: #DC3545; color: white; padding: 10px; border-radius: 5px; font-size: 14px;")
        self.delete_button.clicked.connect(self.delete_task)
        button_layout.addWidget(self.delete_button)

        # Complete Task Button Styling
        self.complete_button = QtWidgets.QPushButton("Complete")
        self.complete_button.setStyleSheet("background-color: #28A745; color: white; padding: 10px; border-radius: 5px; font-size: 14px;")
        self.complete_button.clicked.connect(self.complete_task)
        button_layout.addWidget(self.complete_button)

        layout.addLayout(button_layout)

        # Task List Styling
        self.task_list = QtWidgets.QListWidget()
        self.task_list.setStyleSheet("background-color: #FFFFFF; border: 1px solid #007BFF; font-size: 14px;")
        layout.addWidget(self.task_list)

        self.setLayout(layout)
        self.load_tasks()

    def voice_input(self):
        try:
            with sr.Microphone() as source:
                self.speak("Listening...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
                command = self.recognizer.recognize_google(audio).lower()
                self.task_entry.setText(command)
                self.speak(f"You said: {command}")
        except sr.UnknownValueError:
            self.speak("Sorry, I could not understand the audio.")
        except sr.RequestError:
            self.speak("Could not request results. Please check your internet connection.")

    def voice_date_search(self):
        try:
            with sr.Microphone() as source:
                self.speak("Please say the date you're looking for.")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
                command = self.recognizer.recognize_google(audio).lower()
                self.speak(f"You said: {command}")

                # Match dates in the format '15th February', 'March 20th', etc.
                date_match = re.search(r'(\d{1,2})(st|nd|rd|th)?\s*(january|february|march|april|may|june|july|august|september|october|november|december)', command)

                if date_match:
                    day = int(date_match.group(1))
                    month_name = date_match.group(3).capitalize()
                    month_dict = {
                        "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
                        "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
                    }
                    month = month_dict.get(month_name)
                    if month:
                        current_year = datetime.now().year
                        date = QDate(current_year, month, day)

                        # Set the calendar to the selected date
                        self.calendar.setSelectedDate(date)

                        # Load tasks for the selected date
                        self.load_tasks()

                        self.speak(f"Displaying tasks for {month_name} {day}, {current_year}")
                    else:
                        self.speak("Sorry, I couldn't recognize the month.")
                else:
                    self.speak("Sorry, I couldn't recognize a date in your command.")
        except sr.UnknownValueError:
            self.speak("Sorry, I could not understand the audio.")
        except sr.RequestError:
            self.speak("Could not request results. Please check your internet connection.")

    def add_task(self):
        task = self.task_entry.text()
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        deadline = self.deadline_input.date().toString("yyyy-MM-dd")  # Get deadline input

        if task:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.cursor.execute(
                "INSERT INTO tasks (task, date, time, deadline, completed) VALUES (?, ?, ?, ?, 0)",
                (task, selected_date, timestamp, deadline)
            )
            self.conn.commit()
            self.load_tasks()  # Refresh the task list
            self.speak(f"Task added: {task} with deadline {deadline}")
            self.task_entry.clear()
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "Task cannot be empty!")

    def delete_task(self):
        selected_task = self.task_list.currentItem()
        if selected_task:
            task_text = selected_task.text().split(" - ")[0]
            self.cursor.execute("DELETE FROM tasks WHERE task = ?", (task_text,))
            self.conn.commit()
            self.task_list.takeItem(self.task_list.currentRow())
            self.speak(f"Task deleted: {task_text}")
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select a task to delete!")

    def complete_task(self):
        selected_task = self.task_list.currentItem()
        if selected_task:
            task_text = selected_task.text().split(" - ")[0]
            self.cursor.execute("UPDATE tasks SET completed = 1 WHERE task = ?", (task_text,))
            self.conn.commit()
            selected_task.setText(f"✔ {selected_task.text()}")
            self.speak(f"Task completed: {task_text}")
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select a task to mark as completed!")

    def load_tasks(self):
        self.task_list.clear()
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        self.cursor.execute("SELECT task, date, time, deadline, completed FROM tasks WHERE date = ? ORDER BY deadline ASC", (selected_date,))
        for task, date, time, deadline, completed in self.cursor.fetchall():
            task_text = f"✔ {task} - {date} {time} (Deadline: {deadline})" if completed else f"{task} - {date} {time} (Deadline: {deadline})"
            self.task_list.addItem(task_text)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())
