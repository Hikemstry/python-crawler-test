import asyncio
import aiohttp
import aiofiles
import re

async def download_video():
    url = "https://mjsky.cc/bfang/5458-1-1.html"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()

        title_match = re.search(r'<h1 class="name nowrap">(?P<title>.*?)</h1>', html, re.S)
        m3u8_match = re.search(r'<script type="text/javascript">.*?"url":"(?P<urll>.*?)",', html, re.S)
        tag_match = re.search(r'"vod_class":".*?"\},"url":"(?P<tag>.*?)index.m3u8",', html)
        
        name = title_match.group("title")
        m3u8_first_url = m3u8_match.group("urll").replace("\\", "")
        tag = re.sub(r"\\", "", tag_match.group("tag"))

        async with session.get(m3u8_first_url) as resp:
            first_m3u8 = await resp.text()
        
        second_m3u8_urls = []
        for line in first_m3u8.strip().splitlines():
            if line.startswith("#"):
                continue
            second_m3u8_urls.append(tag + line)
        
        second_m3u8_url = second_m3u8_urls[0]
        async with session.get(second_m3u8_url) as resp:
            second_m3u8_content = await resp.text()
        
        m3u8_path = f"D:/image/video/{name}.m3u8"
        async with aiofiles.open(m3u8_path, "w") as f:
            await f.write(second_m3u8_content)
 
        tag1 = second_m3u8_url.replace("mixed.m3u8", "")
        
        ts_urls = []
        ts_names = []
        
        for line in second_m3u8_content.strip().splitlines():
            if line.startswith("#"):
                continue
            ts_urls.append(tag1 + line)
            ts_names.append(line)
        
        for i in range(min(3, len(ts_urls))):
            print(f"  {i+1}. {ts_urls[i]}")

        import os
        ts_dir = f"D:/image/video/{name}"
        os.makedirs(ts_dir, exist_ok=True)

        semaphore = asyncio.Semaphore(10)
        
        async def download_ts(index):
            async with semaphore:
                ts_url = ts_urls[index]
                ts_name = ts_names[index]
                ts_path = f"{ts_dir}/{ts_name}"
                
                try:
                    async with session.get(ts_url) as resp:
                        content = await resp.read()
                        async with aiofiles.open(ts_path, "wb") as f:
                            await f.write(content)
                    
                    print(f"下载完成: {index+1}/{len(ts_urls)} - {ts_name}")
                    return True
                except Exception as e:
                    print(f"下载失败: {index+1}/{len(ts_urls)} - {ts_name}: {e}")
                    return False

        tasks = [download_ts(i) for i in range(len(ts_urls))]
        results = await asyncio.gather(*tasks)
        
        success_count = sum(results)
        print(f"TS文件下载完成: {success_count}/{len(ts_urls)} 成功")

        from ffmpegtool import FFmpegTool
        tool = FFmpegTool()
        tool.merge_ts(ts_dir, output_name=f"{name}.mp4", delete_source=True)

if __name__ == "__main__":
    asyncio.run(download_video())