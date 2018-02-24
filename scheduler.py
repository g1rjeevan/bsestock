import schedule
import time

def job():
    print("I'm working...fucker")

schedule.every(7).seconds.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)