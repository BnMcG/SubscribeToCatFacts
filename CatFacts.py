import time
import praw
from praw.helpers import comment_stream
import json
import urllib.request
from ProcessedContentHandler import ProcessedContentHandler
from Processor import RedditCommentProcessor
from apscheduler.schedulers.background import BackgroundScheduler

processed = []


class CatFacts:
    reddit = None  # Reddit instance used to communicate with Reddit
    processed_comments = []  # Processed comments so that we don't re-post to comment's already found
    scheduler = None

    def __init__(self):
        self.reddit = praw.Reddit('CatFacts by SubscribeToCatFacts')  # Reddit requires a unique user agent
        self.reddit.login()  # Reddit login details will be set in the praw.ini file. See praw's documentation.

        # Get any previously processed comments as the application may have crashed / Reddit may have gone down
        self.processed_comments = ProcessedContentHandler.get_processed_comments()

        # Setup the scheduler to run tasks on intervals
        self.setup_scheduler()

        # Let the user know that the program has launched!
        print("CatFacts is online...")

    def setup_scheduler(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

        comment_processor = self.scheduler.add_job(self.process_comments, 'interval', minutes=5)
        print("Scheduler configured!")

    @staticmethod
    def get_fact():
        url_response = urllib.request.urlopen("http://catfacts-api.appspot.com/api/facts")
        str_response = url_response.readall().decode('utf-8')
        obj = json.loads(str_response)
        return obj["facts"][0]

    @staticmethod
    def build_subreddit_list():
        file = open('config/subreddits.csv')
        file_contents = file.read()
        split = file_contents.split(',')
        file.close()

        subreddits = ''

        for subreddit in split:
            subreddits += subreddit + "+"

        return subreddits

    def process_comments(self):
        try:
            sr = self.reddit.get_subreddit(self.build_subreddit_list())
            hot_posts = sr.get_hot(limit=100)  # Get hot posts in the subreddit...

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
                                comment.reply("Meow! Here is today's cat fact: " + self.get_fact() + " For more facts,"
                                                                                                     " reply with "
                                                                                                     "[catnip](https://www.reddit.com/r/subscribetocatfacts)!")

                                print("Replied to comment " + comment.id + " with a fact!")
                            except praw.errors.RateLimitExceeded:
                                print("Rate limit exceeded posting comment!")

        except praw.errors.RateLimitExceeded:
            print("Rate limit exceeded processing comments!")
            time.sleep(60)

# Launch the program!
c = CatFacts()

while True:
    time.sleep(0.001)  # Keeps the application open... Terrible fix but seems to work