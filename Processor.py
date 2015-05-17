__author__ = 'bmagee'

import praw
import random

class RedditCommentProcessor:
    target_phrases = []  # Phrases to look for in comments

    def __init__(self):
        target_phrases_file = open('config/target_phrases.csv', 'r')
        target_phrases_content = target_phrases_file.read()
        self.target_phrases = target_phrases_content.split(',')
        target_phrases_file.close()

    def process_comments(self, comments):
        """
        Take comments from a Reddit thread (in a list form) and look for
        targeted phrases...

        :type comments list[praw.objects.Comment]
        :param comments:
        """

        matched_comments = []
        """:type : list[praw.objects.Comment] """

        for comment in comments:
            print("Comment (" + comment.id + "): " + comment.body)
            for phrase in self.target_phrases:
                if phrase.lower() in comment.body.lower() and "meow" not in comment.body.lower():
                    print("Comment " + comment.id + " matched against phrase " + phrase)

                    if phrase.lower() is not "catnip" or phrase.lower() is not "i would like to subscribe to cat facts":
                        # Play a chance game as to whether to post a comment!
                        # Currently a 20% chance of posting a comment
                        if random.randrange(0, 100) < 20:
                            matched_comments.append(comment)
                    else:
                        # If the user replied with catnip we know they want a response!
                        matched_comments.append(comment)

        return matched_comments