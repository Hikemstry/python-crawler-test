from lxml import etree
import asyncio
import aiohttp
import aiofiles
import random
import re
"""目前睡眠监测在asyncio中无法找到有效解决方案"""
tag="https://dailybing.com"
dic={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0"}

async def dl(i): 
        url=f"https://dailybing.com/wall.html?local=zh-cn&page={i}"
        
        
        async with aiohttp.ClientSession(headers=dic,) as session:
            async with session.get(url, headers=dic) as resp:
                    
                resptext = await resp.text()
                html = etree.HTML(resptext)
                a = html.xpath("/html/body/div[3]/div[2]/div[2]/div")   
                                                                                                
                for b in a:                                
                                name=b.xpath("./a/div[2]/div[1]/text()")                             
                                c=b.xpath("./a/@href")
                                durl=tag+c[0]
                                name[0]=re.sub(r"[\\/:*?\"<>|]","-",name[0])
                                """去除非法字符"""
                                
                                async with session.get(durl,headers=dic) as respp:
                                                
                                                respptext=await respp.text()
                                                dhtml=etree.HTML(respptext)
                                                dlhtml=dhtml.xpath("/html/body/div[3]/div[1]/div[2]/div/div[1]/div/a[3]/@href")
                                                """获取到的是4K 3840x2160,具体情况可自行修改。"""
                                                dlhtmll=tag+dlhtml[0]
                                                
                                                async with session.get(dlhtmll,headers=dic) as imageresp:

                                                                async with aiofiles.open(f"D:/image/bing image download(xpath+async)/{name[0]}.jpg",mode="wb") as f:
                                                                        """保存图片的地址，可自行修改。"""
                                                                        imagerespcontent=await imageresp.read()
                                                                        await f.write(imagerespcontent)
                                                                        print(f"completed:{name[0]}")
                                                                        
                                                
async def go():
        tasks=[]
        for i in range(1,73,1):
                task=asyncio.create_task(dl(i))
                tasks.append(task)
        await asyncio.gather(*tasks)
        
if __name__=='__main__':
        asyncio.run(go())
        
                
        
        
        
                                               
        

