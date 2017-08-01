from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from models import stocks,stocks_names,guru_and_dividends,bonds,stocksLastData
from helpers import handle_uploaded_file,readUploadedFiles,check_files,checkFiles
import datetime,json
from performances import performanceData
from valuationsMeasures import valuationsData
from valuationModels import valuationsModels

def home(request):
    return render(request,'home.html')

@login_required
def index(request):
    username = "Dav"
    error = ""
    error2 = ""
    data = []
    data_cleaned = []
    criteria = {}
    criteria["permin"] = 3.0
    criteria["permax"] = 13.0
    criteria["dermin"] = 0.0
    criteria["dermax"] = 85.0
    criteria["fcfmin"] = 5.5
    criteria["fcfmax"] = 100.0
    criteria["roicmin"] = 0.0
    criteria["roicmax"] = 300.0
    criteria["dcfmin"] = 0.0
    criteria["dcfmax"] = 300.0
    criteria["sommin"] = 0.0
    criteria["sommax"] = 300.0

    stocks_names_list = [a_dict["stock"] for a_dict in list(stocks_names.objects.values('stock'))]
    existing_stocks_list = [a_dict["stock"] for a_dict in list(stocksLastData.objects.values('stock'))] 
    existing_stocks_list = list(set(existing_stocks_list))
    if request.user.is_authenticated():
        username = request.user.username
    try:
        for stock_name in existing_stocks_list:
            if stock_name in stocks_names_list:
                try:
                    item = stocksLastData.objects.filter(stock=stock_name.upper()).last()
                    if item:
                        data.append(item)
                except Exception as e:
                    error += str(e)
    except Exception as e:
        error += str(e)
    stocksAvailable = []
    for item in data:
        try:
            stocksAvailable.append(item.stock)
            if (float(item.dcf_value.replace("$","")) >= criteria["dcfmin"] and 
                float(item.dcf_value.replace("$","")) <= criteria["dcfmax"] and  
                float(item.debtEquitity) >= criteria["dermin"] and 
                float(item.debtEquitity) <= criteria["dermax"] and 
                float(item.freecashflowpercent.replace("%","")) >= criteria["fcfmin"] and  
                float(item.freecashflowpercent.replace("%","")) <= criteria["fcfmax"] and 
                float(item.roic) >= criteria["roicmin"] and 
                float(item.roic) <= criteria["roicmax"] and
                float(item.safety_margin) >= criteria["sommin"] and
                float(item.safety_margin) <= criteria["sommax"]):
                data_cleaned.append(item) 
        except Exception as e:
            error2 += str(e)
    if request.method == "POST":

        dcfdata = request.POST.get("dcfdata")
        derdata = request.POST.get("derdata")
        fcfdata = request.POST.get("fcfdata")
        roicdata = request.POST.get("roicdata")
        somdata = request.POST.get("somdata")

        if dcfdata == "":
            dcfdata = str(criteria["permin"]) + "," + str(criteria["permax"])
        if derdata == "":
            derdata = str(criteria["dermin"]) + "," + str(criteria["dermax"])
        if fcfdata == "":
            fcfdata = str(criteria["fcfmin"]) + "," + str(criteria["fcfmax"])
        if roicdata == "":
            roicdata = str(criteria["roicmin"]) + "," + str(criteria["roicmax"])
        if somdata == "":
            somdata = str(criteria["sommin"]) + "," + str(criteria["sommax"])

        dcfmin = dcfdata.split(",")[0]
        dcfmax = dcfdata.split(",")[1]
        dermin = derdata.split(",")[0]
        dermax = derdata.split(",")[1]
        fcfmin = fcfdata.split(",")[0]
        fcfmax = fcfdata.split(",")[1]     
        roicmin = roicdata.split(",")[0]
        roicmax = roicdata.split(",")[1]
        sommin = somdata.split(",")[0]
        sommax = somdata.split(",")[1]

        print dcfmin,dcfmax,dermin,dermax,fcfmin,fcfmax,roicmin,roicmax,sommin,sommax

        error += " Numbers: "+str(dcfmin)+" "+str(dcfmax)+" "+str(dermin)+" "+str(dermax)+" "+str(fcfmin)+" "+str(fcfmax)+" "+str(roicmin)+" "+str(roicmax)+" "+str(sommin)+" "+str(sommax)
        data_cleaned = []
        for item in data:
            try:
                if (float(item.dcf_value.replace("$","")) >= float(dcfmin) and 
                    float(item.dcf_value.replace("$","")) <= float(dcfmax) and 
                    float(item.debtEquitity) >= float(dermin) and 
                    float(item.debtEquitity) <= float(dermax) and 
                    float(item.freecashflowpercent.replace("%","")) >= float(fcfmin) and 
                    float(item.freecashflowpercent.replace("%","")) <= float(fcfmax) and 
                    float(item.roic) >= float(roicmin) and 
                    float(item.roic) <= float(roicmax) and
                    float(item.safety_margin) >= criteria["sommin"] and
                    float(item.safety_margin) <= criteria["sommax"]):
                    data_cleaned.append(item)
            except Exception as e:
                error2 += str(e)
    return render(request, 'index.html',{"user":username,"data":data_cleaned,"error":error,"error2":error2,
                                         "criteria":criteria,"stocksAvailable":stocksAvailable})

@login_required
def summary(request):
    path = r"/home/ubuntu/docs/"
    username = "Dav"
    stock = None
    availableFiles = None
    csv_files = None
    names = None
    pickle_file = None
    error = ""
    data = None
    stock_data = None
    ratios = None
    price = None
    market_cap = None
    bond_data = None
    cocad = {}
    if request.user.is_authenticated():
        username = request.user.username
    if request.method == "POST":
        stock = request.POST.get("stock","")
        try:
            stock_data = [stocksLastData.objects.filter(stock=stock.upper()).last().__dict__]
            price = stock_data[0]['price']
            market_cap = stock_data[0]['capitalmarket']
            data_obj = checkFiles(stock)
            names = data_obj.names
            availableFiles = data_obj.stock_files
            csv_files = data_obj.csv_files
            pickle_file = data_obj.pickle_file
            is_csv_file = data_obj.is_csv_file
            bs_csv_file = data_obj.bs_csv_file
            cf_csv_file = data_obj.cf_csv_file
            data = data_obj.data

            ratios = {}
            ratios['1'] = {}
            ratios['5'] = {}
            ratios = performanceData(pickle_file,is_csv_file,bs_csv_file,cf_csv_file,ratios)
            ratios = valuationsData(pickle_file,is_csv_file,bs_csv_file,cf_csv_file,ratios,price,market_cap)
            
            try:
                stock_names_data = stocks_names.objects.filter(stock=stock.upper()).last().__dict__
                location = stock_names_data['location']
                if location.lower() == "aus":
                    bond_data = bonds.objects.all().last().__dict__["australian_bond"]
                elif location.lower() == "us":
                    bond_data = bonds.objects.all().last().__dict__["american_bond"]
                else:
                    bond_data = "N/A"
            except Exception as e:
                print e
            ratios = valuationsModels(pickle_file,is_csv_file,bs_csv_file,cf_csv_file,ratios,price,market_cap,4.4,bond_data)
            try:
                cost_of_capital_and_dividends = guru_and_dividends.objects.filter(stock=stock.upper()).last().__dict__
                cocad["cost_of_capital"] = cost_of_capital_and_dividends['cost_of_capital']
                cocad["dividend"] = cost_of_capital_and_dividends['dividend']
                cocad["dividend_five_years"] = cost_of_capital_and_dividends['dividend_five_years']
                cocad["intrinsic_value"] = cost_of_capital_and_dividends['intrinsic_value']
            except Exception as e:
                print e

            availableFiles = len(availableFiles)
            if availableFiles > 0:
                availableFiles = True
            else:
                availableFiles = False
        except Exception as e:
            print e
            error += str(e)
        stock = stock.upper()
    return render(request, 'summary.html',{"user":username,"stock":stock,"csv_files":csv_files,"price":price,
                                           "files":availableFiles,"error":error,"pickle_file":pickle_file,
                                           "names":names,"data":data,"stockdata":stock_data,"ratios":ratios,
                                           "market_cap":market_cap,"cocad":cocad,"bond_data":bond_data})

@login_required
def stockspage(request):
    username = "Dav"
    stock = None
    error = None
    stocks_names_list = [str(a_dict["stock"]).upper() for a_dict in list(stocks_names.objects.values('stock'))]
    locations_names_list = [str(a_dict["location"]).upper() for a_dict in list(stocks_names.objects.values('location'))]
    stocks_and_locations = sorted([(st,loc) for st,loc in zip(stocks_names_list,locations_names_list)],key=lambda x:x[0])
    number_of_stocks = len(stocks_names_list)
    if request.user.is_authenticated():
        username = request.user.username
    if request.method == "POST":
        stock = request.POST.get("stocks", "")
        location = request.POST.get("locations", "")
        try:
            obj = stocks_names(stock=stock,location=location,date=datetime.datetime.now())
            obj.save()
            stocks_names_list = [str(a_dict["stock"]).upper() for a_dict in list(stocks_names.objects.values('stock'))] 
            locations_names_list = [str(a_dict["location"]).upper() for a_dict in list(stocks_names.objects.values('location'))] 
            stocks_and_locations = sorted([(st,loc) for st,loc in zip(stocks_names_list,locations_names_list)],key=lambda x:x[0])
            number_of_stocks = len(stocks_names_list)
        except Exception as e:
            error = e
    return render(request, 'stockspage.html',{"user":username,"stocks":stocks_names_list,
                                              "addedstocks":stock,"error":error,
                                              "lenstocks":number_of_stocks,
                                              "locations":locations_names_list,
                                              "stocks_and_locations":stocks_and_locations})

@login_required
def stocksfiles(request):
    username = "Dav"
    keywords = []
    if request.user.is_authenticated():
        username = request.user.username
    if request.method == "POST" and request.FILES['phrasefile']:
        a_file = request.FILES['phrasefile']
        path = handle_uploaded_file(a_file)   
        stocks_obj = readUploadedFiles(path)
        stocks,locations = stocks_obj.reader()
        for stock,location in zip(stocks,locations):
            try:
                obj = stocks_names(stock=stock,location=location,date=datetime.datetime.now())
                obj.save()
    	    except Exception as e:
            	print e
    return render(request, 'stocks_excel.html',{"user":username,"phrase":""})

@login_required
def tables(request):
    data = {}
    if request.method == "POST":
        stock = request.POST.get("django_stock")
        table = request.POST.get("django_table")
        table_id = request.POST.get("django_id")
        data["stock"] = stock.lower()
        data["table"] = table.lower()
        data["id"] = table_id
        data["url"] = "/table/{0}/{1}".format(stock,table)
        data_obj = checkFiles(stock.lower(),table.lower(),True)
        path = data_obj.data
        if path != "":
            data["working"] = "yes"
        else:
            data["working"] = "no"
    return HttpResponse(json.dumps(data),content_type="application/json")

@login_required
def serveFiles(request,stock,table):
    stock = stock.lower()
    table = table.lower()
    data_obj = checkFiles(stock,table,True)
    path = data_obj.data
    name = str(stock) + " " + str(table).upper()
    if path != "":
        with open(path,"rb") as pdf:
            response = HttpResponse(pdf.read(),content_type='application/pdf')
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(name)    
        return response

@login_required
def remover(request):
    from collections import Counter
    username = "Dav"
    locations = None
    error = None
    locations = None
    if request.user.is_authenticated():
        username = request.user.username
    try:
        stocks_values = stocks_names.objects.all().values()
        locations = [stock["location"] for stock in stocks_values]
        locations_counts = Counter(locations).items()
    except Exception as e:
        error = e
    if request.method == "POST":
        loc = request.POST.get("location", "")
        try:
            stocks = stocks_names.objects.filter(location=loc)
            if stocks:
                for stock in stocks:
                    stock.delete()
                stocks_values = stocks_names.objects.all().values()
                locations = [stock["location"] for stock in stocks_values]
                locations_counts = Counter(locations).items()
            else:
                error = "We have the following locations available : {0}".format(", ".join(list(set(locations))))
        except Exception as e:
            error = e
    return render(request, 'remover.html',{"locations":locations_counts,"username":username,"error":error})
