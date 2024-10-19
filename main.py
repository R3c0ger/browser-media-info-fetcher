from functools import partial
from time import sleep

import pyautogui
import pyperclip
import win32gui
from pywinauto.application import Application


BrowserSwitcher = {
    "firefox": "Firefox",
    "edge": "Edge",
    "chrome": "Chrome",
}
SiteSwitcher = [
    # 网站名、网页标题后缀、网址分割处
    ("抖音", " - 抖音", "?"),
    ("快手", "-快手", "?"),
    ("哔哩哔哩", "_哔哩哔哩", "/?"),
    ("YouTube", " - YouTube", "&")
]


def enum_windows_callback(hwnd, results, browser_name="firefox"):
    """
    Callback function for enumerating windows.

    This function is called for each top-level window by `win32gui.EnumWindows`.
    It checks if the window title contains the specified browser name and, if so,
    appends the window handle to the results list.

    Args:
        hwnd (int): Handle to a top-level window.
        results (list): List to store window handles that match the browser name.
        browser_name (str, optional): The name of the browser to look for in window titles. Defaults to "firefox".
    """
    if BrowserSwitcher[browser_name] in win32gui.GetWindowText(hwnd):
        # # 获取窗口类名
        # class_name = win32gui.GetClassName(hwnd)
        # print(class_name)
        results.append(hwnd)


def get_visible_browser_window(browser_name="firefox"):
    """
    Enumerate all windows and return the first visible browser window.

    This function enumerates all top-level windows and returns the handle of the first
    visible window that matches the specified browser name.

    Args:
        browser_name (str, optional): The name of the browser to look for in window titles. Defaults to "firefox".

    Returns:
        int or None: The handle of the first visible browser window that matches the browser name,
                     or None if no such window is found.
    """
    # 枚举所有窗口，返回第一个可见的火狐浏览器窗口
    results = []
    callback = partial(enum_windows_callback, browser_name=browser_name)
    win32gui.EnumWindows(callback, results)
    # print(results)
    return results[0] if results else None


def extract_video_title(title):
    """
    Extract the video title and its corresponding site index from the window title.

    This function iterates through the `SiteSwitcher` list to find a match for the given title.
    If a match is found, it extracts the pure title and the index of the site in the `SiteSwitcher` list.

    Args:
        title (str): The window title to extract the video title from.

    Returns:
        tuple: A tuple containing the pure title (str) and the site index (int).
               If no match is found, returns (None, -1).
    """
    for site_tuple in SiteSwitcher:
        if site_tuple[1] in title:
            pure_title = title.split(site_tuple[1])[0]
            site_index_in_switcher = SiteSwitcher.index(site_tuple)
            print(f"处理后的标题：{pure_title}")
            print(f"网站：{site_tuple[0]}")
            return pure_title, site_index_in_switcher
    return None, -1


def get_active_tab_url(hwnd, title):
    """
    Get the URL of the active tab in the specified browser window.

    This function connects to the browser window using its handle and title,
    selects the address bar, copies the URL, and returns it.

    Args:
        hwnd (int): Handle to the browser window.
        title (str): Title of the browser window.

    Returns:
        str: The URL of the active tab.
    """
    app = Application(backend="uia").connect(handle=hwnd)
    dlg = app[title]
    # print(dlg.exists(timeout=None, retry_interval=None))
    # dlg.print_control_identifiers()
    # 选中地址栏并复制
    dlg.type_keys("^l")
    sleep(0.2)
    dlg.type_keys("^c")
    sleep(0.2)
    raw_url = pyperclip.paste()
    print(f"原始URL：{raw_url}")
    # 切换应用
    pyautogui.hotkey('alt', 'tab')
    return raw_url


def extract_video_url(raw_url, site_index_in_switcher):
    """
    Extract the video URL based on the site index.

    This function checks if the site index is valid and extracts the video URL
    from the raw URL based on the site-specific delimiter.

    Args:
        raw_url (str): The raw URL to extract the video URL from.
        site_index_in_switcher (int): The index of the site in the SiteSwitcher list.

    Returns:
        str: The extracted video URL if the site index is valid and the delimiter is found in the raw URL.
             Otherwise, returns the raw URL.
    """
    if site_index_in_switcher == -1:
        sites_str = "、".join([site_tuple[0] for site_tuple in SiteSwitcher])
        print(f"该网站不属于：{sites_str}")
        return raw_url
    site_tuple = SiteSwitcher[site_index_in_switcher]
    if site_tuple[2] in raw_url:
        url = raw_url.split(site_tuple[2])[0]
        print(f"提取到的URL：{url}")
        return url
    else:
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
