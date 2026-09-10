import sys
import tkinter as tk
from tkinter import messagebox


def main():
    path_file = sys.argv[1]
    depth = sys.argv[2]
    message_file = sys.argv[3]
    revision = sys.argv[4]
    error_file = sys.argv[5]
    cwd = sys.argv[6]

    production_branch = "production250320"

    # 只在 production 分支提醒
    if production_branch.lower() not in cwd.lower():
        return

    clipboardMsg = f"production250320 有新的提交，SVN r{revision}，记得合并一下。"

    root = tk.Tk()
    root.withdraw()

    # 写入剪贴板
    root.clipboard_clear()
    root.clipboard_append(clipboardMsg)
    root.update()

    messagebox.showinfo(
        "SVN Production 提醒",
        f"分支 production250320 提交成功！\n\n"
        f"Revision：r{revision}\n\n"
        f"通知话术已复制到剪贴板，记得提醒后端合并到 Coding。",
    )

    root.destroy()


if __name__ == "__main__":
    main()
