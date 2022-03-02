# Moved the unused functions from a1 to here because they regard comments, not submissions.

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
