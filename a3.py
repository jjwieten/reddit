import praw
import tkinter as tk
from a2 import CommentTreeDisplay


reddit = praw.Reddit(
    username="hci_bot_a1",
    password="s3786617",
    client_id="4-WmhNJXd3n-ZhCsOa3XAQ",
    client_secret="tOBLYrbRKLcz6yDyR8ypNBPcUfL_sw",
    user_agent="hci"
)


class ResponseCommentTreeDisplay(CommentTreeDisplay):
    """Make frame for adding responses by user to selected comments"""
    def __init__(self, root):
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


def main():
    root = tk.Tk()
    root.geometry("300x200")
    root.title('ResponseCommentTreeDisplay')
    win = ResponseCommentTreeDisplay(root)
    win.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
