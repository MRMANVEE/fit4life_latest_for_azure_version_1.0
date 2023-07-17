   #For scheduling task execution
import schedule
import time
import datetime

def job():
    now = datetime.datetime.utcnow()
    with open('timer_log.txt','a') as data:
        data.write(str(now) + '\n')


schedule.every(1).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every(5).to(10).minutes.do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)
schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)











"""import time
import schedule
import datetime

def task():
    now = datetime.datetime.utcnow()
    with open('timer_log.txt','a') as data:
        data.write(str(now) + '\n')

schedule.every(5).seconds.do(task)

while True:

    schedule.run_pending()
    time.sleep(1)
    """