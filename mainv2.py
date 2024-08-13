import os
import csv
from googleapiclient.discovery import build
from textblob import TextBlob

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = 'AIzaSyD4L2fnzwFH1liZjryge9lhQXzOdeqmMww'
VIDEO_ID = '0K7LJOy_KdU'  # Replace with the YouTube video ID you want to scrape comments from


# Create a YouTube Data API service
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Get all comments for the video
def get_all_comments(video_id):
    all_comments = []

    # You can retrieve up to 100 comments per page, and we'll use nextPageToken to iterate through all pages.
    next_page_token = None
    while True:
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            order='relevance',
            maxResults=100,
            pageToken=next_page_token,
        ).execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            all_comments.append(comment)

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return all_comments

def perform_sentiment_analysis(comments):
    sentiments = []
    for comment in comments:
        blob = TextBlob(comment)
        sentiment = blob.sentiment.polarity
        sentiments.append((comment, sentiment))

    # Sort comments based on sentiment (highest sentiment first)
    sorted_comments = sorted(sentiments, key=lambda x: x[1], reverse=True)

    return sorted_comments

def create_summary(sorted_comments):
    summary = ""
    word_count = 0
    for comment, _ in sorted_comments:
        words = comment.split()
        if word_count + len(words) <= 100:
            summary += comment + " "
            word_count += len(words)
        else:
            break

    return summary.strip()

def get_video_statistics(video_id):
    response = youtube.videos().list(
        part='statistics',
        id=video_id,
    ).execute()

    if 'items' in response:
        item = response['items'][0]
        likes = int(item['statistics']['likeCount'])
        comments = int(item['statistics']['commentCount'])
        return likes, comments
    else:
        return 0, 0

def get_comment_statistics(comment_id):
    response = youtube.comments().list(
        part='snippet',
        id=comment_id,
    ).execute()

    if 'items' in response:
        item = response['items'][0]
        likes = int(item['snippet']['likeCount'])

        # Check if the comment has 'topLevelComment' field in the response
        if 'topLevelComment' in item['snippet']:
            parent_id = item['snippet']['topLevelComment']['id']
        else:
            parent_id = comment_id

        replies_response = youtube.comments().list(
            part='snippet',
            parentId=parent_id,
        ).execute()

        # Count the number of replies for the top comment
        replies_count = len(replies_response['items'])

        return likes, replies_count
    else:
        return 0, 0



def create_conclusion(most_positive_comment, most_negative_comment):
    positive_blob = TextBlob(most_positive_comment)
    negative_blob = TextBlob(most_negative_comment)

    conclusion = "The video received both positive and negative feedback from viewers. "
    conclusion += "The most positive comment was: '" + most_positive_comment + "'. "
    conclusion += "It expressed positive sentiment about the video content. On the other hand, "
    conclusion += "the most negative comment was: '" + most_negative_comment + "'. "
    conclusion += "It conveyed negative sentiment and raised concerns about certain aspects of the video. "
    conclusion += "Overall, the video generated mixed reactions, and it's essential for content creators "
    conclusion += "to consider feedback from both perspectives to improve future content."

    return conclusion

# ... (Previous code remains unchanged)

def analyze_comments(sorted_comments):
    # Get the most negative comment (lowest sentiment score)
    most_negative_comment, most_negative_sentiment = sorted_comments[-1]
    # Get the most positive comment (highest sentiment score)
    most_positive_comment, most_positive_sentiment = sorted_comments[0]

    # Sort comments based on likes (highest likes first)
    sorted_comments_by_likes = sorted(sorted_comments, key=lambda x: x[0], reverse=True)
    # Get the top comment (highest likes)
    top_comment, _ = sorted_comments_by_likes[0]

    return top_comment, most_negative_comment, most_positive_comment, most_negative_sentiment, most_positive_sentiment

# ... (Previous code remains unchanged)

if __name__ == "__main__":
    all_comments = get_all_comments(VIDEO_ID)
    if all_comments:
        sorted_comments = perform_sentiment_analysis(all_comments)

        # Calculate overall video sentiment
        overall_sentiment = sum(comment[1] for comment in sorted_comments) / len(sorted_comments)
        if overall_sentiment > 0:
            sentiment_summary = "The overall sentiment of the video is positive."
        elif overall_sentiment < 0:
            sentiment_summary = "The overall sentiment of the video is negative."
        else:
            sentiment_summary = "The overall sentiment of the video is neutral."

        # Save top comments and sentiments to a CSV file
        with open('top_comments_with_sentiments.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Comment', 'Sentiment'])
            for comment, sentiment in sorted_comments:
                writer.writerow([comment, sentiment])

        summary = create_summary(sorted_comments)

        # Analyze comments based on factors and get top, most positive, and most negative comments
        top_comment, most_negative_comment, most_positive_comment, most_negative_sentiment, most_positive_sentiment = analyze_comments(sorted_comments)

        # Get video statistics
        video_likes, video_comments = get_video_statistics(VIDEO_ID)

        # Get top comment statistics
        top_comment_id = youtube.commentThreads().list(
            part='id,snippet',
            videoId=VIDEO_ID,
            order='relevance',
            textFormat='plainText',
        ).execute()['items'][0]['id']
        top_comment_likes, top_comment_replies = get_comment_statistics(top_comment_id)

        print("Top comments and their sentiments have been saved to top_comments_with_sentiments.csv.")
        print(sentiment_summary)
        print("Summary of top comments (limited to 100 words):")
        print(summary)

        conclusion = create_conclusion(most_positive_comment, most_negative_comment)
        print("\nConclusion:")
        print(conclusion)

        print("\nVideo Statistics:")
        print("Likes:", video_likes)
        print("Comments:", video_comments)

        print("\nTop Comment Statistics:")
        print("Top Comment:", top_comment)
        print("Top Comment Likes:", top_comment_likes)
        print("Top Comment Replies:", top_comment_replies)

        print("\nMost Positive Comment:")
        print(most_positive_comment)
        print("Sentiment Score:", most_positive_sentiment)

        print("\nMost Negative Comment:")
        print(most_negative_comment)
        print("Sentiment Score:", most_negative_sentiment)

    else:
        print("No comments found for the given video ID.")
