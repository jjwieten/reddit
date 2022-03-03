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


def main():
    # Create and configure root
    root = tk.Tk()
    root.title("Incoming reddit submissions")
    root.geometry('700x300')

    # Create and pack an IncomingSubmissions instance
    interface = IncomingSubmissions(root)
    interface.pack()

    # Loop
    root.mainloop()


if __name__ == "__main__":
    main()
