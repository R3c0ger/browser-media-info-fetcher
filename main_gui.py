#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

import pyperclip
import win32gui

from main import (
    BrowserSwitcher,
    get_visible_browser_window,
    extract_video_title,
    get_active_tab_url,
    extract_video_url,
)


def fetch_and_copy(browser_name, title_entry, url_entry, title_copy_button):
    hwnd = get_visible_browser_window(browser_name)
    if hwnd:
        window_title = win32gui.GetWindowText(hwnd)
        video_title, site_index = extract_video_title(window_title)
        if video_title:
            raw_url = get_active_tab_url(hwnd, window_title)
            pure_url = extract_video_url(raw_url, site_index)
            title_entry.delete(0, tk.END)
            title_entry.insert(tk.END, video_title)
            url_entry.delete(0, tk.END)
            url_entry.insert(tk.END, pure_url)
            return video_title, pure_url
    title_entry.delete(0, tk.END)
    title_entry.insert(tk.END, "No title")
    url_entry.delete(0, tk.END)
    url_entry.insert(tk.END, "No URL")
    print("No visible browser window found.")
    # 将焦点移动到title_copy_button
    title_copy_button.focus()


def copy_to_clipboard(entry):
    text = entry.get()
    pyperclip.copy(text)


def main_window():
    root = tk.Tk()
    # 禁止调整大小
    root.resizable(False, False)
    root.title("Browser Video Info Fetcher")

    # 框架容器
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0)

    run_frame = ttk.Frame(main_frame)
    run_frame.pack(side=tk.LEFT, padx=5)

    # 下拉选择框
    browser_var = tk.StringVar()
    browser_var.set("firefox")  # 默认选项
    browser_menu = ttk.Combobox(
        run_frame, textvariable=browser_var, values=list(BrowserSwitcher.keys()), width=10
    )
    browser_menu.pack(side=tk.BOTTOM, padx=5, pady=5)

    # “运行”按钮
    run_button = ttk.Button(
        run_frame, text="运行", width=12,
        command=lambda: fetch_and_copy(browser_var.get(), title_entry, url_entry, title_copy_button)
    )
    run_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.Y)

    # 输出标题栏
    title_frame = ttk.Frame(main_frame)
    title_frame.pack(side=tk.TOP, padx=5, pady=5)
    title_label = ttk.Label(title_frame, text="标题:")
    title_label.pack(side=tk.LEFT, padx=5, pady=5)
    title_entry = ttk.Entry(title_frame, width=50)
    title_entry.pack(side=tk.LEFT, padx=5, pady=5)
    title_copy_button = ttk.Button(title_frame, text="复制", command=lambda: copy_to_clipboard(title_entry))
    title_copy_button.pack(side=tk.LEFT, padx=5, pady=5)

    # 输出URL栏
    url_frame = ttk.Frame(main_frame)
    url_frame.pack(side=tk.BOTTOM, padx=5, pady=5)
    url_label = ttk.Label(url_frame, text="URL:")
    url_label.pack(side=tk.LEFT, padx=5, pady=5)
    url_entry = ttk.Entry(url_frame, width=50)
    url_entry.pack(side=tk.LEFT, padx=5, pady=5)
    url_copy_button = ttk.Button(url_frame, text="复制", command=lambda: copy_to_clipboard(url_entry))
    url_copy_button.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main_window()
