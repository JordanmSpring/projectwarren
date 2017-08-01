import pandas as pd
from collections import OrderedDict
import numpy as np
import os

class checkFiles:
    def __init__(self,stock,selector=None,is_pdf=False):
        self.stock = stock.lower()
        self.selector = selector
        self.is_pdf = is_pdf
        print self.stock
        print self.selector
        self.path = r"/home/ubuntu/docs"
        self.pickles_path = r"/home/ubuntu/pickles"
        self.names = []
        self.stock_files = []
        self.getFiles()
        print
        print self.names
        print 
        print self.stock_files
        print
        print len(self.names),len(self.stock_files)
        if not self.is_pdf:
            self.data = self.getCSVS()
        else:
            self.data = self.getPdf()
    def cleanName(self,name):
        stock = name.lower().replace("is","").replace("bs","").replace("cf","")
        stock = stock.replace(".csv","").replace(".pdf","").strip()
        return stock
    def getFiles(self):
        self.csv_files = [] 
        self.is_csv_file = None
        self.bs_csv_file = None
        self.cf_csv_file = None
        self.pickle_file = [os.path.join(self.pickles_path,f) for f in os.listdir(self.pickles_path) if f.replace(".pickle","") == self.stock.upper()]
        if self.pickle_file:
            self.pickle_file = self.pickle_file[0]
        else:
            self.pickle_file = None
        if self.selector:
            self.selector = self.selector.lower()
        for root, dirs, files in os.walk(self.path, topdown=False):
            for name in files:
                if self.stock.lower().strip() == self.cleanName(name):
                    self.stock_files.append(os.path.join(root, name))
                    self.names.append(name)
                    if ".csv" in  name:
                        self.csv_files.append(os.path.join(root, name))
                    if "IS.csv" in name:
                        self.is_csv_file = os.path.join(root, name)
                    if "BS.csv" in name:
                        self.bs_csv_file = os.path.join(root, name)
                    if "CF.csv" in name:
                        self.cf_csv_file = os.path.join(root, name)
    def getCSVS(self):
        titles = []
        list_of_dicts = []
        for name,a_file in zip(self.names,self.stock_files):
            larger_dict = {}
            if a_file.endswith(".csv"):
                title = name.replace(self.stock,"").replace(".csv","").strip()
                print title
                if title == "IS":
                    title = "Income Statement"
                elif title == "CF":
                    title = "Cash Flow"
                elif title == "BS":
                    title = "Balance Sheet"
                print title
                titles.append(title)
                df = pd.read_csv(a_file)
                df = df.replace(np.nan,'--', regex=True)
                dicts = []
                columns = []

                for column in df.columns.tolist():
                    if "Unnamed" not in column:
                        columns.append(column)
                if self.selector:
                    if self.selector == title:
                        for i in range(df.shape[0]):
                            a_dict = OrderedDict()
                            for column in df.columns.tolist():
                                if "Unnamed" not in column:
                                    value_to_guard = df[column].tolist()[i]
                                    try:
                                        if int(value_to_guard.replace("$","")) > 1000000 or int(value_to_guard.replace("$","")) < -1000000:
                                            value_to_guard = int(value_to_guard.replace("$",""))/1000000
                                            
                                            value_to_guard = format(value_to_guard,",d")
                                            value_to_guard = "$" + str(value_to_guard) + " M"
                                    except Exception as e:
                                        pass
                                    #print value_to_guard
                                    a_dict[column] = value_to_guard
                            dicts.append(a_dict)
                        larger_dict["title"] = title
                        larger_dict["columns"] = columns
                        larger_dict["dicts"] = dicts
                        list_of_dicts.append(larger_dict)
                else:
                    for i in range(df.shape[0]):
                        a_dict = OrderedDict()
                        for column in df.columns.tolist():
                            if "Unnamed" not in column:
                                value_to_guard = df[column].tolist()[i]
                                try:
                                    if int(value_to_guard.replace("$","")) > 1000000 or int(value_to_guard.replace("$","")) < -1000000:
                                        value_to_guard = int(value_to_guard.replace("$",""))/1000000
                                        value_to_guard = format(value_to_guard,",d")
                                        value_to_guard = "$" + str(value_to_guard) + " M"
                                except Exception as e:
                                    pass
                                #print value_to_guard
                                a_dict[column] = value_to_guard
                        dicts.append(a_dict)    
                    larger_dict["title"] = title
                    larger_dict["columns"] = columns
                    larger_dict["dicts"] = dicts
                    list_of_dicts.append(larger_dict)
        return list_of_dicts
    def getPdf(self):
        found_file = ""
        for name,a_file in zip(self.names,self.stock_files):
            if a_file.endswith(".pdf"): 
                print a_file
                title = name.lower().replace(self.stock,"").replace(".pdf","").strip()
                print title
                print name
                print
                if self.selector == title:
                    print title
                    found_file = a_file
        return found_file

def getFilesData(stock,names,files):
    titles = []
    list_of_dicts = []
    for name,a_file in zip(names,files):
        larger_dict = {}
        title = name.replace(stock,"").replace(".csv","").strip()
        print title
        if title == "IS":
            title = "Income Statement"
        elif title == "CF":
            title = "Cash Flow"
        elif title == "BS":
            title = "Balance Sheet"
        titles.append(title)
        df = pd.read_csv(a_file)
        df = df.replace(np.nan,'--', regex=True)
        dicts = []
        columns = []

        for column in df.columns.tolist():
            if "Unnamed" not in column:
                columns.append(column)

        for i in range(df.shape[0]):
            a_dict = OrderedDict()
            for column in df.columns.tolist():
                if "Unnamed" not in column:
                    a_dict[column] = df[column].tolist()[i]
            dicts.append(a_dict)    
        larger_dict["title"] = title
        larger_dict["columns"] = columns
        larger_dict["dicts"] = dicts
        list_of_dicts.append(larger_dict)
    return list_of_dicts

def clean_name(name):
    return name.lower().replace("is","").replace("bs","").replace("cf","").replace(".csv","").strip()

def check_files(stock):
    path = r"/home/ubuntu/docs"
    names = []
    stock_files = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if stock.lower().strip() == clean_name(name):
                stock_files.append(os.path.join(root, name))
            names.append(name)  
   
    data = getFilesData(stock,names,stock_files)
    return stock_files,names,data

def handle_uploaded_file(f):
    named = f.name
    pos = "/home/ubuntu/files/"
    path = pos + str(named)
    with open(path,'w') as dest:
        for chunck in f.chunks():
            dest.write(chunck)
    return path

class readUploadedFiles:
    def __init__(self,path):
        self.path = path
    def reader(self):
        try:
            df = pd.read_excel(self.path)
        except Exception:
            df = pd.read_csv(self.path)
        df.columns = df.columns.str.lower()
        if "stocks" not in df.columns and "stock" not in df.columns:
            try:
                df = pd.read_excel(self.path,header=None)
            except Exception:
                df = pd.read_csv(self.path,header=None)
            try:
                stocks = df[0].tolist()
                locations = df[1].tolist()
            except Exception as e:
                print e
        else:
            try:
                stocks = df["stocks"].tolist()
            except Exception as e:
                stocks = df["stock"].tolist()
            try:
                locations = df["countries"].tolist()
            except Exception as e:
                locations = df["country"].tolist()
        return stocks,locations
