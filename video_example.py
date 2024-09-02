from TikTokApi import TikTokApi
import asyncio
import os
import time
from dotenv import dotenv_values

ms_token = "5nH4ToerIsmKoHCHqrlK2PDVNTF3st1txyroV3ERv_pc9nAOgW_0xb1HiQaaMAAY05uWiOaEglrrbhRHA-q9ZrBsMpP5zpXTIH25dvgUg1ZCO7ZEwPnTOhPAU_kES8Upde9GFlmcRZVXiA=="  # set your own ms_token, think it might need to have visited a profile

env_variables = dotenv_values(".env")
async def get_video_example():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False)
        video = api.video(
            url=env_variables["VIDEO"]
        )

        c = 0
        wait_mark = 500
        number_of_comments = int(env_variables["NUMBER_OF_COMMENTS"])
        print(">>>>>> ",type(number_of_comments))
        async for comment in video.comments(count=number_of_comments):
            with open(f"./comments/comment{c}.txt", "w", encoding="utf-8") as file:
                file.write(str(comment.as_dict))
                # if c == wait_mark:
                #     time.sleep(100)
                #     wait_mark = wait_mark + 500
            c = c + 1

        # async for related_video in video.related_videos(count=10):
        #     print(related_video)
        #     print(related_video.as_dict)

        # video_info = await video.info()  # is HTML request, so avoid using this too much
        # print(video_info)
        # video_bytes = await video.bytes()
        # with open("video.mp4", "wb") as f:
        #     f.write(video_bytes)


if __name__ == "__main__":
    asyncio.run(get_video_example())
