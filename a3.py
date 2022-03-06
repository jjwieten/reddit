import praw
import tkinter as tk
from tkinter import ttk
import threading
import time
from a2 import CommentTreeDisplay


reddit = praw.Reddit(
    username="hci_bot_a1",
    password="s3786617",
    client_id="4-WmhNJXd3n-ZhCsOa3XAQ",
    client_secret="tOBLYrbRKLcz6yDyR8ypNBPcUfL_sw",
    user_agent="hci"
)


class ResponseCommentTreeDisplay(CommentTreeDisplay):
    def __init__(self, root):
        # tk.Frame.__init__(self, CommentTreeDisplay)
        super().__init__(root)
        self.tree.bind("<Double-1>", self.double_click_comment)

    def double_click_comment(self, event):
        item_id = event.widget.focus()
        print(item_id)


def main():
    root = tk.Tk()
    root.geometry("300x200")
    root.title('ResponseCommentTreeDisplay')
    win = ResponseCommentTreeDisplay(root)
    win.pack()
    root.mainloop()


if __name__ == "__main__":
    main()

