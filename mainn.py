import csv
import pandas as pd
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import apike


# Create a YouTube service object
youtube = build('youtube', 'v3', developerKey=apike.api_key)

def get_video_comments(video_id):
    comments = []
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=100
        )

        while request:
            response = request.execute()
            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)

            request = youtube.commentThreads().list_next(request, response)
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred. {e._get_reason()}")

    return comments

def search_videos(query):
    all_comments = []
    try:
        # Make the search request to YouTube API
        search_request = youtube.search().list(
            q=query,
            part='snippet',
            type='video',
            maxResults=5  # Get top 5 videos
        )

        # Execute the request and extract video IDs
        response = search_request.execute()
        video_ids = [item['id']['videoId'] for item in response['items']]

        # Get comments for each video
        for video_id in video_ids:
            video_comments = get_video_comments(video_id)
            all_comments.extend(video_comments)
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred. {e._get_reason()}")

    return all_comments

try:
    # Get user input
    user_input = input("Enter a topic to search for: ")

    # Search for videos based on user input and get comments
    comments = search_videos(user_input)

    # Save comments to a CSV file
    with open("all_comments.csv", "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Comments"])  # Write header
        for comment in comments:
            writer.writerow([comment])

    print("All comments saved to all_comments.csv")
except HttpError as e:
    print(f"An HTTP error {e.resp.status} occurred. {e._get_reason()}")
except Exception as e:
    print(f"An error occurred: {str(e)}")



df=pd.read_csv('all_comments.csv')
userinput=df['Comments'].tolist()

import emoji
positive_emojis = ['💪','🚩','😊', '😄', '😍', '👍', '👏', '🌟', '💯', '❤️', '🎉', '👌', '🥳', '✨', '🙌', '🌈', '😁', '😃', '😇', '🤗', '🥰', '🤩', '🤗', '🥳', '🎊', '🎈', '🎶', '🎵', '🎼', '🎸', '🎷', '🎹', '🎮', '🎰', '🎲', '🎳', '🎯', '🏆', '🥇', '🥈', '🥉', '🏅', '🏵️', '🎖️', '🏅', '🎗️', '🏵️', '🎗️', '🏵️', '🎗️', '🎖️', '🏵️', '🎗️', '🏵️', '🎗️', '🎖️', '🏵️', '🎗️', '🏵️', '🎗️', '🎖️', '🏵️', '🎗️', '🏵️', '🎗️', '🎖️', '🏵️', '🎗️', '🏵️', '🎗️', '🎖️', '🏵️', '🎗️', '🏵️', '🎗️', '🎖️', '🏵️', '🎗️', '🏵️', '🎗️', '🎖️', '🏵️', '🎗️', '🏵️', '🎗️', '🎖️', '🏵️', '🎗️', '🏵️', '🎗️', '🎖️', '🏵️', '🎗️', '🏵️', '🎗️', '🎖️', '🏵️', '🎗️', '🏵️', '🎗️', '🎖️', '🏵️', '🎗️', '🏵️', '🎗️', '🎖️', '🏵️', '🎗️', '🏵️', '🎗️','❤','🔥','👏']
negative_emojis = ['😞', '😔', '😩', '😒', '😢', '😭', '👎', '💔', '😡', '🙁']
extranegetive_orcuss=['godi']
from nltk.corpus import opinion_lexicon

# Load positive and negative words
positive_words = set(opinion_lexicon.positive())

negative_words = set(opinion_lexicon.negative())
negative_words |= set(extranegetive_orcuss)
totalval = []

for sentence in userinput:
    try:
        sentence = sentence.lower()
    except AttributeError as e:
        print(f"An error occurred: {e}")
    try:
        wordval = 0  # Reset wordval for each sentence
        words = sentence.split()
        
        for word in words:
            if word in positive_words:
                wordval += 1
            elif word in negative_words:
                wordval -= 1
            else:
                wordval += 0
        
        # Handling emojis separately
        for char in sentence:
            if char in positive_emojis:
                wordval += 1
            elif char in negative_emojis:
                wordval -= 1
        
        if wordval > 0:
            totalval.append(1)
        elif wordval < 0:
            totalval.append(-1)
        else:
            totalval.append(0)
    except AttributeError as e:
        print(f"Error processing sentence: {sentence}. Error: {str(e)}")
positive=0
negetive=0
netural=0
for t in totalval:
    if t==1:
        positive+=1
    elif t==-1:
        negetive+=1
    else:
        netural+=1

total_comments=len(totalval)

positive_per=(positive/total_comments)*100
negetive_per=(negetive/total_comments)*100
netural_per=(netural/total_comments)*100
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

#  list of percentages
percentages = [positive_per,negetive_per,netural_per] 

labels = ['POSITIVE', 'NEGETIVE', 'NETURAL']  

colors = ['green', 'red', 'grey'] 

explode = (0.1, 0, 0)  # Explode the 1st slice (Positive)

plt.figure(figsize=(8, 6))
plt.pie(percentages, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('Sentiment Distribution of Comments', fontsize=16)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Display the plot
plt.show()
print("total comments=",total_comments)
print("negetive comments=",negetive)
print("positive  comments=",positive)
print("netural comments=",netural)                