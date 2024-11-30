# Browser Media Information Fetcher

本脚本可以在浏览器中打开快手、哔哩哔哩、抖音、YouTube 等视频页面时，获取视频的标题和关键 URL。
This is a simple Python script that fetches the title and key URL of a video in KuaiShou, Bilibili, Douyin, and YouTube, which is provided by a page(tab) in a browser like Firefox or Edge.

原理是使用 win32gui 返回最上层的浏览器窗口标题，然后使用 pywinauto 选中地址栏并复制 URL，对 URL 进行清理。
The script uses win32gui to get the title of the topmost window, and then uses pywinauto to select the address bar and copy the URL. The URL is then cleaned up.

本脚本仅用于个人的特定需求，不保证能在所有情况下正常工作，目前也没有更新与维护的计划。
This script is only for my personal needs and may not work in all cases. I have no plan to update or maintain it.

已知 bug：
- 若在视频播放时进行抓取，最后脚本在按下 <kbd>Alt</kbd>+<kbd>Tab</kbd> 切换窗口至本工具界面时，可能会无法松开 <kbd>Alt</kbd> 键。
  解决办法：打开大写锁定再关闭。

Bug known:
- If you capture the video while playing, the script may fail to release the <kbd>Alt</kbd> key when it presses <kbd>Alt</kbd>+<kbd>Tab</kbd> to switch to the tool interface.
  Solution: Turn on Caps Lock and then turn it off.

