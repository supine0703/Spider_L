import copy
import json
# from datetime import datetime

import pandas as pd
from var import data_path, hot_cmt, all_cmt, hot_cmt_options, all_cmt_options


def get_dir(rid: str):
    import os
    for folder_name in os.listdir(data_path):
        if os.path.isdir(os.path.join(data_path, folder_name)):
            if rid + "_" in folder_name:
                print(f"搜索到目录: {folder_name}")
                return folder_name
    return None


def read_options_info(cmt, options):
    ifo = {}
    for keyword in options:
        value = cmt
        for option in options[keyword]:
            value = value[option]
        ifo[keyword[0]] = value
    return ifo


def load_hot_cmt(rid: str, save_path: str):
    # 从JSON文件中加载数据
    # 加载热评的点赞和评论数量
    path = save_path + "cmt_1.json"
    try:
        with open(path, 'r') as file:
            data = json.load(file)["data"]
            if data["hotComments"] is not None:
                hot_cmt[rid] = []
                for cmt in data["hotComments"]:
                    hot_cmt[rid].append(read_options_info(cmt, hot_cmt_options))
                    # hot_cmt[rid].append({
                    #     "uid": cmt["user"]["userId"],  # id
                    #     "name": cmt["user"]["nickname"],  # 昵称
                    #     "comment": cmt["content"],  # 评论
                    #     "likeCount": cmt["likedCount"],  # 点赞数
                    #     "replyCount": cmt["replyCount"],  # 回复数
                    #     "timeStr": datetime.fromtimestamp(cmt["time"] // 1000),  # 时间字符串
                    # })
                # print(hot_cmt[rid])
            file.close()
            print(f"成功读取热评信息 共: {len(hot_cmt[rid]) if rid in hot_cmt else 0}条")
    except FileNotFoundError:
        print(f"没有找到存储热评信息的文件: {path}")


def load_all_cmt(rid: str, save_path: str, max_page: int = 1):
    # # 加载全部评论
    page = max_page if max_page > 0 else 0
    for n in range(1, max_page + 1):
        path = save_path + f"cmt_{n}.json"
        try:
            with open(path, 'r') as file:
                data = json.load(file)["data"]
                if data["comments"] is not None and len(data["comments"]) > 0:
                    if rid not in all_cmt:
                        all_cmt[rid] = []
                    for cmt in data["comments"]:
                        all_cmt[rid].append(read_options_info(cmt, all_cmt_options))
                        # all_cmt[rid].append({
                        #     "uid": cmt["user"]["userId"],  # id
                        #     "name": cmt["user"]["nickname"],  # 昵称
                        #     "comment": cmt["content"],  # 评论
                        #     "likeCount": cmt["likedCount"],  # 点赞数
                        #     "replyCount": cmt["replyCount"],  # 回复数
                        #     "timeStr": datetime.fromtimestamp(cmt["time"] // 1000),  # 时间字符串
                        # })
                    # print(all_cmt[rid])
                file.close()
                print(f"成功读取第{n}页所有评论信息 {len(data['comments'])}条")
        except FileNotFoundError:
            page = n - 1
            print(f"没有找到存储所有评论信息的文件: {path}")
            break
    print(f"所有评论信息 共: {page}页 {len(all_cmt[rid]) if rid in all_cmt else 0}条")
    #     with open(save_path + f"cmt_{n}.json", 'r') as file:
    #         data = json.load(file)
    #         for cmt in data["data"]["comments"]:
    #             info["cmt"].append({
    #                 cmt["user"]["userId"]: [  # id
    #                     cmt["user"]["nickname"],  # 昵称
    #                     cmt["status"],  # 状态
    #                     cmt["time"],  # 时间戳
    #                     cmt["timeStr"],  # 时间字符串
    #                     cmt["likedCount"],  # 点赞数
    #                     cmt["replyCount"],  # 评论数
    #                     cmt["content"]  # 评论
    #                 ]
    #             })
    # 打印提取的信息
    # print(info)


def save_to_csv(rid: str, save_path: str):
    if rid in hot_cmt:
        df = pd.DataFrame()  # 初始化一个DataFrame对象
        for keyword in hot_cmt_options:
            df[keyword[1]] = [cmt[keyword[0]] for cmt in hot_cmt[rid]]
        # df["用户ID"] = [cmt["uid"] for cmt in hc]
        # df["用户昵称"] = [cmt["name"] for cmt in hc]
        # df["点赞数"] = [cmt["likeCount"] for cmt in hc]
        # df["回复数"] = [cmt["replyCount"] for cmt in hc]
        # df["评论时间"] = [cmt["time"] for cmt in hc]
        # df["评论内容"] = [cmt["comment"] for cmt in hc]
        df.to_csv(save_path + "hot_cmt.csv", encoding='utf_8_sig')  # 将数据保存到csv文件
        print(f"热评信息保存为 '{save_path}hot_cmt.csv'")
    if rid in all_cmt:
        df = pd.DataFrame()  # 初始化一个DataFrame对象
        for keyword in hot_cmt_options:
            df[keyword[1]] = [cmt[keyword[0]] for cmt in all_cmt[rid]]
        df.to_csv(save_path + "all_cmt.csv", encoding='utf_8_sig')  # 将数据保存到csv文件
        print(f"所有评论信息保存为 '{save_path}all_cmt.csv'")


def load_data(rid, read_hot_cmt: bool = True, read_all_cmt: int = 1, to_csv=False) -> bool:
    rid = str(rid)
    print(f"歌曲id: {rid} -正在读取歌曲评论信息: ")
    save_path = copy.deepcopy(data_path)
    dir_name = get_dir(rid)
    if dir_name is None:
        print(f"没有歌曲id: {rid}的歌曲数据")
        return False
    else:
        save_path += f"{dir_name}/"
    if read_hot_cmt:
        load_hot_cmt(rid, save_path)
    load_all_cmt(rid, save_path, read_all_cmt)
    if to_csv is True:
        save_to_csv(rid, save_path)
    print()
    return True


if __name__ == '__main__':
    ...
    # load_data(2112196350, to_csv=True)
