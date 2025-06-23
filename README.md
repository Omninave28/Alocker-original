# 🔒 Alocker-original

**Alocker** is a Python-based application locker for Windows that displays a fullscreen password prompt to restrict access to specific applications.

It is designed for:
- 🧑‍👩‍👦 Parental control
- 🧘 Productivity enforcement
- 🎯 Personal focus

By locking access to distractions like games or streaming apps.
## 🧠 Features

- 🔐 Fullscreen Lock Prompt when a locked app is launched  
- 👁️‍🗨️ Invisible in Taskbar to prevent bypassing  
- ⌨️ Blocks System Keys like `ESC`, `Alt+Tab`, `Win`, and `Ctrl+F4`  
- 🔄 Configurable Locked Apps & Passwords via JSON file  
- 🧠 Lightweight & Efficient, suitable for always-on use  
## 📁 Project Structure

```bash
Alocker-original/
├── app_locker.py             # Main script that runs the App Locker
├── app_config_template.json  # Example config file structure (no real passwords)
├── .gitignore                # Prevents sensitive files from being pushed
└── README.md                 # Project documentation
```
## ⚙️ How It Works

1. You list the apps you want to lock in `app_config.json`.  
2. When any locked app is opened, a fullscreen password window appears.  
3. User must enter the correct password to access the app.  
4. System keys are blocked to avoid escape tricks.  

---


## 🧪 Sample Config (`app_config_template.json`)

```json
{
  "locked_apps": ["Netflix", "chrome.exe", "game.exe"],
  "password": "your-password-here"
}
```
## 🔧 Requirements and Installation

- Python **3.8+**
- Packages:
  - `keyboard`
  - `tkinter` *(comes with Python standard library)*
  - `Pillow` (PIL)

### 📦 Install Dependencies

```bash
pip install keyboard pillow
```

### ▶️ Run the Locker
```bash
python app_locker.py
```

## ❗ Warnings

- ❌ Do not forget your password — the app locks you out!

- 🔒 Make sure your config is secure.

- 🛡️ Use this only on your own system or with permission.

## 📜 License

This project is licensed under the [MIT License](LICENSE).
## 🙋 Author

**👤 Om Ninave**  
🔗 [GitHub Profile](https://github.com/Omninave28)
