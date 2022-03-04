import praw
import tkinter as tk
from tkinter import ttk
import threading
import time
from a2 import CommentTreeDisplay

reddit = praw.Reddit(
    username="hci_bot_a1",
    password="s3786617",
    client_id="4-WmhNJXd3n-ZhCsOa3XAQ",
    client_secret="tOBLYrbRKLcz6yDyR8ypNBPcUfL_sw",
    user_agent="hci"
)


class ResponseCommentTreeDisplay(CommentTreeDisplay):
    def __init__(self, root):
        super().__init__(root)

