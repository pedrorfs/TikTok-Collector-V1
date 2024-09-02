from TikTokApi import TikTokApi
import asyncio
import os
import time

video_id = 7397552362706980101
ms_token = os.environ.get("ms_token", None)  # set your own ms_token


async def get_comments():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False)
        video = api.video(id=video_id)
        c = 0
        wait_mark = 500
        async for comment in video.comments(count=30):
            with open(f"comment{c}.txt", "w", encoding="utf-8") as file:
                file.write(str(comment.as_dict))
                
            c = c + 1


if __name__ == "__main__":
    asyncio.run(get_comments())
