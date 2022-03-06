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
        # Counting intreger to append to comment
        self.comment_int = 0
        self.tree.bind("<Double-1>", self.double_click_comment)

    def double_click_comment(self, event):
        item_id = event.widget.focus()
        comment_text = self.ask_comment()
        self.add_comment_to_tree(self, item_id, comment_text)
        print(item_id)

    def add_comment_to_tree(self, parent_id, comment_text):
        comment_id = "{0}_{1}".format(parent_id, self.comment_int)
        self.comment_int += 1
        self.tree.insert('', tk.END, text=comment_text, iid=comment_id, open=False)
        self.tree.move(comment_id, parent_id, 0)

    def ask_comment(self):
        """
        Make window to enter url and recieve input comment
        """
        top = tk.Tk()
        top.geometry("300x100")
        popup = tk.Entry(top)
        url_btn = tk.Button(top, text="Submit comment", command=lambda: testprint(popup.get()))
        popup.pack()
        url_btn.pack()
        top.mainloop()


def testprint(input):
    print(input)


def main():
    root = tk.Tk()
    root.geometry("300x200")
    root.title('ResponseCommentTreeDisplay')
    win = ResponseCommentTreeDisplay(root)
    win.pack()
    root.mainloop()


if __name__ == "__main__":
    main()

