from dotenv import dotenv_values
import asyncio
from TikTokApi import TikTokApi
import asyncio
import os
import json

#Get environment variables
enviroment_variables = dotenv_values(".env")
mode = enviroment_variables["MODE"]
users = enviroment_variables["USERS"].split(",")
video = enviroment_variables["VIDEO"]
path = enviroment_variables["OUTPUT_PATH"]
token = enviroment_variables["TOKEN"]
hashtag = enviroment_variables["HASHTAG"]

async def main():
    if mode == "User":
        await collect_user(unique_ids=users, path=path)

    elif mode == "Video":
        await get_video_example()

    elif mode == "Comments":
        await collect_comments(unique_id=user, path=path)

    elif mode == "Hashtag":
        await collect_hashtag_videos(hashtag, path=path)

    elif mode == "Sound":
        await sound_videos()

def get_selected_attibutes(video):
    selected_data = {}
    selected_data["nickname"] = video["author"]["nickname"]
    selected_data["userId"] = video["author"]["id"]
    selected_data["privateAccount"] = video["author"]["privateAccount"]
    selected_data["signature"] = video["author"]["signature"]
    selected_data["uniqueId"] = video["author"]["uniqueId"]
    selected_data["verified"] = video["author"]["verified"]
    selected_data["videoId"] = video["id"]
    selected_data["createTime"] = video["createTime"]
    selected_data["stats"] = video["stats"]
    if "contents" in video.keys():
        selected_data["contents"] = video["contents"]
    if "duration" in video.keys():
        selected_data["duration"] = video["duration"]
    return selected_data

def get_video_create_time(video):
    return video["createTime"] 

def get_comment_create_time(video):
    return video["create_time"] 

def get_comment_info(comment):
    info = {}
    info["text"] = comment.text
    info["likes_count"] = comment.likes_count
    return info 

async def collect_user(unique_ids, path=None):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[token], num_sessions=1, sleep_after=3, headless=False)

        for id in unique_ids:
            try: 
                if path == None:
                    user_directory = rf"./{id}"
                else:
                    user_directory = path + rf"./{id}"
                os.mkdir(user_directory)

                user = api.user(id)           
                async for video in user.videos(count=30):
                    selected_data = get_selected_attibutes(video.as_dict)
                    file_name = get_video_create_time(video.as_dict)
                    with open(f"{user_directory}/{file_name}.txt", "w", encoding='utf-8') as outfile:
                        outfile.write(str(selected_data))
                    # json.dump(selected_data, outfile)

            except RuntimeError:
                with open("./logs.txt", "w", encoding='utf-8') as outfile:
                    outfile.write("error")


async def collect_hashtag_videos(hashtag, path=None):
    if path == None:
        path = rf"./{hashtag}"
    else:
        path = path + rf"./{hashtag}"
    os.mkdir(path)
    
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[token], num_sessions=1, sleep_after=3, headless=False)
        tag = api.hashtag(name=hashtag)

        async for video in tag.videos(count=30):
            selected_data = get_selected_attibutes(video.as_dict)
            file_name = get_video_create_time(video.as_dict)
            with open(f"{path}/{file_name}.txt", "w", encoding='utf-8') as outfile:
                outfile.write(str(selected_data))
                # json.dump(selected_data, outfile)

async def collect_comments(unique_id, path=None):
    if path == None:
        path = rf"./{unique_id}"
    else:
        path = path + rf"./{unique_id}"

    os.mkdir(path)

    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[token], num_sessions=1, sleep_after=3, headless=False)
        user = api.user(unique_id)           

        async for video in user.videos(count=30):
            video_directory = rf"{path}/{video.id}"
            os.mkdir(video_directory)

            async for comment in video.comments(count=30):
                comment_info = get_comment_info(comment)
                file_name = get_comment_create_time(comment.as_dict)
                with open(f"{video_directory}/{file_name}.txt", "w", encoding='utf-8') as outfile:
                    outfile.write(str(comment_info))

async def collect_sound_videos(unique_id, path=None):
    if path == None:
        path = rf"./{unique_id}"
    else:
        path = path + rf"./{unique_id}"

    os.mkdir(path)

    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[token], num_sessions=1, sleep_after=3, headless=False)
        async for sound in api.sound(id=sound_id).videos(count=30):
            print(sound)
            print(sound.as_dict)         

            video_directory = rf"{path}/{video.id}"
            os.mkdir(video_directory)

            async for comment in video.comments(count=30):
                comment_info = get_comment_info(comment)
                file_name = get_comment_create_time(comment.as_dict)
                with open(f"{video_directory}/{file_name}.txt", "w", encoding='utf-8') as outfile:
                    outfile.write(str(comment_info))

                

if __name__ == "__main__":
    asyncio.run(main())











