import requests
import re
dic={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0"}
url="https://www.dytt8899.com/"

resp=requests.get(url)
resp.encoding="gb2312"
con1=resp.text

obj1=re.compile(r"2026必看热片.*?<ul>(?P<a>.*?)</ul>",re.S)
obj2=re.compile(r"<li><a href='(?P<b>.*?)'",re.S)
obj3=re.compile(r"<br />◎片　　名　(?P<name>.*?)<br />.*?<li><a href=\"jianpian://pathtype=url&path=(?P<download>.*?)\">",re.S)
result1=obj1.finditer(con1)

tar=[]
for i in result1:
    m=i.group("a")
    result2=obj2.finditer(m)
    for j in result2:
        n=url.strip("\"")+j.group("b").strip("/")
        tar.append(n)
for k in tar:
    resp2=requests.get(k)
    resp2.encoding="gb2312"
    con2=resp2.text
    result3=obj3.finditer(con2)
    for l in result3:
        print(l.group("name"))
        print(l.group("download"))
resp.close()
resp2.close()
