import requests
import re
from concurrent.futures import ThreadPoolExecutor
from tool import FFmpegTool
import os
"""目前可以下载电视剧一个季的所有内容，至于所有季自动下载...(懒。。。)"""
for page in range(1,14,1):
    
    """episode_dir = rf"D:/image/video/纸牌屋/第二季第{page}集"
    os.makedirs(episode_dir, exist_ok=True)"""
    """可以用来创建相应文件夹保存相应的电视剧"""
    episode_dir="D:/image/video/纸牌屋/"
    
    """文件夹可以自行创建并添加到episode_dir中,为电视剧保存的地方"""
    url=f"https://mjsky.cc/bfang/48750-1-{page}.html"
    """对应网站第一集的url"""
    resp1=requests.get(url)

    obj1=re.compile(r",\"vod_class\":\".*?\"\},\"url\":\"(?P<first_m3u8>.*?)\",\"url_next\":\".*?\",")
    obj2=re.compile(r"<h1 class=\"name nowrap\">(?P<name>.*?)</h1>")

    a=obj1.finditer(resp1.text)
    b=obj2.finditer(resp1.text)
    for k in b:
        name=k.group("name")
    for i in a:
        first_m3u8=i.group("first_m3u8")
        first_m3u8=re.sub(r"\\","",first_m3u8)
        tag1=first_m3u8.split("index.m3u8")[0]     
            
    resp2=requests.get(first_m3u8)
            
    lines=resp2.text.strip().splitlines()
    for j in lines:
        if j.startswith("#"):
            continue
        else:
            part_second_m3u8=j
            
    second_m3u8=tag1+part_second_m3u8
    tag2=second_m3u8.split("mixed.m3u8")[0]
    resp3=requests.get(second_m3u8)
            
    resp1.close()
    resp2.close()
            
    linedic=[]
    urldic=[]
    count=0
            
    with open(f"D:/image/video/{name}.m3u8",mode="wb") as f:
        """"m3u8文件保存,与54行地址一致,可自行修改"""
        f.write(resp3.content)
    with open(f"D:/image/video/{name}.m3u8",mode="r") as t:
        for line in t:
            line=line.strip()
            if line.startswith("#"):
                continue
            else:
                linedic.append(line)
                urldic.append(tag2+line)
                        
                count+=1
                        
    resp3.close() 
                  
    def dl(i):
        resp4=requests.get(urldic[i])
            
        with open(f"{episode_dir}/{linedic[i]}",mode="wb") as k:
            k.write(resp4.content)
        print(f"{name} {linedic[i]} completed!")
            
        resp4.close()   
                 
    with ThreadPoolExecutor(10) as h: 
        for m in range(0,count+1,1):
            h.submit(dl,i=m)  
        
    print(f"{name} all ts downloaded! ")
    print("----------------------------------")
    """引用ffmpegtool,源代码来自tool,参考tool.py"""
    tool=FFmpegTool()
    tool.merge_ts(rf"{episode_dir}", output_name=f"{name}.mp4", delete_source=True)   
    
    
    
   
