from TikTokApi import TikTokApi
import asyncio
import os
from parsing import parse_content
import json

ms_token = "uNvWzMwAbWc7-XllXm3g0CpaVb-9ADrQvbMyZO7ixe6rAEH-aYCZWsPX45xSUjpZdfqvsmA4mM6WM0jBGbei53KHwegvmdrwSNfirtKq9s_ew693o0sRwg_GoI1EOFFnNIG1lz1MQNjcyw=="  # set your own ms_token, think it might need to have visited a profile

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

async def get_comments(video):
    comments = []
    async for comment in video.comments(count=30):
        if comment is None:
            continue
        comments.append(comment.as_dict)
    return comments

async def collect_user(unique_id, comments=False, path=None):
    if path == None:
        path = rf"./{unique_id}"
    else:
        path = path + rf"./{unique_id}"
    os.mkdir(path)
    
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False)
        user = api.user(unique_id)           

        c = 1
        async for video in user.videos(count=30):
            selected_data = get_selected_attibutes(video.as_dict)
            try:
                if comments:
                    selected_data["comments"] = await get_comments(video)
            finally:
                with open(f"{path}/sample{c}.json", "w") as outfile:
                    json.dump(selected_data, outfile)
                c = c + 1

if __name__ == "__main__":
    asyncio.run(user_example())
