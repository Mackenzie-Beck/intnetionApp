"""
Intention: a startup prompt that asks why you're using your computer.

- Can't be dismissed until you write a short sentence.
- Logs every intention to ~/intentions.log with a timestamp.
- No blocking of apps or sites; it's just a conscious pause.

Requires Python 3 with tkinter (included on Windows/macOS python.org installs).
"""
import datetime
import pathlib
import tkinter as tk

MIN_WORDS = 3          # minimum words required
FULLSCREEN = False     # set True for a full-screen prompt
LOG = pathlib.Path.home() / "intentions.log"


def last_intention():
    try:
        lines = LOG.read_text(encoding="utf-8").strip().splitlines()
        return lines[-1] if lines else ""
    except OSError:
        return ""


def main():
    root = tk.Tk()
    root.title("Intention")
    root.configure(bg="#111418")
    root.attributes("-topmost", True)
    root.protocol("WM_DELETE_WINDOW", lambda: None)  # ignore the close button

    if FULLSCREEN:
        root.attributes("-fullscreen", True)
    else:
        w, h = 640, 320
        x = (root.winfo_screenwidth() - w) // 2
        y = (root.winfo_screenheight() - h) // 3
        root.geometry(f"{w}x{h}+{x}+{y}")

    frame = tk.Frame(root, bg="#111418")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="What do you intend to do this session?",
             font=("Helvetica", 22, "bold"), fg="#f2f2f2", bg="#111418").pack(pady=(0, 6))
    tk.Label(frame, text=datetime.datetime.now().strftime("%A, %d %B · %H:%M"),
             font=("Helvetica", 11), fg="#7d8590", bg="#111418").pack(pady=(0, 18))

    entry = tk.Entry(frame, font=("Helvetica", 16), width=44, bg="#1c2128",
                     fg="#f2f2f2", insertbackground="#f2f2f2", relief="flat")
    entry.pack(ipady=10)
    entry.focus_force()

    hint = tk.Label(frame, text=f"At least {MIN_WORDS} words. Press Enter to begin.",
                    font=("Helvetica", 10), fg="#7d8590", bg="#111418")
    hint.pack(pady=(10, 0))

    prev = last_intention()
    if prev:
        tk.Label(frame, text=f"Last time: {prev.split(' | ', 1)[-1]}",
                 font=("Helvetica", 10, "italic"), fg="#586069", bg="#111418",
                 wraplength=560).pack(pady=(18, 0))

    def submit(_event=None):
        text = entry.get().strip()
        if len(text.split()) < MIN_WORDS:
            hint.config(text=f"Be a little more specific ({MIN_WORDS}+ words).", fg="#e5534b")
            return
        stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        with LOG.open("a", encoding="utf-8") as f:
            f.write(f"{stamp} | {text}\n")
        root.destroy()

    entry.bind("<Return>", submit)
    root.mainloop()


if __name__ == "__main__":
    main()
