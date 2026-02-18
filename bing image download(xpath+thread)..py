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
        c=b.xpath("./a/@href")
        durl=tag+c[0]
        respp=requests.get(durl,headers=dic)
        dhtml=etree.HTML(respp.text)
        dlhtml=dhtml.xpath("/html/body/div[3]/div[1]/div[2]/div/div[1]/div/a[3]/@href")
        dlhtmll=tag+dlhtml[0]
        imageresp=requests.get(dlhtmll,headers=dic)
                                        
        with open(f"D:/image/bing image download(xpath+thread)/{name[0]}.jpg",mode="wb") as f:
            f.write(imageresp.content)
            print(f"page:{aa},completed:{y},finished:{z:.2f}%")
            y+=1

with ThreadPoolExecutor(72) as t:
    for i in range(1,73):
        t.submit(targ,aa=i)
      







