cmt_data_path = "../data/cmt_data/"
cmt_info_path = "../data/cmt_info/"
data_path = "../data/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}  # 定义一个请求头(防止反爬)

infos = {  # rid: info
    "": {  # rid
        "song": "",      # 歌曲名
        "singer": "",    # 歌手
        "album": "",     # 所属专辑
        "dir_name": "",  # 所处文件夹名称
    },
}
hot_cmt = {
    # "": [{  # rid
    #     "uid": "",         # 用户id
    #     "name": "",        # 用户昵称
    #     "comment": "",     # 评论内容
    #     "likeCount": "",   # 点赞数
    #     "replyCount": "",  # 评论数
    # },],
}  # rid: hot cmt
all_cmt = {
    # "": [{  # rid
    #     "uid": "",         # 用户id
    #     "name": "",        # 用户昵称
    #     "comment": "",     # 评论内容
    #     "likeCount": "",   # 点赞数
    #     "replyCount": "",  # 评论数
    # },],
}  # rid: all cmt

# options (xxx_cmt: keyword, df: keyword) : [keywords in json]
# 分别对应为 变量关键字、存储时关键字、cmt.json文件中嵌套的关键字
hot_cmt_options = {  # in file ["data"]["comments"]
    ("uid", "用户id"): ["user", "userId"],
    ("name", "用户昵称"): ["user", "nickname"],
    ("likeCount", "点赞数"): ["likedCount"],
    ("replyCount", "评论数"): ["replyCount"],
    ("time", "时间戳"): ["time"],
    ("comment", "评论内容"): ["content"],
}
all_cmt_options = {  # in file ["data"]["hotComments"]
    ("uid", "用户id"): ["user", "userId"],
    ("name", "用户昵称"): ["user", "nickname"],
    ("likeCount", "点赞数"): ["likedCount"],
    ("replyCount", "评论数"): ["replyCount"],
    ("time", "时间戳"): ["time"],
    ("comment", "评论内容"): ["content"],
}
