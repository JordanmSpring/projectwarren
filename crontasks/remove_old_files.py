import datetime
import os

paths = ["/home/ubuntu/crontasks/tmp","/home/ubuntu/tmp"]

VERBOSE = True
LOGGING = False

def log(message):
    message = str(message)
    if VERBOSE:
        print datetime.datetime.now().strftime('[%d-%m-%y %H:%M:%S] ') + message
    if LOGGING:
        pass

class cleaner:
    def __init__(self):
        self.files_list = []
        self.files()
    def modification_date(self,file_name):
        t = os.path.getmtime(file_name)
        return datetime.datetime.fromtimestamp(t).strftime("%y%m%d")
    def files(self):
        two_days = range(0,2)
        for day in two_days:
            Date = (datetime.date.today() - datetime.timedelta(days=day)).strftime("%y%m%d")
            self.files_list.append(Date)
    def remove(self,path):
        existing_files = [f for f in os.listdir(path)]
        for file in existing_files:
            file_date = self.modification_date(str(path)+"/"+str(file))
            if file_date not in self.files_list:
                if os.path.isfile(os.path.join(path,file)):
                    os.remove(os.path.join(path,file))
                    log("File removed: {0}".format(os.path.join(path,file)))
                    log("Date: {0}".format(file_date))

log("Starting Process")
for path in paths:
    obj = cleaner()
    obj.remove(path)
