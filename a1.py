import praw
import tkinter as tk
import threading
import time


reddit = praw.Reddit(
    username="jj_bot_hci",
    password="s3786617",
    client_id="hEahD4o3y7iGerSQsrwveg",
    client_secret="tf_fC8X0bFb-W0TkxUPjPHm6jReQ0A",
    user_agent="hci"
)


class IncomingSubmissions:
    """The top-level class for submission processing"""
    def __init__(self):
        self.queue = []
        self.paused = False
        self.speed_scale = 1
        self.blacklist = []
        self.whitelist = []
       
    def GetSpeed(self):
        return self.speed_scale

    def TogglePause(self):
        if self.paused:
            self.paused = False
            print(self.paused)
        else:
            self.paused = True
            print(self.paused)
        
    def incoming(self):
        last_post = None
        while True:
            if not self.paused:
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
            if self.queue:
                submission = self.queue.pop(0)
                print(submission.subreddit, submission.title)

def MakeFrame(intf):
    root = tk.Tk()
    root.title("Incoming reddit submissions")
    root.geometry('600x600')

    # Label that shows the current speed
    speedLabel = tk.Label(root, text="The incoming submissions speed is "+ str(intf.GetSpeed()))
    speedLabel.pack()
    
    #Button to pause/unpause the incoming submissions
    b = tk.Button(None, text="Pauze/Unpause", command=intf.TogglePause)
    b.pack()

    # Scale to set the speed

    return root


def main():
    interface = IncomingSubmissions()
    root = MakeFrame(interface)
    root.mainloop()
    
    # TypeError: get() missing 1 required positional argument: 'self'
    # Cause: threading passes one less argument than desired due to the usage of self in the interface class
    t1 = threading.Thread(target=interface.incoming)
    t2 = threading.Thread(target=interface.post)
    t1.start()
    t2.start()


if __name__ == "__main__":
    main()
