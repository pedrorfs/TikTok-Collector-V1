import asyncio
import os
import json
from dotenv import dotenv_values
from TikTokApi import TikTokApi
import time

# Load environment variables
env = dotenv_values(".env")
MODE = env.get("MODE")
USERS = env.get("USERS")
URLS = env.get("URLS")
OUTPUT_PATH = env.get("OUTPUT_PATH")
TOKEN = env.get("TOKEN")
HASHTAG = env.get("HASHTAG")

# Validate environment variables
if not all([MODE, USERS, URLS, OUTPUT_PATH, TOKEN, HASHTAG]):
    raise ValueError("One or more environment variables are missing.")

# Returns the current timestamp in the format "YYYY-MM-DD HH:MM:SS"
def get_current_timestamp():
    return int(time.time())

# Helper function to create directories if they don't exist
def create_directory(path):
    os.makedirs(path, exist_ok=True)

# Helper function to write data to a file
def write_to_file(file_path, data):
    with open(file_path, "w", encoding='utf-8') as outfile:
        outfile.write(str(data))

# Helper function to write data to a JSON file
def write_to_json_file(file_path, data):
    with open(file_path, "w", encoding='utf-8') as outfile:
        json.dump(data, outfile)

# Function to extract selected attributes from a TikTok video
def get_selected_attributes(video):
    selected_data = {
        "nickname": video["author"]["nickname"],
        "userId": video["author"]["id"],
        "privateAccount": video["author"]["privateAccount"],
        "signature": video["author"]["signature"],
        "uniqueId": video["author"]["uniqueId"],
        "verified": video["author"]["verified"],
        "videoId": video["id"],
        "createTime": video["createTime"],
        "stats": video["stats"]
    }

    if "contents" in video:
        selected_data["contents"] = video["contents"]
    if "duration" in video:
        selected_data["duration"] = video["duration"]
    
    return selected_data

def get_selected_user_info(user_info):
    selected_data = {
        "stats": user_info["userInfo"]["stats"]
    }    
    return selected_data

# Function to extract the creation time of the video
def get_create_time(video):
    return video["createTime"]

# Function to extract information from a comment
def get_comment_info(comment):
    return {
        "text": comment.text,
        "likes_count": comment.likes_count
    }

# Function to collect videos from a user
async def collect_user_videos(users, path=None):
    async with TikTokApi() as api:
        # Create session for TikTok authentication
        await api.create_sessions(ms_tokens=[TOKEN], num_sessions=1, sleep_after=3, headless=False)

        # Create a main directory to store all users' data
        current_timestamp = get_current_timestamp()
        main_directory = os.path.join(path, rf"User - {current_timestamp}")
        create_directory(main_directory)  # Ensure the main directory exists

        with open(users, 'r') as file:
            for line in file:
                user_id = line.strip()  # Extract user ID
                user_directory = os.path.join(main_directory, user_id) if path else f"./{user_id}"  # Define output directory
                create_directory(user_directory)  # Create directory if it doesn't exist

                user = api.user(user_id)  # Fetch user data
                user_info = await user.info()
                write_to_file(os.path.join(user_directory, "userInfo.txt"), get_selected_user_info(user_info))

                async for video in user.videos(count=30):  # Fetch user videos
                    video_data = get_selected_attributes(video.as_dict)  # Get selected video data
                    file_name = f"{get_create_time(video.as_dict)}.txt"  # File name based on creation time
                    write_to_file(os.path.join(user_directory, file_name), video_data)  # Write data to file

# Function to collect video data by URL
async def collect_videos_by_urls(urls, path=None):
    async with TikTokApi() as api:
        # Create session for TikTok authentication
        await api.create_sessions(ms_tokens=[TOKEN], num_sessions=1, sleep_after=1, headless=False)

        video_directory = os.path.join(path, "videos") if path else "./video"  # Define output directory
        create_directory(video_directory)  # Create directory if it doesn't exist

        with open(urls, 'r') as file:
            for line in file:
                url = line.strip()  # Extract user ID
                video = api.video(url=url)  # Fetch video by URL
                video_info = await video.info()  # Get detailed video information

                video_data = get_selected_attributes(video_info)  # Get selected video data
                file_name = f"{get_create_time(video_info)}.json"  # File name based on creation time
                write_to_json_file(os.path.join(video_directory, file_name), video_data)  # Write data to file

# Function to collect videos by hashtag
async def collect_hashtag_videos(hashtag, path=None):
    async with TikTokApi() as api:
        # Create session for TikTok authentication
        await api.create_sessions(ms_tokens=[TOKEN], num_sessions=1, sleep_after=3, headless=False)

        # Create a main directory to store all users' data
        current_timestamp = get_current_timestamp()
        main_directory = os.path.join(path, rf"Hashtag - {current_timestamp}")
        create_directory(main_directory)  # Ensure the main directory exists

        path = os.path.join(main_directory, hashtag) if path else f"./{hashtag}"  # Define output directory
        create_directory(path)  # Create directory if it doesn't exist

        tag = api.hashtag(name=hashtag)  # Fetch videos by hashtag
        async for video in tag.videos(count=30):  # Iterate over the found videos
            video_data = get_selected_attributes(video.as_dict)  # Get selected video data
            file_name = f"{get_create_time(video.as_dict)}.txt"  # File name based on creation time
            write_to_file(os.path.join(path, file_name), video_data)  # Write data to file

# Function to collect comments from a video
async def collect_video_comments(url, path=None):
    async with TikTokApi() as api:
        # Create session for TikTok authentication
        await api.create_sessions(ms_tokens=[TOKEN], num_sessions=1, sleep_after=3, headless=False)

        video = api.video(url=url)  # Fetch video by URL

        video_directory = os.path.join(path, "video_comments") if path else "./video_comments"  # Define output directory
        create_directory(video_directory)  # Create directory if it doesn't exist

        async for comment in video.comments(count=30):  # Iterate over video comments
            comment_data = get_comment_info(comment)  # Get comment information
            file_name = f"{get_create_time(comment.as_dict)}.txt"  # File name based on creation time
            write_to_file(os.path.join(video_directory, file_name), comment_data)  # Write data to file

# Main function that runs the process based on the specified mode
async def main():
    if MODE == "User":
        await collect_user_videos(USERS, path=OUTPUT_PATH)  # Collect user videos
    elif MODE == "Video":
        await collect_videos_by_urls(URLS, path=OUTPUT_PATH)  # Collect data from a specific video
    elif MODE == "Comments":
        await collect_video_comments(URLS, path=OUTPUT_PATH)  # Collect comments from a video
    elif MODE == "Hashtag":
        await collect_hashtag_videos(HASHTAG, path=OUTPUT_PATH)  # Collect videos by hashtag
    else:
        raise ValueError("Invalid mode in environment variables.")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
