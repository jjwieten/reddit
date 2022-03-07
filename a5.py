import praw
import tkinter as tk
from tkinter import ttk
import threading
from time import sleep

reddit = praw.Reddit(
    username="hci_bot_a1",
    password="s3786617",
    client_id="4-WmhNJXd3n-ZhCsOa3XAQ",
    client_secret="tOBLYrbRKLcz6yDyR8ypNBPcUfL_sw",
    user_agent="hci"
)


class IncomingSubmissions(tk.Frame):
    """Widget class for submission processing"""
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.queue = []
        self.speed_val = tk.DoubleVar()
        self.paused = False
        self.filter_status = tk.StringVar()
        self.filter_list = []

        # Treeview widget for submission viewing
        self.tree = ttk.Treeview(self, columns='Title')
        self.tree.column('Title', width=400)
        self.tree.pack(side='right')
        # Treeview bind for submission viewing
        self.tree.bind("<Double-1>", RedditNotebook.open_submission)

        # Scale widget for submission speed
        self.speed_scale = tk.Scale(self, variable=self.speed_val, label="Queue delay",
                                    orient=tk.HORIZONTAL, from_=0, to=5, length=150)
        self.speed_scale.pack()

        # Button widget for queue pause
        self.pause_status = tk.StringVar()
        self.pause_status.set("Pause")
        self.pause_button = tk.Button(None, textvariable=self.pause_status, command=self.TogglePause)
        self.pause_button.pack(side='bottom')

        # Button widget for subreddit filtering
        self.filter_status.set("Blacklist")
        self.pause_button = tk.Button(None, textvariable=self.filter_status, command=self.ToggleFilter)
        self.pause_button.pack(side='bottom')

        # Text widget for subreddit filtering
        self.sublist = tk.Text(self, width=20, height=10)
        self.sublist.pack(side='left')

        # Prepare and start threads
        self.t1 = threading.Thread(target=self.incoming)
        self.t2 = threading.Thread(target=self.post)
        self.t1.start()
        self.t2.start()

    def TogglePause(self):
        """
        Toggles self.paused between True and False
        """
        if self.paused:
            self.paused = False
            self.pause_status.set("Pause")
            print('Resumed submissions, queue = ', len(self.queue))
        else:
            self.paused = True
            self.pause_status.set("Resume")
            print('Paused submissions.')

    def ToggleFilter(self):
        """
        Toggles self.filter_status between blacklist and whitelist
        """
        if self.filter_status.get() == 'Blacklist':
            self.filter_status.set('Whitelist')
            print('Set filter to', self.filter_status.get(), self.filter_list)
        else:
            self.filter_status.set('Blacklist')
            print('Set filter to', self.filter_status.get(), self.filter_list)

    def GetFilterList(self):
        """
        Updates filter_list for self.post
        """
        sublist = self.sublist.get("1.0", tk.END).strip().lower().split('\n')
        return sublist

    def incoming(self):
        """
        Obtains submissions from Reddit and queues them.
        """
        print('Loaded fetching thread (t1)')
        last_post = None
        while True:
            for submission in reddit.subreddit("all").new(limit=1):
                # Prevent re-printing of latest post
                if last_post == submission:
                    pass
                else:
                    self.queue.append(submission)
                # Save submission as last weighed post
                last_post = submission

    def post(self):
        """
        Empties in-class queue into Treeview after filtering
        """
        print('Loaded posting thread (t2)')
        while True:
            if not self.paused:
                if self.queue:
                    submission = self.queue.pop(0)
                    self.filter_list = self.GetFilterList()
                    # Check whitelist
                    if self.filter_status.get() == 'Whitelist' \
                            and submission.subreddit.display_name.lower() not in self.filter_list:
                        print('Blocked post from ', submission.subreddit)
                        pass
                    # If whitelist isn't present, check blacklist
                    elif self.filter_status.get() == 'Blacklist' \
                            and submission.subreddit.display_name.lower() in self.filter_list:
                        print('Blocked post from ', submission.subreddit)
                        pass
                    # If neither are present, add by default.
                    else:
                        self.tree.insert('', 0, submission.id, text=submission.subreddit, values=[submission.title])
                        # print(submission.subreddit, submission.title, "queue = ", len(self.queue))
                        sleep(self.speed_val.get())


class CommentTreeDisplay(tk.Frame):
    """ Class for creating comment tree """
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.topframe = tk.Frame(self)
        self.exit = False

        self.tree = ttk.Treeview(self)
        self.tree.pack()

    def load_comments(self):
        """
        Make window to enter url and receive input
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
                c_id = url_in.split("/")[-3]
            else:
                c_id = url_in.split("/")[-2]
            top.destroy()
            self.showComments(c_id)
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
        Function to exit program
        """
        self.exit = True
        exit()


class ResponseCommentTreeDisplay(CommentTreeDisplay):
    """Make frame for adding responses by user to selected comments"""
    def __init__(self, root):
        # tk.Frame.__init__(self, CommentTreeDisplay)
        super().__init__(root)
        # Counting integer to append to comment
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


class RedditNotebook(ttk.Notebook):
    """
    Merge all displays and trees
    """
    def __init__(self, **kw):
        super().__init__(**kw)
        sub_frame = IncomingSubmissions(self)
        com_frame = ResponseCommentTreeDisplay(self)
        self.ctd = CommentTreeDisplay(self)

    def open_submission(self, event):
        item_id = event.widget.focus()
        print(item_id)
        CommentTreeDisplay.showComments(ttk.Notebook, item_id)
        # new_frame = ResponseCommentTreeDisplay(nb)
        # nb.add(new_frame, text='item_id')


def main():
    # Create window
    root = tk.Tk()
    root.geometry('700x300')
    n = ttk.Notebook(root)

    submission_frame = IncomingSubmissions(n)  # first page, which would get widgets gridded into it
    comment_frame = ResponseCommentTreeDisplay(n)  # second page

    # Create menubar
    menubar = tk.Menu()
    # Add file menu
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Exit", command=comment_frame.stopRunning)
    menubar.add_cascade(label="File", menu=file_menu)
    # Add processing menu
    proc_menu = tk.Menu(menubar, tearoff=0)
    proc_menu.add_command(label="Load comments", command=comment_frame.load_comments)
    menubar.add_cascade(label="Processing", menu=proc_menu)
    root.config(menu=menubar)

    n.add(submission_frame, text='Submissions')
    n.add(comment_frame, text='Comments')
    n.pack(expand=1, fill='both')
    root.mainloop()


if __name__ == "__main__":
    main()
