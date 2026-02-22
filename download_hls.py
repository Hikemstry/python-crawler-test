# -*- coding: utf-8 -*-
"""
HLS 下载解密主脚本（支持手动输入密钥 URL,自动重试,TS头验证,处理路径空格,合并后删除选项）
"""

import os
import time
import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor
from hls_decryptor import HLSDecryptor

# 禁用不安全请求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class HLS_Downloader:
        
    def getinfo(self,M3U8_URL,VIDEO_NAME,HEADERS):
        self.M3U8_URL = M3U8_URL
        self.VIDEO_NAME = VIDEO_NAME 
        self.WORK_DIR = f"D:/image/video/EVA/{VIDEO_NAME}" 
        self.TS_DIR = os.path.join(self.WORK_DIR, "ts")    
        os.makedirs(self.TS_DIR, exist_ok=True)
        self.HEADERS = HEADERS
        
    def download_and_decrypt(self,i, decryptor, headers, ts_dir):
        seg_url = decryptor.segments[i]
        max_retries = 3
        for attempt in range(max_retries):
            try:
                resp = requests.get(seg_url, headers=headers, timeout=10, verify=False)
                resp.raise_for_status()
                encrypted_data = resp.content
                resp.close()

                if decryptor.method == 'AES-128':
                    decrypted_data = decryptor.decrypt_segment(encrypted_data, segment_index=i)
                else:
                    decrypted_data = encrypted_data

                out_path = os.path.join(ts_dir, f"segment_{i:05d}.ts")
                with open(out_path, 'wb') as f:
                    f.write(decrypted_data)

                # 验证TS头（应为0x47）
                if len(decrypted_data) >= 4:
                    if decrypted_data[0] == 0x47:
                        print(f"[{i+1}/{len(decryptor.segments)}]-TS头正确(0x47)-尝试:{attempt+1}")
                    else:
                        print(f"[{i+1}/{len(decryptor.segments)}]-TS头错误:0x{decrypted_data[0]:02x}{decrypted_data[1]:02x}{decrypted_data[2]:02x}{decrypted_data[3]:02x} - 尝试{attempt+1}")
                else:
                    print(f"[{i+1}/{len(decryptor.segments)}]-文件太小,无法验证-尝试:{attempt+1}")

                return True
            except Exception as e:
                print(f"[{i+1}/{len(decryptor.segments)}] 尝试 {attempt+1} 失败: {e}")
                if attempt == max_retries - 1:
                    print(f"[{i+1}]超过最大重试次数,放弃")
                    return False
                else:
                    time.sleep(2)

    def run(self,max_workers):
        print("正在获取m3u8文件...")
        try:
            decryptor = HLSDecryptor.from_url(self.M3U8_URL, headers=self.HEADERS)
        except Exception as e:
            print(f"获取m3u8失败:{e}")
            return

        print(f"加密方式:{decryptor.method}")
        print(f"片段数量:{len(decryptor.segments)}")

        if decryptor.method == 'AES-128':
            print("检测到 AES-128 加密")
            choice = input("是否手动输入密钥 URL? (y/n, 默认 n):").strip().lower()
            if choice == 'y':
                manual_key_url = input("请输入完整的密钥URL:").strip()
                try:
                    decryptor.download_key(manual_key_url=manual_key_url, headers=self.HEADERS)
                    print("密钥下载成功")
                except Exception as e:
                    print(f"密钥下载失败:{e}")
                    return
            else:
                try:
                    decryptor.download_key(headers=self.HEADERS)
                    print("密钥自动下载成功")
                except Exception as e:
                    print(f"自动下载密钥失败: {e}")
                    retry = input("是否手动输入密钥 URL? (y/n):").strip().lower()
                    if retry == 'y':
                        manual_key_url = input("请输入完整的密钥URL:").strip()
                        decryptor.download_key(manual_key_url=manual_key_url, headers=self.HEADERS)
                        print("密钥下载成功")
                    else:
                        return

            print(f"密钥长度: {len(decryptor.key)} 字节")
            print(f"密钥: {decryptor.key.hex()}")
            if decryptor.iv:
                print(f"IV:{decryptor.iv.hex()}")
            else:
                print("IV:使用片段序号生成")
        else:
            print("无加密或加密方式不支持，将直接下载")

        print("\n开始下载并解密 TS 片段...")
        success_count = 0
        with ThreadPoolExecutor(max_workers) as executor:
            futures = []
            for i in range(len(decryptor.segments)):
                future = executor.submit(self.download_and_decrypt, i, decryptor, self.HEADERS, self.TS_DIR)
                futures.append(future)

            for future in futures:
                if future.result():
                    success_count += 1

        print(f"\n下载完成: 成功 {success_count}/{len(decryptor.segments)} 个片段")

        if success_count == 0:
            print("没有成功下载任何片段，退出")
            return

        print("\n开始合并视频...")
        output_mp4 = os.path.join(self.WORK_DIR, f"{self.VIDEO_NAME}.mp4")

        #concat demuxer（需要正确的文件列表）
        file_list = os.path.join(self.WORK_DIR, "file_list.txt")
        try:
            with open(file_list, 'w', encoding='utf-8') as f:
                for i in range(len(decryptor.segments)):
                    ts_path = os.path.join(self.TS_DIR, f"segment_{i:05d}.ts").replace('\\', '/')
                    #路径用引号括起来，防止空格问题
                    f.write(f"file '{ts_path}'\n")

            cmd = [
                "ffmpeg", "-f", "concat", "-safe", "0",
                "-i", file_list,
                "-c", "copy", "-fflags", "+genpts",
                output_mp4
            ]
            print("执行命令:", " ".join(cmd))
            import subprocess
            subprocess.run(cmd, check=True)
            print(f"合并成功！输出文件: {output_mp4}")

            confirm = input("是否删除临时 TS 文件夹？(y/n): ").strip().lower()
            if confirm == 'y':
                import shutil
                shutil.rmtree(self.TS_DIR)
                print("临时文件夹已删除")
            else:
                print("保留临时文件")

        except subprocess.CalledProcessError as e:
            print(f"concat demuxer合并失败:{e}")
            print("\n尝试备用方法:直接合并所有TS文件(需要先进入 TS 目录)...")
            try:
                # 切换到 TS 目录
                os.chdir(self.TS_DIR)
                # 使用 copy /b 合并（Windows）
                os.system("copy /b segment_*.ts output_temp.ts")
                # 转封装为 MP4
                subprocess.run([
                    "ffmpeg", "-i", "output_temp.ts", "-c", "copy",
                    os.path.join(self.WORK_DIR, f"{self.VIDEO_NAME}.mp4")
                ], check=True)
                print(f"备用合并成功！输出文件: {output_mp4}")
                os.remove("output_temp.ts")

                confirm = input("是否删除临时 TS 文件夹？(y/n): ").strip().lower()
                if confirm == 'y':
                    import shutil
                    shutil.rmtree(self.TS_DIR)
                    print("临时文件夹已删除")
                else:
                    print("保留临时文件")

            except Exception as e2:
                print(f"备用合并也失败: {e2}")
                print("请手动合并 TS 文件：")
                print(f"1. 进入目录: {self.TS_DIR}")
                print("2. 执行: copy /b segment_*.ts output.ts")
                print("3. 然后: ffmpeg -i output.ts -c copy \"../{VIDEO_NAME}.mp4\"")

