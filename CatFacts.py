import time
import praw
from praw.helpers import comment_stream
import json
import urllib.request

target_text = ['subscribe to cat facts', 'catnip', 'cat', 'cats']

processed = ['crasook', 'craziol']

r = praw.Reddit('CatFacts by SubscribeToCatFacts')
r.login('SubscribeToCatFacts', 'BroadwayCats')
r.config.api_request_delay = 120

print("Launching CatFacts...")

def comments():
    try:
        sr = r.get_subreddit('aww')
        hot_posts = sr.get_hot()

        for p in hot_posts:
            print("Submission: " + p.title)
            p.replace_more_comments()
            flat_comments = praw.helpers.flatten_tree(p.comments)
            for c in flat_comments:
                print("Comment: " + c.id)
                for t in target_text:
                    if t in c.body and c.id not in processed and "Meow" not in c.body:
                        print("Comment text: " + c.body)
                        url_response = urllib.request.urlopen("http://catfacts-api.appspot.com/api/facts")
                        str_response = url_response.readall().decode('utf-8')
                        obj = json.loads(str_response)
                        fact = obj["facts"][0]

                        c.reply("Meow! Here is today's cat fact: " + fact + " For more facts, reply with catnip!"
                                                                            "\n"
                                                                            "\n"
                                                                            "\n"
                                                                            "\n"
                                                                            "------------------\n"
                                                                            "Disclaimer: I am new. Please PM me if you find me annoying!")
                        processed.append(c.id)
                        time.sleep(120)
    except praw.errors.RateLimitExceeded:
        print("Rate limit exceeded! Resting for 2 minutes...")
        time.sleep(120)
        print("Well rested! Begin searching again!")

while True:
    comments()
    time.sleep(10)