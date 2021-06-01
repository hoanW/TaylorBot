import praw
import random
import os

#create a bot instance
r = praw.Reddit(username = "Taylor_Bot",
                password = os.environ["reddit_password"],
                client_id = os.environ["client_id"],
                client_secret = os.environ["client_secret"],
                user_agent = "iOS:https:taylorlyricsbot:v1 (by /u/Taylor_Bot)")


if __name__ == "__main__":
    #open file
    with open("lyrics_quotes.txt") as f:
        content = f.readlines()
    trigger_answers = [x.strip() for x in content] 

    #reply to mentions  
    for m in r.inbox.stream(): #fetch messages as an iterable
        try: 
            if m in r.inbox.mentions() and m in r.inbox.unread(): #if m in mentions and is unread
                 m.reply(random.choice(trigger_answers))
                 m.mark_read() #mark as read
        except praw.exceptions.APIException:
            print("I can't function properly right now, maybe because of rate limit?")

    #reply to comments
    # phrases to trigger the bot
    trigger_phrases = ["!TaylorBot", "!Taylor_Bot", "Taylor Swift", "lyrics"]

    subreddit = r.subreddit("TaylorSwift")
    for comment in subreddit.stream.comments():
        try:
            for phrase in trigger_phrases:
                if phrase in comment.body:
                    comment.reply(random.choice(trigger_answers))
        except praw.exceptions.APIException:
            print("I can't function properly right now, maybe because of rate limit?")

