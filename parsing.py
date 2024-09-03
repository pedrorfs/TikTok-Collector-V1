def get_user_nickname(text):
    reference = text.find("isEmbedBanned")
    start = text.find("'nickname':", reference)
    end = text.find("'openFavorite':", reference) - 2
    user_nickname = text[start:end]
    print(user_nickname)
    return user_nickname

def get_user_unique_id(text):
    reference = text.find("stitchSetting")
    start = text.find("'uniqueId':", reference)
    end = text.find("'verified':", reference) - 2
    user_unique_id = text[start:end]
    print(user_unique_id)
    return user_unique_id

def get_signature(text):
    reference = text.find("secUid")
    start = text.find("'signature':", reference)
    end = text.find("'stitchSetting':", reference) - 2
    signature = text[start:end]
    print(signature)
    return signature

def get_verified(text):
    reference = text.find("stitchSetting")
    start = text.find("'verified':", reference)
    end = text.find("'backendSourceEventTracking':", reference) - 3
    verified = text[start:end]
    print(verified)
    return verified

def get_private_account(text):
    reference = text.find("openFavorite")
    start = text.find("'privateAccount':", reference)
    end = text.find("'relation':", reference) - 2
    private_account = text[start:end]
    print(private_account)
    return private_account

def get_user_id(text):
    reference = text.find("'duetSetting':")
    start = text.find("'id':", reference)
    end = text.find("'isADVirtual':", reference) - 2
    user_id = text[start:end]
    print(user_id)
    return user_id

def get_video_create_time(text):
    start = text.find("'createTime':")
    end = text.find(",", start) 
    create_time = text[start:end]
    print(create_time)
    return create_time
    
def get_stats(text):
    reference = text.find("'shareEnabled':")
    start = text.find("'stats':", reference)
    end = text.find("'statsV2':", start) - 2
    stats = text[start:end]
    print(stats)
    return stats

def get_contents(text):
    reference = text.find("'backendSourceEventTracking':")
    start = text.find("'contents':", reference)
    end = text.find("'createTime':", start) - 2
    contents = text[start:end]
    print(contents)
    return contents

def parse_content(file_content):
    get_user_nickname(file_content)
    get_user_unique_id(file_content)
    get_signature(file_content)
    get_verified(file_content)
    get_private_account(file_content)
    get_user_id(file_content)
    get_video_create_time(file_content)
    get_stats(file_content)
    get_contents(file_content)

if __name__ == "__main__":
    with open('video2.txt', 'r', encoding='utf-8') as file:
        file_content = file.read()
    get_user_nickname(file_content)
    get_user_unique_id(file_content)
    get_signature(file_content)
    get_verified(file_content)
    get_private_account(file_content)
    get_user_id(file_content)
    get_video_create_time(file_content)
    get_stats(file_content)
    get_contents(file_content)