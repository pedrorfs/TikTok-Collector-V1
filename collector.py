from dotenv import dotenv_values
from user_example import collect_user
from video_example import get_video_example
from sound_example import sound_videos
import asyncio

#Get environment variables
enviroment_variables = dotenv_values(".env")
mode = enviroment_variables["MODE"]
user = enviroment_variables["USER"]
video = enviroment_variables["VIDEO"]

async def main():
    if mode == "User":
        await collect_user(user)

    elif mode == "Video":
        await get_video_example()

    elif mode == "Sound":
        await sound_videos()



if __name__ == "__main__":
    asyncio.run(main())











