import csv, datetime,urllib2,os,json,schedule,time,errno,zipfile,redis

import operator

from models import BSEObject


def silentRemove(filename):
    try:
        os.remove(filename)
        print filename + " removed"+ str(datetime.datetime.now())
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise e
    return

def bhavDate():
    current_time = datetime.datetime.now()

    if (current_time.hour < 10):
        current_time = (current_time - datetime.timedelta(hours=12))
    dateStr = current_time

    if(current_time.weekday()>4):
        # get last friday if today is sunday/ saturaday
        last_friday = (current_time.date()
                       - datetime.timedelta(days=current_time.weekday())
                       + datetime.timedelta(days=4, hours=12))
        dateStr = last_friday

    return dateStr

def getBhav():
    date_str_full = bhavDate().date()
    date_str = bhavDate().strftime("%d%m%y")
    downloadUrl = "https://www.bseindia.com/download/BhavCopy/Equity/EQ"+date_str+"_CSV.ZIP"
    bhavZipFile = "eq" + date_str + "_csv.zip"
    destination = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(destination) is False:
        os.mkdir(destination)
    fullpath = os.path.join(destination, bhavZipFile)
    print fullpath

    try:
        with open(fullpath, 'w+b') as f:
            f.write(urllib2.urlopen(downloadUrl).read())
            f.close()
        if os.path.exists(fullpath):
            results = []
            fileHandler = zipfile.ZipFile(fullpath, 'r')
            fileHandler.extractall(destination)
            fileHandler.close()
            data = []

            with open(destination + '\EQ' + date_str + '.CSV') as f:
                for row in csv.DictReader(f):
                    data.append(BSEObject(row.get("SC_CODE"), row.get("SC_NAME"), float(row.get("OPEN")), float(row.get("LOW")),
                                          float(row.get("CLOSE")), float(row.get("HIGH"))))

            sorted_data = sorted(data, key=lambda bse: bse.close, reverse=True)
            json_string = json.dumps([ob.__dict__ for ob in data])
            redis_server = redis.Redis("localhost")
            redis_server.flushall()

            redis_server.set("bhavcopy",json_string)
            redis_server.set("bsetop",json.dumps([ob.__dict__ for ob in sorted_data[:10]]))
            redis_server.set("datestr",date_str_full)
    except:
        import sys
        print str(sys.exc_info())
        schedule.every(1).minutes.do(getBhav)
    try:
        time.sleep(2)
        silentRemove(fullpath)
        silentRemove(destination + '\EQ' + date_str + '.CSV')
    except:
        schedule.every(1).minutes.do(getBhav)
    finally:
        print datetime.datetime.now()


#getBhav()

schedule.every(1).minutes.do(getBhav)

while 1:
    schedule.run_pending()
    time.sleep(1)

