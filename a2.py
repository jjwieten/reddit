import praw
import tkinter as tk
from tkinter import ttk
import threading
import time

reddit = praw.Reddit(
    username="hci_bot_a1",
    password="s3786617",
    client_id="4-WmhNJXd3n-ZhCsOa3XAQ",
    client_secret="tOBLYrbRKLcz6yDyR8ypNBPcUfL_sw",
    user_agent="hci"
)


class CommentTreeDisplay(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.topframe = tk.Frame(self)
        self.exit = False

        # Create menubar
        self.menubar = tk.Menu()
        # Add file menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Exit", command=self.stopRunning)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        # Add processing menu
        self.proc_menu = tk.Menu(self.menubar, tearoff=0)
        self.proc_menu.add_command(label="Load comments", command=self.load_comments)
        self.menubar.add_cascade(label="Processing", menu=self.proc_menu)
        root.config(menu=self.menubar)

        self.tree = ttk.Treeview(self)

    def load_comments(self):
        top = tk.Tk()
        top.geometry("300x100")
        popup = tk.Entry(top)
        url_btn = tk.Button(top, text="Submit URL", command=lambda: self.get_url(popup.get(), top))
        popup.pack()
        url_btn.pack()
        top.mainloop()

    def get_url(self, url_in, top):
        try:
            #find appropriate id
            if url_in[-1] == "/":
                id = url_in.split("/")[-3]
            else:
                id = url_in.split("/")[-2]
            top.destroy()
            self.showComments(id)
        except IndexError:
            e = tk.Label(top, text="Please enter a valid URL\n")
            e.pack()

    def showComments(self, id):
        #subm_ID = reddit.submission(url)
        #print(subm_ID)
        #subm = reddit.__init__(self, subm_ID)

        submission = reddit.submission(id=id)
        for comment in submission.comments.list():
            print(comment.body)

        #count = 0
        #for top_level_comment in subm.comments.list():
        #    count += 1
        #print(top_level_comment.body)
        #count = self.process_child_comments(top_level_comment.replies, count)
        #print(count)

    def process_child_comments(self, parent, count):
        for comment in parent:
            print(comment.body)
            count = self.process_child_comments(comment.replies, count)
        return count

    def stopRunning(self):
        self.exit = True
        exit()


def main():
    root = tk.Tk()
    root.geometry("300x200")
    root.title = 'CommentTreeDisplay'
    win = CommentTreeDisplay(root)
    win.pack()
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


