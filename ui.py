5import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import webbrowser
import os
import csv
import smtplib
from email.message import EmailMessage
import datetime

# ========== GMAIL CONFIG ==========
SENDER_EMAIL = "your_email@gmail.com"       # Replace with your Gmail
APP_PASSWORD = "your_app_password_here"     # App-specific password

# ========== GREETING ==========
def get_greeting():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 17:
        return "Good Afternoon"
    elif 17 <= hour < 21:
        return "Good Evening"
    else:
        return "Good Night"

# ========== ACTIVITY LOGGER ==========
def log_activity(command):
    with open("user_activity.csv", "a", newline="") as f:
         writer = csv.writer(f)
        writer.writerow([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), command])

# ========== EMAIL SENDER ==========
def send_email(to_email, subject, content):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg.set_content(content)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)

        return True
    except Exception as e:
        print("Email Error:", e)
        return False

# ========== SPEECH RECOGNITION ==========
def recognize_speech():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            messagebox.showinfo("Listening", "Speak now...")
            print("Listening...")
            audio = r.listen(source, timeout=10, phrase_time_limit=10)  # Increased timeout

        command = r.recognize_google(audio).lower()
        messagebox.showinfo("You said", command)
        log_activity(command)

        if "facebook" in command:
            webbrowser.open("https://www.facebook.com")
        elif "whatsapp" in command:
            webbrowser.open("https://web.whatsapp.com")
        elif "youtube" in command:
            webbrowser.open("https://www.youtube.com")
        elif "notepad" in command:
            os.system("notepad.exe")
        elif "calculator" in command:
            os.system("calc.exe")
        elif "camera" in command:
            os.system("start microsoft.windows.camera:")
        elif "photo" in command or "photos" in command:
            os.system("start ms-photos:")
        elif "shutdown" in command:
            os.system("shutdown /s /t 5")
        else:
            messagebox.showwarning("Unknown Command", f"Unrecognized: {command}")

    except sr.WaitTimeoutError:
        messagebox.showerror("Timeout", "No speech detected. Try again.")
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Could not understand your speech.")
    except sr.RequestError:
        messagebox.showerror("Error", "Network or Google API error.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ========== USER MANAGEMENT ==========
csv_file = "users.csv"

def signup():
    uname = username_entry.get()
    email = email_entry.get()
    contact = contact_entry.get()
    pwd = password_entry.get()

    if uname and email and contact and pwd:
        with open(csv_file, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([uname, email, contact, pwd])
        messagebox.showinfo("Success", "Sign Up Successful!")
    else:
        messagebox.showerror("Error", "All fields are required!")

def login():
    uname = username_entry.get()
    pwd = password_entry.get()

    if not uname or not pwd:
        messagebox.showerror("Error", "Username and Password required!")
        return

    found = False
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == uname:
                if row[3] == pwd:
                    found = True
                    email = row[1]
                    greeting = get_greeting()
                    send_email(
                        email,
                        "Login Successful",
                        f"{greeting} {uname},\n\nYou have successfully logged in.\nUsername: {uname}\nPassword: {pwd}"
                    )
                    open_dashboard(uname)
                else:
                    messagebox.showerror("Error", "Invalid Password!")
                break
    if not found:
        messagebox.showerror("Error", "Username not found!")

def reset():
    username_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# ========== DASHBOARD ==========
def open_dashboard(username):
    login_window.destroy()
    dash = tk.Tk()
    dash.title("Dashboard")
    dash.geometry("500x400")
    dash.config(bg="#f0f8ff")

    tk.Label(dash, text=f"{get_greeting()}, {username}!", font=("Arial", 16), fg="green", bg="#f0f8ff").pack(pady=20)
    tk.Button(dash, text="🎤 Start Voice Command", font=("Arial", 12, "bold"),
              command=recognize_speech, bg="blue", fg="white").pack(pady=30)
    tk.Label(dash, text="Try saying: Facebook, WhatsApp, Notepad, YouTube, Shutdown...", font=("Arial", 10), bg="#f0f8ff").pack()
    dash.mainloop()

# ========== MAIN UI ==========
login_window = tk.Tk()
login_window.title("Voice App Launcher")
login_window.geometry("500x600")
login_window.config(bg="#e8f0fe")

tk.Label(login_window, text="Voice App Launcher", font=("Arial", 16, "bold"), bg="#e8f0fe").pack(pady=10)
tk.Label(login_window, text=get_greeting(), font=("Arial", 12), fg="green", bg="#e8f0fe").pack()

frame = tk.Frame(login_window, bg="white", bd=2, relief=tk.SOLID)
frame.place(x=70, y=80, width=360, height=300)

tk.Label(frame, text="Username", font=("Arial", 11), bg="white").place(x=20, y=20)
username_entry = tk.Entry(frame, font=("Arial", 11))
username_entry.place(x=130, y=20)

tk.Label(frame, text="Email", font=("Arial", 11), bg="white").place(x=20, y=60)
email_entry = tk.Entry(frame, font=("Arial", 11))
email_entry.place(x=130, y=60)

tk.Label(frame, text="Contact No", font=("Arial", 11), bg="white").place(x=20, y=100)
contact_entry = tk.Entry(frame, font=("Arial", 11))
contact_entry.place(x=130, y=100)

tk.Label(frame, text="Password", font=("Arial", 11), bg="white").place(x=20, y=140)
password_entry = tk.Entry(frame, font=("Arial", 11), show="*")
password_entry.place(x=130, y=140)

tk.Button(frame, text="Sign Up", command=signup, bg="green", fg="white", width=10).place(x=30, y=200)
tk.Button(frame, text="Login", command=login, bg="blue", fg="white", width=10).place(x=140, y=200)
tk.Button(frame, text="Reset", command=reset, bg="orange", fg="white", width=10).place(x=250, y=200)

login_window.mainloop()
