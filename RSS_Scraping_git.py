from email.mime.text import MIMEText
import smtplib
import feedparser
import schedule
import time
import datetime


"""""""""""""""""""""""""""
Set info to message text
"""""""""""""""""""""""""""
def get_message_text(list_max, name, list_title):
    message_text = ""
    if list_max == 1:
        message_text = message_text + "\n" + list_title + \
                        "\n" + name.entries[0].title +\
                        "\n" + name.entries[0].updated +\
                        "\n" + name.entries[0].link + "\n"
    else:
        for list_num, ent in enumerate(name.entries):
            if list_num == list_max:
                break
            No = list_num + 1
            message_text = message_text + "\n" + list_title + " " + str(No) +\
                            "\n" + ent.title +\
                            "\n" + ent.updated +\
                            "\n" + ent.link + "\n"
    return message_text

"""""""""""""""""""""""""""
Get RSS and send e-mail
"""""""""""""""""""""""""""
def get_RSS_send_email():
    #### Get RSS info in web
    onepunch    = feedparser.parse("https://tonarinoyj.jp/atom/series/13932016480028984490")
    tiempo      = feedparser.parse("https://tonarinoyj.jp/atom/series/10834108156632992433")
    gizmode     = feedparser.parse("https://www.gizmodo.jp/index.xml")
    gigazine    = feedparser.parse("https://gigazine.net/news/rss_2.0/")
    
    #### set message
    message_temp = get_message_text(1, onepunch, "Onepunch") +\
                   get_message_text(1, tiempo, "Tiempo") +\
                   get_message_text(5, gizmode, "Gizmode") +\
                   get_message_text(5, gigazine, "Gigazine")
    
    #### mail send
    # SMTP recognition information
    account = "hogehoge@hoge.com"       #set your e-mail account which you want to send from
    password = "xxxxxxxx"               #set your e-mail account password
     
    # To/From for e-mail
    to_email = "hoge@xxx.co.jp"         #set e-mail which you want to receive
    from_email = "hogehoge@hoge.com"    #set your e-mail account
     
    # MIME input
    subject = "Update information"
    message = message_temp
    msg = MIMEText(message)
    msg["Subject"]  = subject
    msg["To"]       = to_email
    msg["From"]     = from_email
     
    # Send e-mail
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(account, password)
    server.send_message(msg)
    server.quit()
    
"""""""""""""""""""""""""""
Main (schedule)
"""""""""""""""""""""""""""
#Start Job at every AM6:00
schedule.every().day.at("06:00").do(get_RSS_send_email)

while True:
    time_now = datetime.datetime.now()
    print(time_now.strftime('%Y.%m.%d. %H:%M:%S'), "  Probram runnning")
    schedule.run_pending()
    time.sleep(60)