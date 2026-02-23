from playwright.sync_api import sync_playwright
import requests
import re

""" Select Soap to Download """
tag="https://vv.jisuzyv.com"
headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0",
            "referer":"https://www.shankubf.com/"}

for t in range(6, 31):
    url=f"https://www.yinghuadongman.com.cn/v/45094-1-{t}/"

    resp1=requests.get(url)

    obj1=re.compile(r",\"link_next\":\".*?\",\"link_pre\":\".*?\",\"url\":\"(?P<m3u8_first>.*?)\",",re.S)
    obj2=re.compile(r"<title>(?P<name>.*?)</title>",re.S)

    result1=obj1.finditer(resp1.text)
    result2=obj2.finditer(resp1.text)

    for i in result1:
        m3u8_first_url=i.group("m3u8_first")
        m3u8_first_url=re.sub(r"\\","",m3u8_first_url)
    for j in result2:
        name=j.group("name")
        name=re.sub(r"[\/:*?\"<>|]","",name)

    resp2=requests.get(m3u8_first_url,verify=False)
    for line in resp2.text.splitlines():
        if line.startswith("#"):
            continue
        part_second_m3u8=line

    m3u8_second_url=tag+part_second_m3u8  

    enc_key=m3u8_second_url.strip("index.m3u8")+"enc.key"
    print(f"Automatically Generated ENC.KEY_URL:\n{enc_key}")

    from download_hls import HLS_Downloader
    t=HLS_Downloader()
    t.getinfo(M3U8_URL=m3u8_second_url,VIDEO_NAME=name,HEADERS=headers)
    t.run(max_workers=15,manual_key_url_output=enc_key)
