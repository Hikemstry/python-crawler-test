import requests
import re
from concurrent.futures import ThreadPoolExecutor

url="https://mjsky.cc/bfang/5458-1-1.html"
"""url为该电影页面的网址"""
dic={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0"}

obj=re.compile(r"<script type=\"text/javascript\">.*?\"url\":\"(?P<urll>.*?)\",",re.S)
obj2=re.compile(r"<h1 class=\"name nowrap\">(?P<title>.*?)</h1>",re.S)
obj3=re.compile(r"\"vod_class\":\".*?\"\},\"url\":\"(?P<tag>.*?)index.m3u8\",")

resp=requests.get(url,headers=dic)

m3u8_first_url_demo=obj.finditer(resp.text)
title=obj2.finditer(resp.text)
"""拿名字"""
tags=obj3.finditer(resp.text)

for k in title:
    name=k.group("title")
for i in m3u8_first_url_demo:
    m3u8d_first_url=i.group("urll").replace("\\","")
    respp=requests.get(m3u8d_first_url,headers=dic)
for j in tags:
    tag=j.group("tag")
    tag=re.sub(r"\\","",tag)
    

for line in respp.text.strip().splitlines():
    if line.startswith("#"):
        continue
    part_second_m3u8=line
    m3u8_second_url=tag+part_second_m3u8
    tag1=m3u8_second_url.strip("mixed.m3u8")
    print(tag1)
    resppp=requests.get(m3u8_second_url,headers=dic)
    resppp_con=resppp.content.decode("utf-8")
    with open(f"D:/image/video/{name}.m3u8",mode="a") as f:
        """电影m3u8保存,可自行修改,但需要与43行地址相同!"""
        f.write(resppp_con)
        
resp.close()
respp.close()

urlll=[]
linedic=[]

p=0

with open(f"D:/image/video/{name}.m3u8",mode="r") as t:
    for line in t:
        line=line.strip()
        if line.startswith("#"):
            continue
        linedic.append(line)
        urlll.append(tag+line) 

for i in urlll:
    print(i)
for j in linedic:
    p+=1
def dl(i):
    resppp=requests.get(urlll[i])
    with open(f"D:/image/video/{name}/{linedic[i]}",mode="wb") as k:
        """电影保存的地方"""
        k.write(resppp.content)
    print(f"{linedic[i]} completed!")
    resppp.close()

with ThreadPoolExecutor(12) as t:
    for j in range(0,p+1,1):
        t.submit(dl,i=j)
print("all ts downloaded!")
print("-----------------------------------------")

"""引用ffmpegtool,源代码来自tool,参考tool.py"""
from tool import FFmpegTool
tool=FFmpegTool()
tool.merge_ts(rf"D:/image/video/{name}", output_name=f"{name}.mp4", delete_source=True)
