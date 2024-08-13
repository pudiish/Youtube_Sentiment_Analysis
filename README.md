# YouTube Comment Sentiment Analyzer

This Python script allows you to scrape comments from a YouTube video, analyze the sentiment of those comments using TextBlob, and generate insights, summaries, and statistics about the comments. The script also retrieves video statistics like the number of likes and comments, and provides detailed information on the top comment based on sentiment and engagement.

## Features

- **Comment Scraping:** Extracts all comments from a specified YouTube video.
- **Sentiment Analysis:** Analyzes the sentiment of each comment and ranks them from most positive to most negative.
- **Summary Generation:** Creates a concise summary of the top comments.
- **Video Statistics:** Retrieves and displays basic statistics for the video (likes, comments).
- **Top Comment Analysis:** Provides detailed statistics on the top comment, including likes and replies.
- **Conclusion Generation:** Generates a conclusion based on the most positive and most negative comments.

## Requirements

- Python 3.x
- `google-api-python-client` for interacting with YouTube Data API.
- `textblob` for sentiment analysis.
- `csv` for saving comment data.

You can install the necessary Python packages using pip:

```bash
pip install google-api-python-client textblob


Replace the API Key:

Open the script and replace 'YOUR_API_KEY' with your actual YouTube Data API key. You can obtain the API key by following the instructions here.

Replace the Video ID:

Replace the VIDEO_ID variable in the script with the ID of the YouTube video you want to analyze.

Run the script:

bash
Copy code
python youtube_comment_sentiment_analyzer.py
Output:

The script will save a CSV file named top_comments_with_sentiments.csv containing comments and their corresponding sentiment scores.
It will also print the overall sentiment, summary, and various statistics to the console.

