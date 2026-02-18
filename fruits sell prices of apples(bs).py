import requests
from bs4 import BeautifulSoup
import time
import random

x=1
for i in range(1,10,1):
    time.sleep(random.uniform(1,8))
    
    url=f"https://www.cnhnb.com/hangqing/cdlist-2001636-0-0-0-0-{i}/"
    dic={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0",
         "Cookie":"deviceId=f64ea19-9a5c-49d8-9e6f-c89402d08; Hm_lvt_0e023fed85d2150e7d419b5b1f2e7c0f=1770166614; Hm_lvt_a6458082fb548e5ca7ff77d177d2d88d=1770166617; sessionId=S_0MLA54RVL0E0D59X; Hm_lvt_b99541cbfb0edd202bb49abf3a0bef84=1770166164,1770337338; HMACCOUNT=C801FCB48DA5C9ED; Hm_lvt_91cf34f62b9bedb16460ca36cf192f4c=1770166164,1770337338; _c_WBKFRo=zuh6j5iBePmKHrUrYaijyVqOamyuc2w8DrsVjLNL; _nb_ioWEgULi=; Hm_lvt_81fc10bb72f85b5a9ff93042925f6543=1770338228; Hm_lpvt_81fc10bb72f85b5a9ff93042925f6543=1770338228; Hm_lpvt_b99541cbfb0edd202bb49abf3a0bef84=1770341731; Hm_lpvt_91cf34f62b9bedb16460ca36cf192f4c=1770341733"}
    resp=requests.get(url,headers=dic)
    page=BeautifulSoup(resp.text,"html.parser")

    a=page.find_all("li",attrs={"class":"market-list-item"})
    for b in a:
        c=b.find_all("span")
        time1=c[0].text
        pro=c[1].text
        place=c[2].text
        price=c[3].text
        print(f"{time1}\t{pro:10}\t{place}\t{price}\t" )
    print(f"page:{x}") 
    x+=1                                                
