from pyecharts.charts import Pie, Bar, EffectScatter, WordCloud, Page
from pyecharts.components import Table
from pyecharts import options as opts
from pyecharts.globals import *
import pandas as pd  # 存取csv

# 设置分段
bins = [0, 100, 200, 500, 1000, 2000, 5000, 99999999]
# 设置标签
labels = ['0-100', '100-200', '200-500', '500-1k', '1k-2k', '2k-5k', '5k+']

df = pd.read_csv("../data/cmt_info/hot_cmt.csv", usecols=[
    "用户ID",
    "用户昵称",
    "点赞数",
    "回复数",
    "评论内容"
])

# 按分段离散化数据
likes = df["点赞数"]
reply = df["回复数"]
count_list = likes.add(reply)
# print(count_list)
segments = pd.cut(count_list, bins, labels=labels)  # 按分段切割数据
counts = pd.Series(segments).value_counts(sort=False).values.tolist()  # 统计个数


# print(counts)


def like_and_reply_bar():
    # 初始化条形图
    bar = Bar(init_opts=opts.InitOpts(theme=ThemeType.CHALK, width="450px", height="350px", chart_id='bar_cmt2'))
    bar.add_xaxis(labels)  # 增加x轴数据
    bar.add_yaxis("热评数量", counts)  # 增加y轴数据
    bar.set_global_opts(
        legend_opts=opts.LegendOpts(pos_left='right'),
        title_opts=opts.TitleOpts(title="点赞回复数量区间分布-柱形图", pos_left='center'),  # 标题
        toolbox_opts=opts.ToolboxOpts(is_show=False),  # 不显示工具箱
        xaxis_opts=opts.AxisOpts(name="点\n赞\n\n回\n复\n数\n量",  # x轴名称
                                 axislabel_opts=opts.LabelOpts(font_size=8)),  # 字体大小
        yaxis_opts=opts.AxisOpts(name="热评数量",
                                 axislabel_opts={"rotate": 0},
                                 splitline_opts=opts.SplitLineOpts(is_show=True,
                                                                   linestyle_opts=opts.LineStyleOpts(type_='solid')),
                                 ),  # y轴名称
    )
    # 标记最大值
    bar.set_series_opts(
        markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max", name="最大值"), ],
                                          symbol_size=35)  # 标记符号大小
    )
    return bar
    # bar.render("点赞回复数分布-柱形图.html")  # 生成html文件
    # print('生成完毕:点赞回复数分布-柱形图.html')
