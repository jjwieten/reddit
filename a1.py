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


class IncomingSubmissions(tk.Frame):
    """The top-level class for submission processing"""

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.queue = []
        self.paused = False
        self.speed_scale = 1
        self.blacklist = []
        self.whitelist = []

        self.scale = tk.Scale(self)
        self.scale.pack()

    def GetSpeed(self):
        return self.speed_scale
    
    def SetSpeed(self, NewSpeed):
        self.speed = NewSpeed

    def TogglePause(self):
        if self.paused:
            self.paused = False
            print('Resumed submissions, queue = {0}'.format(len(self.queue)))
        else:
            self.paused = True
            print('Paused submissions.')

    def incoming(self):
        last_post = None
        while True:
            for submission in reddit.subreddit("all").new(limit=1):
                # Prevent re-printing of latest post
                if last_post == submission:
                    pass
                # Check whitelist
                elif self.whitelist:
                    if submission.subreddit in self.whitelist:
                        self.queue.append(submission)
                # If whitelist isn't present, check blacklist
                elif self.blacklist:
                    if submission.subreddit not in self.blacklist:
                        self.queue.append(submission)
                # If neither are present, add by default.
                else:
                    self.queue.append(submission)
                # Save submission as last weighed post
                last_post = submission

    def post(self):
        while True:
            if not self.paused:
                if self.queue:
                    submission = self.queue.pop(0)
                    print(submission.subreddit, submission.title)


def makeSpeedLabel(root,speed):
    speedLabel = tk.Label(root, text="The incoming submissions speed is "+str(speed))
    speedLabel.pack()


def main():
    root = tk.Tk()
    root.title("Incoming reddit submissions")
    root.geometry('600x400')

    interface = IncomingSubmissions(root)

    # Scale to set the speed
    speed = tk.DoubleVar()
    s = tk.Scale(root, variable=speed, orient=tk.HORIZONTAL, from_=1, to=10)
    sb = tk.Button(root, text="Set this speed",
                   command=lambda: [interface.SetSpeed(speed.get()), makeSpeedLabel(root, speed.get())])
    sb.pack()
    s.pack()

    # Button to pause/unpause the incoming submissions
    b = tk.Button(None, text="Pauze/Unpause", command=interface.TogglePause)
    b.pack()

    # Treeview widget to display incoming submissions
    tree = ttk.Treeview(root, columns='Title')
    tree.insert('', 0, 'TEST', text='Applications')
    tree.insert('', 0, 'gallery', text='Applications 2')
    tree.pack()
    t1 = threading.Thread(target=interface.incoming)
    t2 = threading.Thread(target=interface.post)
    t1.start()
    t2.start()

    root.mainloop()


if __name__ == "__main__":
    main()
