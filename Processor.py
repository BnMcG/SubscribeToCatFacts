__author__ = 'bmagee'

import praw
import random
import re

class RedditCommentProcessor:
    target_phrases = []  # Phrases to look for in comments
    percentage_chance = None  # Chance of posting a comment

    def __init__(self):
        target_phrases_file = open('config/target_phrases.csv', 'r')
        target_phrases_content = target_phrases_file.read()
        self.target_phrases = target_phrases_content.split(',')
        target_phrases_file.close()

        percentage_chance_file = open('config/percentage_chance.txt', 'r')
        self.percentage_chance = percentage_chance_file.read()
        percentage_chance_file.close()

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
            for phrase in self.target_phrases:
                expression = re.compile(r'(.)*\b' + phrase + r'\b(.)*', re.IGNORECASE)
                if expression.match(comment.body.lower()) is not None and "meow" not in comment.body.lower():
                    print("Comment " + comment.id + " matched against phrase " + phrase)

                    if "catnip" in phrase.lower() or "i would like to subscribe to cat facts" in phrase.lower():
                        # If the user replied with these phrases we know they want a response!
                        matched_comments.append(comment)
                    else:
                        # Play a chance game as to whether to post a comment!
                        if random.randrange(0, 100) < int(self.percentage_chance):
                            matched_comments.append(comment)

        return matched_comments