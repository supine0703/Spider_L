# 目录
- [目录](#目录)
- [Web Spider.](#web-spider)
  - [爬取网易云音乐的评论以及评论的用户信息：](#爬取网易云音乐的评论以及评论的用户信息)
- [环境](#环境)
- [TODO](#todo)

# Web Spider.
## 爬取网易云音乐的评论以及评论的用户信息：
- 通过直接请求（get）rid，获取有音乐基本信息（歌名、作者、所属专辑），判断歌曲 rid 是否存在
- 模拟网易云音乐的数据加密过程通过XHR对服务器请求数据保存为.json
- 可以通过提取json文件汇总信息，可自行设置需要提取的内容（如：用户详细信息、用户设备信息、用户网易账号基本信息、评论以及回复相关内容等）



# 环境
- python 3.11.5
- beautifulsoup4 4.12.2
- pandas 2.1.4
- pycryptodome 3.15.0
- pyecharts 2.0.4
- requests 2.31.0


# TODO
- 网易音乐评论区的爬虫 还有很多要做的，陆陆续续做吧，比如数据分析，比如更友好的交互，比如更丰富的设置等。
- 之后也可能会写一些其他爬虫
