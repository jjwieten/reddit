import praw
import tkinter as tk
from tkinter import ttk
import time


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

        self.comments_ids = set()

        self.submid = ""

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
            self.submid = id
            self.showComments(id)
        except IndexError:
            e = tk.Label(top, text="Please enter a valid URL\n")
            e.pack()

        #start update cycle
        UpdateTreeDisplay.UpdateTree()

    def showComments(self, c_id):
        """
        Find all top level comments
        """
        submission = reddit.submission(id=c_id)
        for comment in submission.comments:
            self.comments_ids.add(comment.id)
            self.tree.insert('', tk.END, text=comment.body, iid=comment.id, open=False)
            self.process_child_comments(comment.replies, comment)

    def process_child_comments(self, parent, parent_id):
        """
        Recursive: find all child comments
        """
        for comment in parent:
            self.comments_ids.add(comment.id)
            self.tree.insert('', tk.END, text=comment.body, iid=comment.id, open=False)
            self.tree.move(comment.id, parent_id, 0)
            self.process_child_comments(comment.replies, comment.id)

    def stopRunning(self):
        """
        Funciton to exit program
        """
        self.exit = True
        exit()

class ResponseCommentTreeDisplay(CommentTreeDisplay):
    """Make frame for adding responses by user to selected comments"""
    def __init__(self, root):
        # tk.Frame.__init__(self, CommentTreeDisplay)
        super().__init__(root)
        # Counting intreger to append to comment
        self.comment_int = 0
        self.tree.bind("<Double-1>", self.double_click_comment)

    def double_click_comment(self, event):
        """
        Make input window and get input
        """
        item_id = event.widget.focus()
        # Create response window
        top = tk.Tk()
        top.geometry("300x100")
        popup = tk.Entry(top)
        # Set button response
        url_btn = tk.Button(top, text="Submit comment",
                            command=lambda: self.add_comment_to_tree(item_id, popup.get(), top))
        popup.pack()
        url_btn.pack()
        top.mainloop()

    def add_comment_to_tree(self, parent_id, comment_text, top):
        """
        Add the user input (comment) to the tree below the selected comment
        """
        if comment_text != "":
            # Generate an iid for Treeview comment
            comment_id = "{0}_{1}".format(parent_id, self.comment_int)
            self.comment_int += 1
            self.tree.insert('', tk.END, text=comment_text, iid=comment_id, open=False)
            self.tree.move(comment_id, parent_id, 0)
            top.destroy()
        else:
            e = tk.Label(top, text="Please enter a valid URL\n")
            e.pack()

class UpdateTreeDisplay(ResponseCommentTreeDisplay):
    def __init__(self, root):
        super().__init__(root)

        #sleep time in seconds
        self.update_speed = 60

        # Scale widget for update speed
        self.speed_scale = tk.Scale(self, variable=self.update_speed, label="Update speed in sec.",
                                    orient=tk.HORIZONTAL, from_=15, to=120, length=150)
        self.speed_scale.pack()


    def UpdateTree(self):
        while True:
            print("wono")
            # Wait until next update
            time.sleep(self.update_speed)

            # Check for updates
            self.showNewComments(self.submid)
            # Wait until next update
            time.sleep(self.update_speed)

    def showNewComments(self, c_id):
        """
        Find all top level comments
        """
        submission = reddit.submission(id=c_id)
        for comment in submission.comments:
            if comment.id not in self.comments_ids:
                self.tree.insert('', tk.END, text=comment.body, iid=comment.id, open=False)
                self.process_new_child_comments(comment.replies, comment)
                self.comments_ids.add(comment.id)


    def process_new_child_comments(self, parent, parent_id):
        """
        Recursive: find all child comments
        """
        for comment in parent:
            if comment.id not in self.comments_ids:
                self.tree.insert('', tk.END, text=comment.body, iid=comment.id, open=False)
                self.tree.move(comment.id, parent_id, 0)
                self.comments_ids.add(comment.id)
                self.process_child_comments(comment.replies, comment.id)


def main():
    root = tk.Tk()
    root.geometry("300x300")
    root.title('Update Tree Display')

    win = ResponseCommentTreeDisplay(root)
    win.pack()
    root.mainloop()


if __name__ == "__main__":
    main()