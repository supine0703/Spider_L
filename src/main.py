import json

from save import get_songs_info, save_cmt_json
from load import load_data


def get_y_or_n(s: str = "") -> bool:
    y_or_n = {"y": True, "n": False}
    while True:
        var = input(f"{s}(y/n): ")
        if var == "y" or var == "n":
            return y_or_n[var]


def get_int(s: str = "") -> int:
    while True:
        try:
            return int(input(f"{s}(int): "))
        except ValueError:
            print("输入不是有效的整数")


def main():
    save_path = "default"
    while True:
        print(
            "网易歌曲评论区爬虫程序:",
            "0. 退出",
            "1. 爬取歌曲评论区",
            "2. 读取爬取的内容",
            "3. 设置",
            sep="\n"
        )
        key = input()
        if key == "0":
            break
        elif key == "1":
            rids = input("请输入要爬取的网易歌曲id (多个则使用空格间隔):\n").split()
            # print(rids)
            result = get_songs_info(rids, make_dir=True, clear_dir=False)
            rids = [rids[i] for i in range(len(rids)) if result[i]]
            max_page = input("请输入需要爬取的评论最大页数 (输入 'one by one' 逐个输入): ")
            if max_page == "one by one":
                for rid in rids:
                    max_page = get_int(f"请输入 id:'{rid}' 的歌曲需要爬取的评论最大页数")
                    save_cmt_json(rid, page=max_page)
            else:
                try:
                    max_page = int(max_page)
                except ValueError:
                    print("输入不是有效的整数")
                    max_page = get_int(f"请重新输入需要爬取的评论最大页数")
                save_cmt_json(page=max_page, save_data_path=save_path)
        elif key == "2":
            rid = input("请输入要读取的网易歌曲id: ")
            load_data(rid, to_csv=get_y_or_n("是否保存为.csv"), read_hot_cmt=get_y_or_n("是否读取热评信息"),
                      read_all_cmt=get_int("读取多少页所有评论信息"))
        elif key == "3":
            ...
        else:
            print("无效key")
    print("已退出.")
    # get_songs_info([2112196351, "2112196353"], mk_or_cl=False)
    # save_cmt_json()
    # load_data(2112196350, to_csv=True, read_all_cmt=3)
    # load_data(2112196351, to_csv=True)
    # load_data(2112196353, to_csv=True)


if __name__ == '__main__':
    # get_songs_info([211219], make_dir=False, clear_dir=True)
    # save_cmt_json(page=4)
    # load_data(211219, to_csv=True, read_all_cmt=4)
    main()
    ...
