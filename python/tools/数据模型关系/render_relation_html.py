#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : 邓军
# @time    : 2023/10/14 17:58
# @function: 读取数据库中的数据，生成html
# @version : V1.0.0

from collections import Counter

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Graph

categories, nodes, links = [], [], []

# 读取Excel文件，注意是data目录中的文件，不是模板文件
df = pd.read_excel("data/data_relations.xlsx", '模型关联关系').fillna('', inplace=False)

# 将表头字段作为字典的key，每行的值作为字典的值，每行转换为字典，所有内容存放到列表中
df_dict = []
for item in df.values:
    data_dict = {}
    i = 0
    while i < len(item):
        # 将key最为字典的key，每行的值作为字典的值
        data_dict[df.keys()[i]] = item[i]
        i += 1
    df_dict.append(data_dict)

table_schemas = []
table_names = {}
table_relations = {}
table_statics = []

# 循环数据转换为pyecharts所需的数据
for item in df_dict:

    table_name = item["模型名称"]
    table_schema = table_name.split(".")[0]
    if table_schema not in table_schemas:
        table_schemas.append(table_schema)

    table_names[table_name] = item["模型描述"]

    # 添加节点关系
    if len(item["关联模型"]) > 0:
        # 有关联关系，则将表计入统计
        table_statics.append(table_name)
        table_statics.append(item["关联模型"])
        links.append(opts.GraphLink(source=table_name,
                                    target=item["关联模型"],
                                    emphasis_linestyle_opts=opts.LineStyleOpts(is_show=False),
                                    emphasis_label_opts=opts.LabelOpts(formatter=item["关联关系"])))

# 添加节点信息
# 使用Counter计算被关联表的出现次数,作为节点的权重
counter = Counter(table_statics)
for table_name, table_desc in table_names.items():
    tooltip_opts = opts.TooltipOpts(formatter=table_desc + " : {b} ({c})")
    nodes.append(opts.GraphNode(name=table_name,
                                category=table_schemas.index(table_name.split(".")[0]),
                                value=str(counter[table_name]),
                                symbol_size=counter[table_name],
                                tooltip_opts=tooltip_opts))

# 添加节点分组信息
[categories.append(opts.GraphCategory(name=table_schema)) for table_schema in table_schemas]

chart = (
    Graph(init_opts=opts.InitOpts(width="1366px", height="768px"))
    .add(
        "",
        nodes=nodes,
        links=links,
        categories=categories,
        layout="circular",
        is_rotate_label=True,
        linestyle_opts=opts.LineStyleOpts(color="source", curve=0.3),
        label_opts=opts.LabelOpts(position="right", is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="数据模型关联关系"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%"),
    )
    .render("data/data_relations.html")

)
