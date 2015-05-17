import time
import praw
from praw.helpers import comment_stream
import json
import urllib.request
from ProcessedContentHandler import ProcessedContentHandler
from Processor import RedditCommentProcessor

processed = []


class CatFacts:
    reddit = None  # Reddit instance used to communicate with Reddit
    processed_comments = []  # Processed comments so that we don't re-post to comment's already found

    def __init__(self):
        self.reddit = praw.Reddit('CatFacts by SubscribeToCatFacts')  # Reddit requires a unique user agent
        self.reddit.login()  # Reddit login details will be set in the praw.ini file. See praw's documentation.

        # Get any previously processed comments as the application may have crashed / Reddit may have gone down
        self.processed_comments = ProcessedContentHandler.get_processed_comments()

        # Let the user know that the program has launched!
        print("CatFacts is online...")

    @staticmethod
    def get_fact():
        url_response = urllib.request.urlopen("http://catfacts-api.appspot.com/api/facts")
        str_response = url_response.readall().decode('utf-8')
        obj = json.loads(str_response)
        return obj["facts"][0]

    def process_comments(self):
        try:
            sr = self.reddit.get_subreddit('jimmiescrew')
            hot_posts = sr.get_hot()  # Get hot posts in the subreddit...

            for p in hot_posts:
                print("Submission: " + p.title)
                p.replace_more_comments()
                flat_comments = praw.helpers.flatten_tree(p.comments)

                comments_processor = RedditCommentProcessor()

                matched_comments = comments_processor.process_comments(flat_comments)
                """:type : list[praw.objects.Comment] """

                if matched_comments is not None:
                    print("Matched comments detected in thread!")
                    for comment in matched_comments:
                        if comment.id not in self.processed_comments:
                            # Mark comment as processed
                            ProcessedContentHandler.handle_processed_comment(comment.id)
                            self.processed_comments.append(comment.id)

                            # Reply to comment with a fact!
                            try:
                                comment.reply("Meow! Here is today's cat fact: " + self.get_fact() + "For more facts,"
                                                                                                     " reply with "
                                                                                                     "catnip!")

                                print("Replied to comment " + comment.id + " with a fact!")
                            except praw.errors.RateLimitExceeded:
                                print("Rate limit exceeded posting comment!")

        except praw.errors.RateLimitExceeded:
            print("Rate limit exceeded processing comments!")
            time.sleep(60)

# Launch the program!
c = CatFacts()

while True:
    c.process_comments()
    print("All hot threads processed... Sleeping for 20 seconds before next run.")
    time.sleep(20)