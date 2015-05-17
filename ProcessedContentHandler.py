__author__ = 'bmagee'


class ProcessedContentHandler:

    @staticmethod
    def handle_processed_comment(comment_id):
        # Open CSV file and append the processed ID to it
        file = open('config/processed_comments.csv', 'a')
        file.write(comment_id + ',')
        file.close()

    @staticmethod
    def get_processed_comments():
        # Open CSV file of processed comments
        file = open('config/processed_comments.csv', 'r')
        contents = file.read()
        file.close()
        return contents.split(',')

