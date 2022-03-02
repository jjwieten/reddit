import praw
import tkinter as tk
from tkinter import ttk
import threading
import time

reddit = praw.Reddit(
    username="jj_bot_hci",
    password="s3786617",
    client_id="hEahD4o3y7iGerSQsrwveg",
    client_secret="tf_fC8X0bFb-W0TkxUPjPHm6jReQ0A",
    user_agent="hci"
)


class CommentTreeDisplay:
    def showComments(self, url):
        pass


def load_comments():
    top = tk.Tk()
    top.geometry("300x100")
    popup = tk.Entry(top)
    btn = tk.Button(top, text="Submit URL", command=lambda: get_url(popup.get(), top))
    popup.pack()
    btn.pack()
    top.mainloop()


def get_url(url_in, top):
    try:
        url = url_in.split("/")[-3]
        print(url)
        top.destroy()
    except IndexError:
        print("Bad url")


def main():
    root = tk.Tk()
    root.title = 'CommentTreeDisplay'

    # Create menubar
    menubar = tk.Menu()
    # Add file menu
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Exit")
    menubar.add_cascade(label="File", menu=file_menu)
    # Add processing menu
    proc_menu = tk.Menu(menubar, tearoff=0)
    proc_menu.add_command(label="Load comments", command=load_comments)
    menubar.add_cascade(label="Processing", menu=proc_menu)
    root.config(menu=menubar)

    root.mainloop()


if __name__ == "__main__":
    main()

#def process_child_comments(parent, count):
#    for comment in parent:
#        count += 1
#        #print(comment.body)
#        count = process_child_comments(comment.replies, count)
#    return count


#subreddit = reddit.subreddit("thenetherlands")

#for submission in subreddit.hot(limit=1):
#    submission.comments.replace_more(limit=None)
#    print(submission.title)
#    count = 0
#    for top_level_comment in submission.comments.list():
#        count += 1
        # print(top_level_comment.body)
        # count = process_child_comments(top_level_comment.replies, count)
#   print(count)
