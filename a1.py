import praw


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
        # print(comment.body)
        count = process_child_comments(comment.replies, count)
    return count


subreddit = reddit.subreddit("thenetherlands")

for submission in subreddit.hot(limit=1):
    submission.comments.replace_more(limit=None)
    print(submission.title)
    count = 0
    for top_level_comment in submission.comments.list():
        count += 1
        # print(top_level_comment.body)
        # count = process_child_comments(top_level_comment.replies, count)
    print(count)
