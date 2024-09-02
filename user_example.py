from TikTokApi import TikTokApi
import asyncio
import os

ms_token = "yGg8FqnOOg4MwQDX4XiymRWsoPtu7UGd_Gi2XUeEK8gGh5uOPQ3DplyIK9cJCgQJu5RdClqU48a7ztDw-G275vcDHy7pholCyK5jD2zHvnSnqlipU0djq-tAZAcT-D8JQieEzDvUncwtwA==" # set your own ms_token, think it might need to have visited a profile


async def user_example():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False)
        user = api.user("therock")
        # user_data = await user.info()
        # print(user_data)
        c = 1
        async for video in user.videos(count=30):
            with open(f"video{c}.txt", "w", encoding="utf-8") as file:
                file.write(str(video.as_dict))
            c = c + 1

        # async for playlist in user.playlists():
        #     print(playlist)


if __name__ == "__main__":
    asyncio.run(user_example())
