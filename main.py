from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import historyIDScraper as scraper

# Replace with API key and the video ID you're interested in
DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
VIDEO_ID = ""


def contains_all_words(text, words):
    for word in words:
        if word not in text:
            return False
    return True


def get_comments(service, **kwargs):
    comments = []
    results = service.commentThreads().list(**kwargs).execute()
    counter = 5

    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

            # Get replies
            if item['snippet']['totalReplyCount'] > 0:
                for reply in item['replies']['comments']:
                    comments.append(reply['snippet']['textDisplay'])

        # Check if there are more pages
        if 'nextPageToken' in results and counter > 0:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.commentThreads().list(**kwargs).execute()
            counter = counter - 1
        else:
            break

    return comments


if __name__ == "__main__":
    # Build the service object
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    urls = scraper.get_URLS()
    words = ["high school", "realize", "work"]

    for i in range(len(urls)):
        try:
            comments = get_comments(youtube, part='snippet,replies', videoId=urls[i], textFormat='plainText')
            for comment in comments:
                if contains_all_words(comment, words):
                    print(f"Found a comment. URL is: {urls[i]}")
                    print(comment)
        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
