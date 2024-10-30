from functools import partial
from time import sleep

import pyautogui
import pyperclip
import win32gui
from pywinauto.application import Application

__VERSION__ = "0.1.2"

BrowserSwitcher = {
    "firefox": "Firefox",
    "edge": "Edge",
    "chrome": "Chrome",
}
SiteSwitcher = [
    # 网站名、网页标题后缀、网址分割处
    ("抖音", " - 抖音", ["?",]),
    ("快手", "-快手", ["?",]),
    ("哔哩哔哩", "_哔哩哔哩", ["/?", "?", ]),
    ("YouTube", " - YouTube", ["&ab_channel=",])
]


def enum_windows_callback(hwnd, results, browser_name="firefox"):
    if BrowserSwitcher[browser_name] in win32gui.GetWindowText(hwnd):
        # # 获取窗口类名
        # class_name = win32gui.GetClassName(hwnd)
        # print(class_name)
        results.append(hwnd)


def get_visible_browser_window(browser_name="firefox"):
    # 枚举所有窗口，返回第一个可见的火狐浏览器窗口
    results = []
    callback = partial(enum_windows_callback, browser_name=browser_name)
    win32gui.EnumWindows(callback, results)
    # print(results)
    return results[0] if results else None


def extract_video_title(title):
    for site_tuple in SiteSwitcher:
        if site_tuple[1] in title:
            pure_title = title.split(site_tuple[1])[0]
            site_index_in_switcher = SiteSwitcher.index(site_tuple)
            print(f"处理后的标题：{pure_title}")
            print(f"网站：{site_tuple[0]}")
            return pure_title, site_index_in_switcher
    return None, -1


def get_active_tab_url(hwnd, title):
    app = Application(backend="uia").connect(handle=hwnd)
    dlg = app[title]
    # print(dlg.exists(timeout=None, retry_interval=None))
    # dlg.print_control_identifiers()
    # 选中地址栏并复制
    dlg.type_keys("^l")
    sleep(0.1)
    dlg.type_keys("^c")
    sleep(0.1)
    raw_url = pyperclip.paste()
    print(f"原始URL：{raw_url}")
    # 切换应用
    pyautogui.hotkey('alt', 'tab')
    return raw_url


def extract_video_url(raw_url, site_index_in_switcher):
    if site_index_in_switcher == -1:
        sites_str = "、".join([site_tuple[0] for site_tuple in SiteSwitcher])
        print(f"该网站不属于：{sites_str}")
        return raw_url
    site_tuple = SiteSwitcher[site_index_in_switcher]
    for param in site_tuple[2]:
        if param in raw_url:
            extracted_url = raw_url.split(param)[0]
            print(f"提取到的URL：{extracted_url}")
            return extracted_url
    print(f"提取到的URL（无需处理）：{raw_url}")
    return raw_url


def main():
    browser_name = "firefox"
    hwnd = get_visible_browser_window(browser_name)
    if hwnd:
        # 获取窗口标题
        window_title = win32gui.GetWindowText(hwnd)
        print(f"窗口标题：{window_title}")

        # 提取短视频标题实际内容、所属网站
        video_title, site_index = extract_video_title(window_title)
        if not video_title:
            print("Could not extract video title from current window title.")
            return

        raw_url = get_active_tab_url(hwnd, window_title)
        pure_url = extract_video_url(raw_url, site_index)
        # 复制到剪贴板
        pyperclip.copy(video_title)
        sleep(0.5)
        pyperclip.copy(pure_url)
    else:
        print("No visible Firefox window found.")


if __name__ == "__main__":
    main()
