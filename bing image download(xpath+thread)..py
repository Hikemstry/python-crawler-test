import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import time
import random
import re

tag="https://dailybing.com"
dic={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0"}
def targ(aa):
    y=1 
    """bing 壁纸网站该方法目前尽可能小的睡眠时间是1-20秒,可以自行修改。"""
    time.sleep(random.uniform(0,20))
    
    url=f"https://dailybing.com/wall.html?local=zh-cn&page={aa}"
    resp=requests.get(url,headers=dic)
    html=etree.HTML(resp.text)
    a=html.xpath("/html/body/div[3]/div[2]/div[2]/div")
                                                                                            
    for b in a: 
        z=(y/24.0)*100
        time.sleep(random.uniform(0,20))
                                        
        name=b.xpath("./a/div[2]/div[1]/text()")  
        name[0]=re.sub(r"[\\/:*?\"<>|]","-",name[0])
        """去除非法字符"""                          
        c=b.xpath("./a/@href")
        durl=tag+c[0]
        respp=requests.get(durl,headers=dic)
        dhtml=etree.HTML(respp.text)
        dlhtml=dhtml.xpath("/html/body/div[3]/div[1]/div[2]/div/div[1]/div/a[3]/@href")
        """获取到的是4K 3840x2160,具体情况可自行修改。"""
        dlhtmll=tag+dlhtml[0]
        imageresp=requests.get(dlhtmll,headers=dic)
                                        
        with open(f"D:/image/bing image download(xpath+thread)/{name[0]}.jpg",mode="wb") as f:
            f.write(imageresp.content)
            """保存图片的地址，可自行修改。"""
            print(f"page:{aa},completed:{y},finished:{z:.2f}%")
            y+=1

with ThreadPoolExecutor(15) as t:
    for i in range(1,73):
        t.submit(targ,aa=i)
    """线程数量可自行修改,但请勿超过你的电脑线程数。推荐10到15。"""







