import requests
import re
from concurrent.futures import ThreadPoolExecutor
dic={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0"}
def targ(i):
    
        url=f"https://book.douban.com/top250?start={i}"
        resp=requests.get(url,headers=dic)

        con=resp.text
        obj=re.compile(r"""<div class="pl2">.*?title=\"(?P<id>.*?)\".*?<p class="pl">(?P<name>.*?)</p>.*?<span class="rating_nums">(?P<rate>.*?)</span>.*?<span class="pl">\((?P<num>.*?)\)</span>""",re.S)
        
        result=obj.finditer(con)

        for i in result:
            print("《",i.group("id"),"》")
            print(i.group("name"))
            print("评分:",i.group("rate"),"(",i.group("num").strip(),")")
        resp.close()

with ThreadPoolExecutor(10) as t:
    for k in range(10):
        t.submit(targ,i=k*25)
