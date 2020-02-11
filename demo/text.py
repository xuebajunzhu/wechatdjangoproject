# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/15 16:27

parant_list = [
    {
        "id": 1,
        "content": "1",
        "user__nickname": "wupeiqi",
        "user__avatar": "aads",
        "create_date": "2020-01-15T07:46:35.113307Z"
    },
    {
        "id": 6,
        "content": "2",
        "user__nickname": "大卫-1",
        "user__avatar": "https://mini-1251317460.cos.ap-chengdu.myqcloud.com/08a9daei1578736867828.png",
        "create_date": "2020-01-15T07:46:35.527296Z"
    },
    {
        "id": 7,
        "content": "3",
        "user__nickname": "大卫-2",
        "user__avatar": "https://mini-1251317460.cos.ap-chengdu.myqcloud.com/08a9daei1578736867828.png",
        "create_date": "2020-01-15T07:46:35.618243Z"
    }

]

node_list = [
    {
        "id": 5,
        "content": "1-2",
        "user__nickname": "大卫-6",
        "user__avatar": "https://mini-1251317460.cos.ap-chengdu.myqcloud.com/08a9daei1578736867828.png",
        "create_date": "2020-01-15T07:46:35.434290Z",
        "reply_id": 1,
        "reply__user__nickname": "wupeiqi"
    },
    {
        "id": 8,
        "content": "2-1",
        "user__nickname": "大卫-2",
        "user__avatar": "https://mini-1251317460.cos.ap-chengdu.myqcloud.com/08a9daei1578736867828.png",
        "create_date": "2020-01-15T07:46:35.618243Z",
        "reply_id": 6,
        "reply__user__nickname": "大卫-1"
    }
]

parant_dict = {i["id"]:i for i in parant_list}

for key in node_list:
    parant_dict[key["reply_id"]].setdefault("child",[]).append(key)

print(parant_dict)
