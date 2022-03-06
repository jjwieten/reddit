import praw
import tkinter as tk
from tkinter import ttk
import threading
import time
from a2 import CommentTreeDisplay
from a3 import ResponseCommentTreeDisplay


reddit = praw.Reddit(
    username="hci_bot_a1",
    password="s3786617",
    client_id="4-WmhNJXd3n-ZhCsOa3XAQ",
    client_secret="tOBLYrbRKLcz6yDyR8ypNBPcUfL_sw",
    user_agent="hci"
)



def testprint(input):
    print(input)

def main():
    root = tk.Tk()
    root.geometry("300x200")
    root.title('Update Tree Display')
    win = ResponseCommentTreeDisplay(root)
    win.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
