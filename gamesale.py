import smtplib
from email.mime.text import MIMEText
import requests
import time
from pyquery import PyQuery as pq

n_url = 'https://www.ptt.cc/bbs/part-time/index.html'
platform_dict = {0:'PS4',1:'NS',2:'PS3',3:'PSV',4:'XONE',5:'PC',6:''}
sent = []
msg = '抓到了！\n'

print('抓抓gamesale版買賣資訊!')
platform = int(input('抓什麼平台呢? (0:PS4,1:Switch,2:PS3,3:PSV,4:XONE,5:PC,6:全)'))
keywords = input('輸入要抓的關鍵字，用空白區隔(只要其中一個符合就會通知!)').split()
msg_to = input('抓到內容時寄到哪個信箱?')

def send_email(msg):
    gmail_user = 'philasofa@gmail.com'
    gmail_password = 'ybncczgytybzbyfb' #應用程式password

    msg = MIMEText(msg)
    msg['Subject'] = '爬蟲通知'
    msg['From'] = gmail_user
    msg['To'] = msg_to

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    print(server.ehlo()) 
    server.login(gmail_user, gmail_password)
    server.send_message(msg)
    server.quit()

    print('Email sent!')

pages_per_crawler = 50

while True:
    for i in range(pages_per_crawler):
        res = requests.get(n_url)
        doc = pq(res.text)

        a = doc('.title a')
        b = doc('#action-bar-container > div > div.btn-group.btn-group-paging > a:nth-child(2)')
        n_url  = 'https://www.ptt.cc' + b.attr("href")
        
        for j in a.items():
            title = j.text()
            url = j.attr('href')
            for keyword in keywords:
                if keyword in title and platform_dict[platform] in title and url not in sent:
                    sent.append(url)
                    msg += title + '\n'
                    msg += 'https://www.ptt.cc' + url + '\n'
                    print(title,url)
        
    if msg != '抓到了！\n' :
        send_email(msg)
    
    msg = '抓到了！\n' 
    'https://www.ptt.cc/bbs/part-time/index.html'
    time.sleep(10)
