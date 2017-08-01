from django.contrib import admin

# Register your models here.

from .models import stocks,stocks_names,unworkingStocks,bannedStocks,guru_and_dividends,bonds,stocksLastData

class stocksAdmin(admin.ModelAdmin):
    class Meta:
        model = stocks
    list_display = ["__unicode__","dates","scraperErrors","scraperApis","bookValues","debtEquitities",
                    "priceEarnings","operatingCashFlows","leveredCashFlows","priceEarningGrowths","roics",
                    "capitalMarkets","freeCashFlows","freeCashFlowPercents","exchanges","names","prices",
                    "dcf_values","safety_margins"]
class latestStocksAdmin(admin.ModelAdmin):
    class Meta:
        model = stocksLastData
    list_display = ["__unicode__","dates","scraperErrors","scraperApis","bookValues","debtEquitities",
                    "priceEarnings","operatingCashFlows","leveredCashFlows","priceEarningGrowths","roics",
                    "capitalMarkets","freeCashFlows","freeCashFlowPercents","exchanges","names","prices",
                    "dcf_values","safety_margins"]
class stocksnamesAdmin(admin.ModelAdmin):
    class Meta:
        model = stocks_names
    list_display = ["__unicode__","dates","locations"]
class unworkingStocksAdmin(admin.ModelAdmin):
    class Meta:
        model = unworkingStocks
    list_display = ["__unicode__","dates"]
class bannedStocksAdmin(admin.ModelAdmin):
    class Meta:
        model = bannedStocks
    list_display = ["__unicode__","dates"]
class guruAndDividensAdmin(admin.ModelAdmin):
    class Meta:
        models = guru_and_dividends
    list_display = ["stocks","dates","cost_of_capitals","dividends","dividends_five_years","intrinsic_values","safety_margins"]
class bondAdmin(admin.ModelAdmin):
    class Meta:
        models = bonds
    list_display = ["Date","Australian_Bond","American_Bond","Scraper_Working"]

admin.site.register(stocks,stocksAdmin)
admin.site.register(stocksLastData,latestStocksAdmin)
admin.site.register(stocks_names,stocksnamesAdmin)
admin.site.register(unworkingStocks,unworkingStocksAdmin)
admin.site.register(bannedStocks,bannedStocksAdmin)
admin.site.register(guru_and_dividends,guruAndDividensAdmin)
admin.site.register(bonds,bondAdmin)

