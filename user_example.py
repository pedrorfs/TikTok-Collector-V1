from TikTokApi import TikTokApi
import asyncio
import os
from parsing import parse_content
import json

ms_token = "uNvWzMwAbWc7-XllXm3g0CpaVb-9ADrQvbMyZO7ixe6rAEH-aYCZWsPX45xSUjpZdfqvsmA4mM6WM0jBGbei53KHwegvmdrwSNfirtKq9s_ew693o0sRwg_GoI1EOFFnNIG1lz1MQNjcyw=="  # set your own ms_token, think it might need to have visited a profile


async def collect_user(unique_id):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False)
        user = api.user(unique_id)
        # user_data = await user.info()
        # print(user_data)

        async for video in user.videos(count=30):
            with open("sample.json", "w") as outfile: 
                json.dump(video.as_dict, outfile)
            # print(video)
            # print(video.as_dict["stats"])
            # parse_content(str(video.as_dict))
            # print(video.as_dict)


        # async for playlist in user.playlists():
        #     print(playlist)


if __name__ == "__main__":
    asyncio.run(user_example())
