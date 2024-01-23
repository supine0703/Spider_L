import os
import copy
import json
import requests
from base64 import b64encode
from Crypto.Cipher import AES
from bs4 import BeautifulSoup
from var import data_path, headers, infos


def cl_dir(path: str) -> bool:
    # 判断文件夹是否存在
    if os.path.exists(path):
        # 清空文件夹
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                cl_dir(file_path)  # 递归清空子文件夹
        return True
    return False


def mk_dir(path: str) -> bool:
    if not os.path.exists(path):
        # 创建文件夹
        os.makedirs(path)
        # print(f"路径:'{path}'不存在 已成功创建")
        return True
    return False


def get_song_info(rid, make_dir=True, clear_dir=False) -> bool:
    rid = str(rid)
    flg = False
    res = requests.get(f"https://music.163.com/song?id={rid}", headers=headers)
    # 判断请求是否成功
    if res.status_code != 200:  # 失败
        print("请求失败，状态码：", res.status_code)
    else:  # 成功
        soup = BeautifulSoup(res.text, "html.parser")
        g_top = soup.find(id="g_top")
        # print(g_top)
        if g_top:
            data_module = g_top.get("data-module")
            # print("data-module 的内容是:", data_module)
            if data_module == "404":
                print(f"没有在网易云中找到歌曲 id: {rid} 的歌")
            else:
                if f"{rid}" not in infos:
                    infos[rid] = {}
                info = infos[rid]
                info["song"] = soup.find("em", class_="f-ff2").text
                info_fa = soup.find_all("p", class_="des s-fc4")
                info["singer"] = info_fa[0].find("a").text
                info["album"] = info_fa[1].find("a").text
                dir_name = f"{rid}"
                for key in info:
                    dir_name += f"_{info[key]}"
                info["dir_name"] = dir_name
                dir_path = copy.deepcopy(data_path) + dir_name
                if make_dir:
                    if mk_dir(dir_path):
                        print(f"成功创建目录'{dir_path}'")
                if clear_dir:
                    if cl_dir(dir_path):
                        print(f"目录'{dir_path}'已清空")
                print(f"rid: {rid} 歌曲: {info['song']} 歌手: {info['singer']} 所属专辑: {info['album']}")
                flg = True
        else:
            print("未找到符合条件的 div 元素")
    res.close()
    print()
    return flg


def get_songs_info(rids: list, make_dir=True, clear_dir=False) -> list[bool]:
    return [get_song_info(rid, make_dir=make_dir, clear_dir=clear_dir) for rid in rids]


url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="
# 请求方式POST
d = {
    "rid": "",
    "threadId": "",
    "pageNo": "",
    # "rid": "R_SO_4_2112196350",
    # "threadId": "R_SO_4_2112196350",
    # "pageNo": "1",
    "pageSize": "20",
    "cursor": "-1",  # 需要读取上一页的偏移量传入
    "offset": "0",
    "orderType": "1",
    "csrf_token": ""
}
# 破解出的定值
e = "010001"
f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
g = "0CoJUm6Qyw8W8jud"
i = "NLdIANC1Ejt546nc"  # 16位随机串 强行设为定值
encSecKey = {  # 根据i计算出的密钥 i固定 密钥固定
    "NLdIANC1Ejt546nc": "bf3bd2fba1a9538b6b9ef885d8694f15ba9aba3ba4870cf7bf94a81dd03388bd39baccd4d4dedbdc2a664cf08b09706fb815ffe27c2bdc20b88b9b49e2613a7a18a2c6dfa259485fa714b70ffdf561c9aa5f80035eb87a074a7f3f2a4f9affe67d71094f0d27d4232fff3b987d9a718dea5a23fa1b7965d3d8cd51e577f8ebce"
}


def get_params(data):  # 获取加密后的数据
    def enc_params(dat, key):  # aes加密
        iv = "0102030405060708"
        pad = 16 - len(dat) % 16
        dat += chr(pad) * pad  # 转为可加密的串
        aes = AES.new(key=key.encode("utf-8"), IV=iv.encode("utf-8"), mode=AES.MODE_CBC)
        bs = aes.encrypt(dat.encode("utf-8"))
        return str(b64encode(bs), "utf-8")

    first = enc_params(data, g)
    second = enc_params(first, i)
    return second


def save_cmt_json(rid: str = "", page: int = 1, save_data_path=data_path):
    if rid == "":
        for n_rid in infos:
            if n_rid != "":
                save_cmt_json(rid=n_rid, page=page)
        return
    if rid not in infos:
        print(f"需要先获取 id: {rid} 的歌曲的基本信息 可以尝试先调用 'get_song_info(rid)'")
        return
    d["rid"] = f"R_SO_4_{rid}"
    d["threadId"] = f"R_SO_4_{rid}"
    if save_data_path == "default":
        save_data_path = copy.deepcopy(data_path)
    save_path = save_data_path + infos[rid]["dir_name"] + "/"
    print(f"歌曲id: {rid} -正在保存爬取的信息: ")
    if os.path.exists(save_path) and os.path.isdir(save_path):
        pg = page
        num = None
        for n in range(1, page + 1):
            d["pageNo"] = f"{n}"
            res = requests.post(url, data={
                "params": get_params(json.dumps(d)),
                "encSecKey": encSecKey[i]
            })
            # 将响应数据转换为JSON格式
            json_data = res.json()
            # print(json_data)
            res.close()
            # 将JSON数据保存到文件中
            fs = save_path + f"cmt_{n}.json"
            with open(fs, 'w') as file:
                json.dump(json_data, file)
            print(f"成功爬取第{n}页评论 保存为 '{fs}'")
            d["cursor"] = json_data["data"]["cursor"]
            if n == 1:
                num = json_data["data"]["totalCount"]
            if 20 * n >= json_data["data"]["totalCount"]:
                pg = n
                break
        print(f"已经爬取完毕所有评论 共: {pg}页 {num}条")
    else:
        print(f"目录: '{save_path}' 不存在")
    print()


if __name__ == '__main__':
    ...
    # get_songs_info(["2112196350", "123", "21121963"])
    # save_cmt_json("2112196350")

"""
    # 加密过程:
    function a(a) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {
        var h = {}
          , i = a(16);
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),  # 返回 params
        h.encSecKey = c(i, e, f),  # 返回 encSecKey
        h
    }
"""
