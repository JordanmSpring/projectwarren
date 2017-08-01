from __future__ import unicode_literals
from django.utils.encoding import smart_unicode
from django.db import models
import datetime

# Create your models here.

class stocks(models.Model):
    stock = models.CharField(max_length=10,blank=False)
    date = models.CharField(max_length=25,blank=False)
    scraperError = models.CharField(max_length=250,blank=True)
    scraperApi = models.CharField(max_length=250,blank=True)
    bookValue = models.CharField(max_length=12,blank=True)   
    debtEquitity = models.CharField(max_length=12,blank=True) 
    priceEarning = models.CharField(max_length=12,blank=True) 
    operatingCashFlow = models.CharField(max_length=12,blank=True)
    leveredCashFlow = models.CharField(max_length=12,blank=True)
    priceEarningGrowth = models.CharField(max_length=12,blank=True)
    roic = models.CharField(max_length=12,blank=True)
    capitalmarket = models.CharField(max_length=12,blank=True)
    freecashflow = models.CharField(max_length=12,blank=True)
    freecashflowpercent = models.CharField(max_length=12,blank=True)
    exchange = models.CharField(max_length=150,blank=True)
    name = models.CharField(max_length=150,blank=True)
    price = models.CharField(max_length=15,blank=True)
    dcf_value = models.CharField(max_length=15,blank=True)
    safety_margin = models.CharField(max_length=15,blank=True)

    class Meta:
        verbose_name = "Stocks Data"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return smart_unicode(self.stock)
    def dates(self):
        return smart_unicode(self.date)
    def scraperErrors(self):
        return smart_unicode(self.scraperError)
    def scraperApis(self):
        return smart_unicode(self.scraperApi)
    def bookValues(self):
        return smart_unicode(self.bookValue)
    def debtEquitities(self):
        return smart_unicode(self.debtEquitity)
    def priceEarnings(self):
        return smart_unicode(self.priceEarning)
    def operatingCashFlows(self):
        return smart_unicode(self.operatingCashFlow)
    def leveredCashFlows(self):
        return smart_unicode(self.leveredCashFlow)
    def priceEarningGrowths(self):
        return smart_unicode(self.priceEarningGrowth)
    def roics(self):
        return smart_unicode(self.roic)
    def capitalMarkets(self):
        return smart_unicode(self.capitalmarket)
    def freeCashFlows(self):
        return smart_unicode(self.freecashflow)
    def freeCashFlowPercents(self):
        return smart_unicode(self.freecashflowpercent)
    def exchanges(self):
        return smart_unicode(self.exchange)
    def names(self):
        return smart_unicode(self.name)
    def prices(self):
        return smart_unicode(self.price)
    def dcf_values(self):
        return smart_unicode(self.dcf_value)
    def safety_margins(self):
        return smart_unicode(self.safety_margin)

class stocksLastData(models.Model):
    stock = models.CharField(max_length=10,blank=False)
    date = models.CharField(max_length=25,blank=False)
    scraperError = models.CharField(max_length=250,blank=True)
    scraperApi = models.CharField(max_length=250,blank=True)
    bookValue = models.CharField(max_length=12,blank=True)   
    debtEquitity = models.CharField(max_length=12,blank=True) 
    priceEarning = models.CharField(max_length=12,blank=True) 
    operatingCashFlow = models.CharField(max_length=12,blank=True)
    leveredCashFlow = models.CharField(max_length=12,blank=True)
    priceEarningGrowth = models.CharField(max_length=12,blank=True)
    roic = models.CharField(max_length=12,blank=True)
    capitalmarket = models.CharField(max_length=12,blank=True)
    freecashflow = models.CharField(max_length=12,blank=True)
    freecashflowpercent = models.CharField(max_length=12,blank=True)
    exchange = models.CharField(max_length=150,blank=True)
    name = models.CharField(max_length=150,blank=True)
    price = models.CharField(max_length=15,blank=True)
    dcf_value = models.CharField(max_length=15,blank=True)
    safety_margin = models.CharField(max_length=15,blank=True)

    class Meta:
        verbose_name = "Latest Stocks Data"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return smart_unicode(self.stock)
    def dates(self):
        return smart_unicode(self.date)
    def scraperErrors(self):
        return smart_unicode(self.scraperError)
    def scraperApis(self):
        return smart_unicode(self.scraperApi)
    def bookValues(self):
        return smart_unicode(self.bookValue)
    def debtEquitities(self):
        return smart_unicode(self.debtEquitity)
    def priceEarnings(self):
        return smart_unicode(self.priceEarning)
    def operatingCashFlows(self):
        return smart_unicode(self.operatingCashFlow)
    def leveredCashFlows(self):
        return smart_unicode(self.leveredCashFlow)
    def priceEarningGrowths(self):
        return smart_unicode(self.priceEarningGrowth)
    def roics(self):
        return smart_unicode(self.roic)
    def capitalMarkets(self):
        return smart_unicode(self.capitalmarket)
    def freeCashFlows(self):
        return smart_unicode(self.freecashflow)
    def freeCashFlowPercents(self):
        return smart_unicode(self.freecashflowpercent)
    def exchanges(self):
        return smart_unicode(self.exchange)
    def names(self):
        return smart_unicode(self.name)
    def prices(self):
        return smart_unicode(self.price)
    def dcf_values(self):
        return smart_unicode(self.dcf_value)
    def safety_margins(self):
        return smart_unicode(self.safety_margin)

class stocks_names(models.Model):
    stock = models.CharField(max_length=10,blank=False, unique=True)
    date = models.DateTimeField(default=datetime.datetime.now(),blank=True) 
    location = models.CharField(max_length=12,blank=True)

    class Meta:
        verbose_name = "Stocks"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return smart_unicode(self.stock)
    def dates(self):
        return smart_unicode(self.date)
    def locations(self):
        return smart_unicode(self.location)

class unworkingStocks(models.Model):
    stock = models.CharField(max_length=10,blank=False)
    date = models.DateTimeField(default=datetime.datetime.now(),blank=True)

    class Meta:
        verbose_name = "Unworking Stocks"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return smart_unicode(self.stock)
    def dates(self):
        return smart_unicode(self.date)

class bannedStocks(models.Model):
    stock = models.CharField(max_length=10,blank=False, unique=True)
    date = models.DateTimeField(default=datetime.datetime.now(),blank=True)

    class Meta:
        verbose_name = "Banned Stocks"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return smart_unicode(self.stock)
    def dates(self):
        return smart_unicode(self.date)

class guru_and_dividends(models.Model):
    stock = models.CharField(max_length=10,blank=False)
    date = models.DateTimeField(default=datetime.datetime.now(),blank=True)
    cost_of_capital = models.CharField(max_length=10,blank=False)
    dividend = models.CharField(max_length=10,blank=False)
    dividend_five_years = models.CharField(max_length=10,blank=False)
    intrinsic_value = models.CharField(max_length=10,blank=True)
    safety_margin = models.CharField(max_length=10,blank=True)

    class Meta:
        verbose_name = "Guru Values and Dividends"
        verbose_name_plural = verbose_name
    def stocks(self):
        return smart_unicode(self.stock)
    def dates(self):
        return smart_unicode(self.date)
    def cost_of_capitals(self):
        return smart_unicode(self.cost_of_capital)
    def dividends(self):
        return smart_unicode(self.dividend)
    def dividends_five_years(self):
        return smart_unicode(self.dividend_five_years)
    def intrinsic_values(self):
        return smart_unicode(self.intrinsic_value)
    def safety_margins(self):
        return smart_unicode(self.safety_margin)

class bonds(models.Model):
    australian_bond = models.CharField(max_length=10,blank=False)
    american_bond = models.CharField(max_length=10,blank=False)
    date = models.DateTimeField(default=datetime.datetime.now(),blank=True)
    scraper_working = models.CharField(max_length=5,blank=True)

    class Meta:
        verbose_name = "Bonds"
        verbose_name_plural = verbose_name
    def Date(self):
        return smart_unicode(self.date)
    def Australian_Bond(self):
        return smart_unicode(self.australian_bond)
    def American_Bond(self):
        return smart_unicode(self.american_bond)
    def Scraper_Working(self):
        return smart_unicode(self.scraper_working)
