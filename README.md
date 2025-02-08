# Voice-Enabled To-Do List Application

A Python-based Voice-Enabled To-Do List application built using **PyQt5**, **SQLite**, **Speech Recognition**, and **Text-to-Speech** (pyttsx3). This app allows users to manage tasks using voice commands and a graphical interface, supporting features such as adding, deleting, completing tasks, and navigating tasks by date.

## Features

- **Voice Input**: Users can add tasks, search for tasks, and navigate to specific dates using voice commands.
- **Task Management**: Add, delete, and mark tasks as completed.
- **Calendar View**: Users can view and select tasks based on the calendar date.
- **Deadline Management**: Set deadlines for each task and see them in the task list.
- **Text-to-Speech Feedback**: The application provides voice feedback for each action.

## Technologies Used

- **Frontend**:
  - **PyQt5**: For building the graphical user interface (GUI).
  - **CSS**: For customizing the UI to make it colorful and visually appealing.
  
- **Backend**:
  - **Python**: Core programming language used for logic, task management, and integrating libraries.
  - **SQLite**: A lightweight database to store tasks.
  - **Speech Recognition**: Converts voice commands into text.
  - **pyttsx3**: Text-to-speech engine for providing feedback via voice.

## Installation

### Prerequisites
Make sure you have Python installed. You will also need the following Python packages:
- PyQt5
- pyttsx3
- SpeechRecognition
- sqlite3 (comes with Python)
- PyAudio (required for speech recognition)

To install the required dependencies, run the following command:

```bash
pip install PyQt5 pyttsx3 SpeechRecognition pyaudio
