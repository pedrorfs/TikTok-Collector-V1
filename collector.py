from dotenv import dotenv_values
import asyncio
from TikTokApi import TikTokApi
import asyncio
import os
import json

#Get environment variables
enviroment_variables = dotenv_values(".env")
mode = enviroment_variables["MODE"]
user = enviroment_variables["USER"]
video = enviroment_variables["VIDEO"]
path = enviroment_variables["OUTPUT_PATH"]
token = enviroment_variables["TOKEN"]

async def main():
    if mode == "User":
        await collect_user(unique_id=user, path=path)

    elif mode == "Video":
        await get_video_example()

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

def get_create_time(video):
    return video["createTime"] 

async def collect_user(unique_id, path=None):
    if path == None:
        path = rf"./{unique_id}"
    else:
        path = path + rf"./{unique_id}"
    os.mkdir(path)
    
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[token], num_sessions=1, sleep_after=3, headless=False)
        user = api.user(unique_id)           

        async for video in user.videos(count=30):
            selected_data = get_selected_attibutes(video.as_dict)
            file_name = get_create_time(video.as_dict)
            with open(f"{path}/{file_name}.txt", "w", encoding='utf-8') as outfile:
                outfile.write(str(selected_data))
                # json.dump(selected_data, outfile)

if __name__ == "__main__":
    asyncio.run(main())











