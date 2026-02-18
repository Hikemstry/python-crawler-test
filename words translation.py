import requests

url="https://fanyi.baidu.com/sug"


s=input("输入一个单词：\n")
dat={"kw":s}
resp=requests.post(url,data=dat)
print(resp.json())
resp.close()