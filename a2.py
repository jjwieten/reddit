import praw
import tkinter as tk
from tkinter import ttk

reddit = praw.Reddit(
    username="hci_bot_a1",
    password="s3786617",
    client_id="4-WmhNJXd3n-ZhCsOa3XAQ",
    client_secret="tOBLYrbRKLcz6yDyR8ypNBPcUfL_sw",
    user_agent="hci"
)


class CommentTreeDisplay(tk.Frame):
    """ Class for creating comment tree """
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
        self.tree.pack()

    def load_comments(self):
        """
        Make window to enter url and recieve input
        """
        top = tk.Tk()
        top.geometry("300x100")
        popup = tk.Entry(top)
        url_btn = tk.Button(top, text="Submit URL", command=lambda: self.get_url(popup.get(), top))
        popup.pack()
        url_btn.pack()
        top.mainloop()

    def get_url(self, url_in, top):
        """
        From input get the comment id, or return error message
        """
        try:
            if url_in[-1] == "/":
                id = url_in.split("/")[-3]
            else:
                id = url_in.split("/")[-2]
            top.destroy()
            self.showComments(id)
        except IndexError:
            e = tk.Label(top, text="Please enter a valid URL\n")
            e.pack()

    def showComments(self, c_id):
        """
        Find all top level comments
        """
        submission = reddit.submission(id=c_id)
        for comment in submission.comments:
            self.tree.insert('', tk.END, text=comment.body, iid=comment.id, open=False)
            self.process_child_comments(comment.replies, comment)

    def process_child_comments(self, parent, parent_id):
        """
        Recursive: find all child comments
        """
        for comment in parent:
            self.tree.insert('', tk.END, text=comment.body, iid=comment.id, open=False)
            self.tree.move(comment.id, parent_id, 0)
            self.process_child_comments(comment.replies, comment.id)

    def stopRunning(self):
        """
        Funciton to exit program
        """
        self.exit = True
        exit()


def main():
    # Make window
    root = tk.Tk()
    root.geometry("300x200")
    root.title('CommentTreeDisplay')
    win = CommentTreeDisplay(root)
    win.pack()
    root.mainloop()


if __name__ == "__main__":
    main()

