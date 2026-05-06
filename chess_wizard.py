"""
chess_wizard.py – Tkinter-based start-up wizard.
Returns a dict with keys: comm_type ("alone"|"server"|"client"), my_color ("White"|"Black")
Returns None if the user cancelled/closed the dialog.
"""
import tkinter as tk
from tkinter import ttk
import os
import sys

ICON_PATH = os.path.join(os.path.dirname(__file__), "img", "chess_icon.ico")


def _center(win):
    win.update_idletasks()
    w, h = win.winfo_width(), win.winfo_height()
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    win.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")


def run_wizard():
    result = {}

    root = tk.Tk()
    root.title("Chess – 시작")
    root.resizable(False, False)

    if os.path.isfile(ICON_PATH):
        try:
            root.iconbitmap(ICON_PATH)
        except Exception:
            pass

    # ── Style ─────────────────────────────────────────────────────────────
    style = ttk.Style(root)
    style.theme_use("clam")
    BG = "#1e1e2e"
    FG = "#cdd6f4"
    ACC = "#89b4fa"
    BTN = "#313244"
    BTN_ACTIVE = "#45475a"

    root.configure(bg=BG)
    style.configure("TFrame",       background=BG)
    style.configure("TLabel",       background=BG, foreground=FG,
                    font=("Segoe UI", 11))
    style.configure("Title.TLabel", background=BG, foreground=ACC,
                    font=("Segoe UI", 18, "bold"))
    style.configure("Sub.TLabel",   background=BG, foreground=FG,
                    font=("Segoe UI", 10))
    style.configure("TRadiobutton", background=BG, foreground=FG,
                    font=("Segoe UI", 11), indicatorcolor=ACC)
    style.map("TRadiobutton",
              background=[("active", BG)],
              foreground=[("active", ACC)])
    style.configure("TButton",      background=BTN, foreground=FG,
                    font=("Segoe UI", 11), padding=(12, 6), relief="flat")
    style.map("TButton",
              background=[("active", BTN_ACTIVE)],
              foreground=[("active", ACC)])

    # ── Main frame ────────────────────────────────────────────────────────
    main = ttk.Frame(root, padding=28)
    main.pack()

    # Title
    ttk.Label(main, text="♟  Chess", style="Title.TLabel").pack()
    ttk.Label(main, text="게임 설정을 선택해주세요",
              style="Sub.TLabel").pack(pady=(2, 18))

    ttk.Separator(main, orient="horizontal").pack(fill="x", pady=(0, 18))

    # ── Mode section ──────────────────────────────────────────────────────
    ttk.Label(main, text="게임 모드", font=("Segoe UI", 11, "bold"),
              background=BG, foreground=ACC).pack(anchor="w")

    mode_var = tk.StringVar(value="alone")

    modes = [
        ("alone",  "1인용  (AI 대전)"),
        ("server", "2인용  (서버 – White)"),
        ("client", "2인용  (클라이언트 – Black)"),
    ]
    for val, label in modes:
        ttk.Radiobutton(main, text=label, variable=mode_var,
                        value=val).pack(anchor="w", pady=2)

    ttk.Separator(main, orient="horizontal").pack(fill="x", pady=18)

    # ── Color section (only relevant for alone / server) ──────────────────
    color_lbl = ttk.Label(main, text="내 색상 (1인용 / 서버 모드)",
                          font=("Segoe UI", 11, "bold"),
                          background=BG, foreground=ACC)
    color_lbl.pack(anchor="w")

    color_var = tk.StringVar(value="White")
    colors = [("White", "White  ♔"), ("Black", "Black  ♚")]
    for val, label in colors:
        ttk.Radiobutton(main, text=label, variable=color_var,
                        value=val).pack(anchor="w", pady=2)

    ttk.Separator(main, orient="horizontal").pack(fill="x", pady=18)

    # ── Buttons ───────────────────────────────────────────────────────────
    btn_frame = ttk.Frame(main)
    btn_frame.pack(fill="x")

    def on_start():
        result["comm_type"] = mode_var.get()
        result["my_color"]  = color_var.get() if mode_var.get() != "client" else "Black"
        root.destroy()

    def on_cancel():
        root.destroy()

    ttk.Button(btn_frame, text="취소", command=on_cancel).pack(
        side="right", padx=(6, 0))
    ttk.Button(btn_frame, text="게임 시작  ▶", command=on_start).pack(
        side="right")

    _center(root)
    root.mainloop()

    return result if result else None
