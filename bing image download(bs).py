import requests
from bs4 import BeautifulSoup
import time
import random
import re
x=y=1
for i in range(1,9):
    """bing 壁纸网站存在睡眠时间检测,所以加入睡眠时间,目前尽可能小的睡眠时间是1-12秒,可以自行修改。"""
    time.sleep(random.uniform(1,12))
    tag="https://dailybing.com"
    url=f"https://dailybing.com/hot.html?local=zh-cn&page={i}"
    dic={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0"}
    try:
        resp1=requests.get(url,headers=dic,timeout=10)
        resp1.raise_for_status()
    except requests.exceptions.RequestException as e :
        print(f"page{i}fasle!{e}")
        continue
    page1=BeautifulSoup(resp1.text,"html.parser")

    a=page1.find_all("a",attrs={"class":"image-body"})[1:]
    for b in a:
        time.sleep(random.uniform(1,12))
        name=b.find("div",attrs={"class":"image-caption-title"})
        name.text=re.sub(r"[\\/:*?\"<>|]","-",name.text)
        """去除非法字符"""
        c=b.get("href")
        urll=tag+c
        respp=requests.get(urll,headers=dic)
        pagee=BeautifulSoup(respp.text,"html.parser")
        
        d=pagee.find("a",attrs={"title":"4K 3840x2160"})
        """获取到的是4K 3840x2160,具体情况可自行修改。"""
        if d is None:
            print("completed!")
            continue
        e=d.get("href")
        imageurl=tag+e
        image=requests.get(imageurl,headers=dic)
        
        with open(f"D:/image/bing image download(bs)/{name.text}.jpg",mode="wb") as f:
            """保存图片的地址，可自行修改。"""
            f.write(image.content)
        z=(y/192.0)*100
        print(f"page:{x},completed:{y},finished:{z:.2f}%")
        """显示进度"""
        y+=1
        respp.close()
        image.close()
    x+=1
    resp1.close()

