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
    #open answers file
    with open("lyrics_quotes.txt") as f:
        content = f.readlines()
    trigger_answers = [x.strip() for x in content] 

    #reply to mentions  
    for m in r.inbox.mentions(limit=50): #fetch 50 recent mentions
      try: 
            if m in r.inbox.unread(): #if mention is unread
                 m.reply(random.choice(trigger_answers))
                 m.mark_read() #mark as read
        except praw.exceptions.APIException:
            print("I can't function properly right now, maybe because of rate limit?")

    #reply to comments
    trigger_phrase = "Taylor Swift" #phrases to trigger the bot
    COMMENT_FOOTER = "\n\n\n `I am a bot who likes quoting Taylor Swift's song lyrics`"

    subreddit = r.subreddit("all")
    for comment in subreddit.stream.comments(skip_existing = True): #streaming comments from all subreddits
        try:
            if trigger_phrase in comment.body and comment.author != "Taylor_Bot": #if the comment is not made by this own bot and contains the word Taylor Swift
                comment.reply(random.choice(trigger_answers) + COMMENT_FOOTER)
                comment.upvote()
        except praw.exceptions.APIException:
            print("I can't function properly right now, maybe because of rate limit?")

