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
            # Wait until next update
            time.sleep(self.update_speed)

            # Check for updates


def testprint(input):
    print(input)

def main():
    root = tk.Tk()
    root.geometry("300x300")
    root.title('Update Tree Display')
    win = UpdateTreeDisplay(root)
    win.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
