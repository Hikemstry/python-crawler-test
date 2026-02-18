import requests
from lxml import etree

url="https://www.cnhnb.com/hangqing/cdlist-2001636-0-0-0-0-6"

resp=requests.get(url,headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0",
                              "Cookie":"deviceId=f64ea19-9a5c-49d8-9e6f-c89402d08; Hm_lvt_0e023fed85d2150e7d419b5b1f2e7c0f=1770166614; Hm_lvt_a6458082fb548e5ca7ff77d177d2d88d=1770166617; sessionId=S_0MLA54RVL0E0D59X; Hm_lvt_b99541cbfb0edd202bb49abf3a0bef84=1770166164,1770337338; HMACCOUNT=C801FCB48DA5C9ED; Hm_lvt_91cf34f62b9bedb16460ca36cf192f4c=1770166164,1770337338; _c_WBKFRo=zuh6j5iBePmKHrUrYaijyVqOamyuc2w8DrsVjLNL; _nb_ioWEgULi=; Hm_lvt_81fc10bb72f85b5a9ff93042925f6543=1770338228; Hm_lpvt_81fc10bb72f85b5a9ff93042925f6543=1770343591; Hm_lpvt_b99541cbfb0edd202bb49abf3a0bef84=1770344079; Hm_lpvt_91cf34f62b9bedb16460ca36cf192f4c=1770344081; hnUserTicket=bfc9bcd6-370a-4cb7-8220-c9e9153973f4; hnUserId=745538317"  })
html=etree.HTML(resp.text)
a=html.xpath("/html/body/div[1]/div/div/div/div[2]/div[1]/div[4]/div/div[1]/div[1]/div[1]/div[2]/ul/li")
for b in a:
    time=b.xpath("./a/span[1]/text()")
    pro=b.xpath("./a/span[2]/text()")
    lk=b.xpath("./a/span[3]/text()")
    price=b.xpath("./a/span[4]/text()")
    print(f"{time[0]}\t{pro[0]}\t{lk[0]}\t{price[0]}")
    
