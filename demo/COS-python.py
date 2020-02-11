# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/9 15:19

# APPID 已在配置中移除,请在参数 Bucket 中带上 APPID。Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = 'AKIDyqhLlwnd9UvBnBFI9nEJDuMYYN0Of11l'      # 替换为用户的 secretId
secret_key = 'g8M1S7Wlkl5D6PUNlupUvBPPAk5B3h6O'      # 替换为用户的 secretKey
region = 'ap-beijing'     # 替换为用户的 Region
token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)
# 参照下文的描述。或者参照 Demo 程序，详见 https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py

#创建存储桶
# response = client.create_bucket(
#     Bucket='examplebucket-1300594020'
# )
# print(response)

#查看同列表
response = client.list_buckets(
)
print(response)


"""
#文件流简单上传(不支持超过5G的文件,推荐使用下方高级上传接口)
# 强烈建议您以二进制模式(binary mode)打开文件,否则可能会导致错误
with open('公众号.png', 'rb') as fp:
    response = client.put_object(
        Bucket='examplebucket-1300594020',
        Body=fp,
        Key='picture.jpg',
        StorageClass='STANDARD',
        EnableMD5=False
    )
print(response['ETag'])
"""
"""
#### 字节流简单上传
response = client.put_object(
    Bucket='examplebucket-1300594020',
    Body=b'bytes12',
    Key='789.text',
    EnableMD5=False
)
print(response['ETag'])
"""

"""
#### chunk 简单上传
import requests
stream = requests.get('https://cloud.tencent.com/document/product/436/7778')

# 网络流将以 Transfer-Encoding:chunked 的方式传输到 COS
response = client.put_object(
    Bucket='examplebucket-1300594020',
    Body=stream,
    Key='picture.jpg'
)
print(response['ETag'])
"""

#### 高级上传接口（推荐）
# 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
response = client.upload_file(
    Bucket='examplebucket-1300594020',
    LocalFilePath='local.txt',
    Key='xxx.txt',
    PartSize=1,
    MAXThread=10,
    EnableMD5=False
)
print(response['ETag'])


# 查询对象列表
response = client.list_objects(
    Bucket='examplebucket-1300594020',
    Prefix='picture1.txt'
)

print(response)


"""
#单次调用list_objects接口一次只能查询1000个对象，如需要查询所有的对象，则需要循环调用。

marker = ""
while True:
    response = client.list_objects(
        Bucket='examplebucket-1300594020',
        Prefix='folder1', #文件名
        Marker=marker
    )
    print(response['Contents'])
    if response['IsTruncated'] == 'false':
        break
    marker = response['NextMarker']

"""
"""
####  下载文件到本地
response = client.get_object(
    Bucket='examplebucket-1300594020',
    Key='picture.jpg',
)
response['Body'].get_stream_to_file('output.txt')
"""
"""
#### 获取文件流
response = client.get_object(
    Bucket='examplebucket-1300594020',
    Key='picture.jpg',
)
fp = response['Body'].get_raw_stream()
print(fp.read(20))
"""
"""
#### 设置 Response HTTP 头部
response = client.get_object(
    Bucket='examplebucket-1300594020',
    Key='picture.jpg',
    ResponseContentType='text/html; charset=utf-8'
)
print(response['Content-Type'])
fp = response['Body'].get_raw_stream()
print(fp.read(2))
"""
"""
#### 指定下载范围
response = client.get_object(
    Bucket='examplebucket-1300594020',
    Key='picture.jpg',
    Range='bytes=0-10'
)
fp = response['Body'].get_raw_stream()
print(fp.read())
"""
"""
# 删除object
## deleteObject
response = client.delete_object(
    Bucket='examplebucket-1300594020',
    Key='picture.jpg'
)
"""
"""
# 删除多个object
## deleteObjects
response = client.delete_objects(
    Bucket='examplebucket-1300594020',
    Delete={
        'Object': [
            {
                'Key': 'exampleobject1',
            },
            {
                'Key': 'exampleobject2',
            },
        ],
        'Quiet': 'true'|'false'
    }
)

"""