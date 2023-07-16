import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import os
"""
作者 薛明昊
时间 203-7-17
操作系统 windows
用途 爬取菠萝包轻小说的内容，需要selenium进行解密。
"""


link = r"https://www.linovelib.com/novel/2829/catalog"  # 这是小说目录页面
myBookTitle = "啦啦啦"

#================================此后为源码核心内容，请勿乱动==================================

chrome_driver_path_obj = Service("D:\Project\python\webDriver\msedgedriver.exe")
web = webdriver.Edge(service=chrome_driver_path_obj)

os.makedirs(myBookTitle+"/imgs",exist_ok=True)

print("欢迎使用菠萝包轻小说整合器 v1.5")

#获得一张图，如 https://img1.readpai.com/3/3184/161936/191426.jpg
def imgGetter(link):
    headers = {
        'referer': 'https://www.linovelib.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    }
    x = requests.get(link,headers=headers)
    return x.content

#获得一个章节所属卷，放入的应该是一个etree.HTML输出的对象
def juanGetter(juan):
    ju = juan.xpath("//div[@class='chepnav']/text()")[-1]
    return ju.replace("\n","").replace(">","").replace(" ","")

host = "https://www.linovelib.com"


muLu = requests.get(link)  # 获取目录
muLuObject = etree.HTML(muLu.text)  # 获取目录对象
bookTitle = muLuObject.xpath(r"//div[@class='book-meta']/h1/text()")[0]
liSrc = muLuObject.xpath(r"//div[@class='volume-list']//ul/li/a/@href")[0] #获得目录头
print(liSrc)


mainText = requests.get(f"{host}{liSrc}")  # 获取主页面
web.get(f"{host}{liSrc}") # 获取主页面Selenium
book = open(f"{myBookTitle}/{myBookTitle}.txt","w",encoding="utf-8")

 
count = 0

while True:
    page = etree.HTML(mainText.text) #获取当前页面的数据
    title = page.xpath("//div[@id='mlfy_main_text']/h1/text()")[0] #章节标题
    juan = juanGetter(page) #卷标题
    print(f"正在下载{juan}-{title}...")
    textList = [i.text for i in web.find_elements(By.XPATH,"//div[@id='mlfy_main_text']/div[@id='TextContent']/p")]
    imgs = page.xpath("//div[@id='mlfy_main_text']/div[@id='TextContent']/img/@data-src") #所有图
    
    allText = juan + "  " + title + "\n" + "\n".join(textList) + "\n" + "\n" + "\n"
    xiaYiZhangSrc = page.xpath("//p[@class='mlfy_page']/a[last()]/@href")[0] #下一页连接
    xiaYiZhangTitle = page.xpath("//p[@class='mlfy_page']/a[last()]/text()")[0] #比如 是下一页 下一章 返回书页
    book.write(allText)
    for i,j in enumerate(imgs):
        count+=1
        with open(f"{myBookTitle}/imgs/{juan}-{count}.jpg","wb") as f:
            f.write(imgGetter(imgs[i]))
    print(f"下载完成...")
    if xiaYiZhangTitle == "返回书页":
        break
    else:
        mainText = requests.get(f"{host}{xiaYiZhangSrc}")  # 获取主页面
        web.get(f"{host}{xiaYiZhangSrc}") # 获取主页面Selenium
book.close()

print("下载整合完成")
