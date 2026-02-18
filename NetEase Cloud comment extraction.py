import requests
from Crypto.Cipher import AES
from base64 import b64encode
import json

def pad(s, bs=16):
    pad_size = bs - len(s) % bs
    return s + bytes([pad_size] * pad_size)

def get_params(data):

    first = aes_encrypt(data, g)
    second = aes_encrypt(first, i)
    return second
    
def aes_encrypt(data, key):
    iv = "0102030405060708"
    
    if isinstance(data, dict):
        data = json.dumps(data)
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    aes = AES.new(
        key=key.encode("utf-8"),
        iv=iv.encode("utf-8"),
        mode=AES.MODE_CBC
    )
    padded_data = pad(data)
    encrypted = aes.encrypt(padded_data)
    return b64encode(encrypted).decode('utf-8')

def get_encSecKey():
        return "615bd4fc7e8194d7cc9a79a2fbc2520128e64faa9155ff775cb45a59386e360c8b3111699bdc73ffa2d5001886b08484d3d67a0230a8125950233e06028fe7eea138534fe8daa396bfc2d02601ad45fc1de6915f2b4566b7f818d6da92d508b88838cf7d21255c406db229dc9dd84f4c4ab25b7b791cbe173f488c31dfd933ff"
    
e = "010001"
f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
g = "0CoJUm6Qyw8W8jud"
i = "Cze1O0OVnyI102sB"
x=y=1
cursor=-1
for page in range(1,11,1):
    """获取评论的页数"""
    data = {
            "csrf_token": "ae11f2c6709b55bde4de7d71cd952940",
            "cursor": f"{cursor}",
            "offset": "0",  
            "orderType": "2",
            "pageNo": "1",  
            "pageSize": "20",  
            "rid": "R_SO_4_185904", 
            "threadId": "R_SO_4_185904" 
            """rid和threadId是对应歌手的,可以通过搜索歌手获取"""
        }
    url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="
    resp = requests.post(url, data={"params": get_params(data),
                                        "encSecKey": get_encSecKey()
        })
    dic=json.loads(resp.text)
    cursor=dic.get("data").get("cursor")
    dic=dic.get("data").get("comments")
    for j in dic:
        id=[]
        time=[]
        like=[]
        con=[]
        id.append(j["user"]["nickname"])
        time.append(j["timeStr"])
        like.append(j["likedCount"])
        con.append(j["content"])
        
        print(f"{id[0]}({time[0]} like:{like[0]} page:{x} count:{y}):\n{con[0]}\n")
        y+=1
    x+=1

        
        
    