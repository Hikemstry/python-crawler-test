# -*- coding: utf-8 -*-

import re
import binascii
from urllib.parse import urljoin
import requests
import urllib3
from Crypto.Cipher import AES
import colorama

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class HLSDecryptor:
 
    def __init__(self, m3u8_content=None, base_url=None):
        
        self.m3u8_content = m3u8_content
        self.base_url = base_url
        self.key = None          # 密钥二进制数据
        self.key_uri = None      # 密钥相对/绝对路径（从 m3u8 解析）
        self.iv = None           # 指定的 IV（如果 m3u8 中有）
        self.method = None       # 加密方法，如 'AES-128'
        self.media_sequence = 0  # 起始片段序号
        self.segments = []       # 片段 URL 列表

    def parse(self):
 
        lines = self.m3u8_content.strip().splitlines()
        self.segments = []
        self.key_uri = None
        self.iv = None
        self.method = None
        self.media_sequence = 0

        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith('#EXT-X-KEY:'):

                method_match = re.search(r'METHOD=([^,]+)', line)
                uri_match = re.search(r'URI="([^"]+)"', line)
                iv_match = re.search(r'IV=(0x[0-9A-Fa-f]+)', line)
                if method_match:
                    self.method = method_match.group(1)
                if uri_match:
                    self.key_uri = uri_match.group(1)
                if iv_match:
                    iv_hex = iv_match.group(1)[2:]  
                    
                    if len(iv_hex) % 2 != 0:
                        iv_hex = '0' + iv_hex
                    self.iv = binascii.unhexlify(iv_hex)
            elif line.startswith('#EXT-X-MEDIA-SEQUENCE:'):
                self.media_sequence = int(line.split(':')[1])
                
            elif line.startswith('#EXTINF:'):
                
                if i + 1 < len(lines):
                    seg_uri = lines[i+1].strip()
                    if not seg_uri.startswith(('http://', 'https://')):
                        if self.base_url:
                            seg_uri = urljoin(self.base_url, seg_uri)
                        else:
                            raise ValueError(f"{colorama.Fore.RED}相对路径片段需要提供base_url{colorama.Fore.RESET}")
                    self.segments.append(seg_uri)

        if not self.segments:
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    if not line.startswith(('http://', 'https://')):
                        if self.base_url:
                            line = urljoin(self.base_url, line)
                        else:
                            continue
                    self.segments.append(line)
        return self

    def download_key(self, manual_key_url=None, headers=None):
        
        if manual_key_url:
            url = manual_key_url
        elif self.key_uri:
            if self.key_uri.startswith(('http://', 'https://')):
                url = self.key_uri
            else:
                if not self.base_url:
                    raise ValueError(f"{colorama.Fore.RED}密钥为相对路径，需要提供 base_url{colorama.Fore.RESET}")
                url = urljoin(self.base_url, self.key_uri)
        else:
            raise ValueError(f"{colorama.Fore.RED}没有密钥信息可下载，且未提供 manual_key_url{colorama.Fore.RESET}")

        resp = requests.get(url, headers=headers or {}, verify=False)
        resp.raise_for_status()
        self.key = resp.content
        return self.key

    def decrypt_segment(self, encrypted_data, segment_index=None):
        """
        :param encrypted_data: 加密的 TS 片段二进制数据
        :param segment_index: 片段索引(从0开始)，用于生成 IV(如果 m3u8 未指定 IV)
        """
        if not self.key:
            raise ValueError(f"{colorama.Fore.RED}请先调用download_key()获取密钥{colorama.Fore.RESET}")

        if self.iv:
            iv = self.iv
        else:
            # 使用片段序号生成 IV（大端序 16 字节）
            seq_num = self.media_sequence + segment_index
            iv = seq_num.to_bytes(16, byteorder='big')

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted_data)

        # 去除 PKCS#7 填充
        pad_len = decrypted[-1]
        if 1 <= pad_len <= 16:
            decrypted = decrypted[:-pad_len]
        return decrypted

    @classmethod
    def from_url(cls, m3u8_url, headers=None):
 
        resp = requests.get(m3u8_url, headers=headers or {}, verify=False)
        resp.raise_for_status()
        content = resp.text
        base_url = m3u8_url[:m3u8_url.rfind('/')+1]
        decryptor = cls(content, base_url)
        decryptor.parse()
        return decryptor