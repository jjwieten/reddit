import praw
import tkinter as tk
import threading


reddit = praw.Reddit(
    username="jj_bot_hci",
    password="s3786617",
    client_id="hEahD4o3y7iGerSQsrwveg",
    client_secret="tf_fC8X0bFb-W0TkxUPjPHm6jReQ0A",
    user_agent="hci"
)


def process_child_comments(parent, count):
    for comment in parent:
        count += 1
        #print(comment.body)
        count = process_child_comments(comment.replies, count)
    return count


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

class Queue:
    """A Python list as submission queue"""
    def __init__(self):
        self.queue = []

    def add(self, item):
        # Add item to queue
        self.queue.append(item)

    def get(self):
        # Get top item from queue
        return self.queue.pop(0)

    def clear(self):
        # Clear queue
        self.queue = []


class IncomingSubmissions:
    """The top-level class for submission processing"""
    def __init__(self, q):
        self.queue = q
        self.paused = False
        self.speed_scale = 1
        self.blacklist = []
        self.whitelist = []

    def incoming(self):
        while True:
            if not self.paused:
                for submission in reddit.subreddit("all").new(limit=1):
                    # Check whitelist
                    if self.whitelist:
                        if submission.subreddit in self.whitelist:
                            self.queue.add(submission)
                    # If whitelist isn't present, check blacklist
                    elif self.blacklist:
                        if submission.subreddit not in self.blacklist:
                            self.queue.add(submission)
                    # If neither are present, add by default.
                    else:
                        self.queue.add(submission)

    def post(self):
        while True:
            if self.queue:
                submission = self.queue.get()
                print(submission.subreddit, submission.title)


def main():
    queue = Queue
    interface = IncomingSubmissions(queue)


if __name__ == "__main__":
    main()
