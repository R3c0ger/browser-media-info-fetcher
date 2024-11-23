#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

import pyperclip
import win32gui

from main import (
    get_visible_browser_window,
    extract_video_title,
    get_active_tab_url,
    extract_video_url,
)
from version import __VERSION__


def fetch_and_copy(title_entry, url_entry):
    hwnd = get_visible_browser_window()
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


def copy_to_clipboard(entry):
    text = entry.get()
    if not text.startswith("No ") and text:
        pyperclip.copy(text)


def add_to_areas(title_entry, url_entry, title_area, url_area):
    title = title_entry.get()
    url = url_entry.get()
    if url:
        current_titles = title_area.get("1.0", tk.END)
        current_urls = url_area.get("1.0", tk.END)

        new_titles = f"{title}\n{current_titles}" if current_titles else title
        new_urls = f"{url}\n{current_urls}" if current_urls else url

        title_area.delete("1.0", tk.END)
        title_area.insert(tk.END, new_titles)

        url_area.delete("1.0", tk.END)
        url_area.insert(tk.END, new_urls)


def copy_area_text(area):
    text = area.get("1.0", tk.END).strip()
    if text:
        pyperclip.copy(text)


def main_window():
    root = tk.Tk()
    # 禁止调整大小
    root.resizable(False, False)
    root.title(f"Browser Video Info Fetcher - {__VERSION__}")

    # 框架容器
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0)

    run_frame = ttk.Frame(main_frame)
    run_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True)

    # “运行”按钮
    run_button = ttk.Button(
        run_frame, text="运行抓取\n(Ctrl+R)", width=15,
        command=lambda: fetch_and_copy(title_entry, url_entry)
    )
    run_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.Y, expand=True)
    root.bind("<Control-r>", lambda event: run_button.invoke())

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
    url_frame.pack(side=tk.TOP, padx=5, pady=5)
    url_label = ttk.Label(url_frame, text="URL:")
    url_label.pack(side=tk.LEFT, padx=5, pady=5)
    url_entry = ttk.Entry(url_frame, width=50)
    url_entry.pack(side=tk.LEFT, padx=5, pady=5)
    url_copy_button = ttk.Button(url_frame, text="复制", command=lambda: copy_to_clipboard(url_entry))
    url_copy_button.pack(side=tk.LEFT, padx=5, pady=5)

    # 按钮区域
    add_clr_frame = ttk.Frame(main_frame)
    add_clr_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
    # 添加到列表按钮
    add_btn = ttk.Button(
        add_clr_frame,
        text="添加到列表 (Ctrl+A)",
        width=32,
        command=lambda: add_to_areas(title_entry, url_entry, title_area, url_area)
    )
    add_btn.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
    root.bind("<Control-a>", lambda event: add_btn.invoke())
    # 清空列表按钮
    clear_btn = ttk.Button(
        add_clr_frame,
        text="清空列表 (Ctrl+Q)",
        width=32,
        command=lambda: [title_area.delete("1.0", tk.END), url_area.delete("1.0", tk.END)]
    )
    clear_btn.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.X, expand=True)
    root.bind("<Control-q>", lambda event: clear_btn.invoke())

    # 列表区域
    areas_frame = ttk.Frame(main_frame, padding="5")
    areas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    # 标题列表
    title_area = tk.Text(areas_frame, height=8, width=32, font=("宋体", 9))
    title_area.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
    # URL 列表
    url_area = tk.Text(areas_frame, height=8, width=32, font=("宋体", 9))
    url_area.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

    # 用于复制的按钮
    cpybtn_frame = ttk.Frame(main_frame)
    cpybtn_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
    # 复制所有标题
    copy_titles_btn = ttk.Button(cpybtn_frame, text="复制所有标题", command=lambda: copy_area_text(title_area))
    copy_titles_btn.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
    # 复制所有 URL
    copy_urls_btn = ttk.Button(cpybtn_frame, text="复制所有URL", command=lambda: copy_area_text(url_area))
    copy_urls_btn.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

    root.mainloop()


if __name__ == "__main__":
    main_window()
