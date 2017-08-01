# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/ubuntu/venv/lib/python2.7/site-packages')
import MySQLdb as mdb
import datetime
import os
import keys_script

class updatedb:
    def __init__(self):
        self.con = self.connect()
    def connect(self):
        return mdb.connect(keys_script.HOST,keys_script.USER,keys_script.PASSWORD,keys_script.NAME,use_unicode=True,charset="utf8mb4")
    def getPrice(self,table):
        with self.con:
            cur = self.con.cursor()
            cmd = "SELECT value FROM {0}".format(table)
            cur.execute(cmd)
            lastpairprice = cur.fetchall()[-1][0]
        return lastpairprice
    def getLastValue(self,field,table):
        with self.con:
            cur = self.con.cursor()
            cmd = "SELECT {0}".format(field)
            cmd = cmd + " FROM {0}".format(table)
            cur.execute(cmd)
            lastpairvalue = cur.fetchall()[-1][0]
        return lastpairvalue
    def getLastValueUsingField(self,table,column,value):
        with self.con:
            cur = self.con.cursor(mdb.cursors.DictCursor)
            cmd = "SELECT * FROM {0} WHERE {1} = '{2}'".format(table,column,value)
            cur.execute(cmd)
            data = cur.fetchall()
            if data != ():
                data = data[-1]
            else:
                data = {}
        return data
    def getAllValuesUsingField(self,table,column,value):
        with self.con:
            cur = self.con.cursor(mdb.cursors.DictCursor)
            cmd = "SELECT * FROM {0} WHERE {1} = '{2}'".format(table,column,value)
            cur.execute(cmd)
            data = cur.fetchall()
        return data
    def getValues(self,field,table):
        with self.con:
            cur = self.con.cursor()
            cmd = "SELECT {0}".format(field)
            cmd = cmd + " FROM {0}".format(table)
            cur.execute(cmd)
            values = [value[0] for value in cur.fetchall()]
        return values
    def getAllValues(self,table):
        with self.con:
            cur = self.con.cursor()
            cmd = "SELECT * FROM {0}".format(table)
            cur.execute(cmd)
            values = cur.fetchall()
        return values
    def update(self,columns,table,*args):
        with self.con:
            cur = self.con.cursor()
            string = "INSERT INTO " + str(table)
            #print string
            variables = ["%s"]*len(args)
            variables = ",".join(variables)
            variables = "("+variables+")"
            cmd = string + columns + " VALUES " + variables
            #print cmd
            cur.execute(cmd,args)
    def remove(self,table):
        with self.con:
            cur = self.con.cursor()
            cmd = "TRUNCATE TABLE {0}".format(table)
            cur.execute(cmd)        
    def checkifexists(self,table,column,value):
        with self.con:
            cur = self.con.cursor(mdb.cursors.DictCursor)
            cmd = "SELECT * FROM {0} WHERE {1} = '{2}'".format(table,column,value)
            cur.execute(cmd)
            results = cur.fetchone()
            if results:
                return True,results
            else:
                return False,False
    def editrecord(self,table,column,value,columns,args):
        with self.con:
            cur = self.con.cursor()
            stringlist = []

            for column in columns:
                string = "Set %s " % column + "= '%s'" 
                stringlist.append(string)
            string = " ".join(stringlist)
            cmd = "UPDATE {0} ".format(table)
            cmd = cmd + string + " WHERE {0} = '{1}'".format(column,value)
            cmd = "UPDATE {0} SET ".format(table)
            cmd = cmd % args
            cur.execute(cmd)
    def showTables(self):
        with self.con:
            cur = self.con.cursor()
            cmd = "SHOW TABLES"
            cur.execute(cmd)
            print cur.fetchall()
    def deleteRecord(self,table,column,value):
        with self.con:
            cur = self.con.cursor()
            cmd = "DELETE FROM {0} WHERE {1} = '{2}'".format(table,column,value)
            cur.execute(cmd)
db_obj = updatedb()
db_obj.showTables()

#table = "data_unworkingstocks"
#stock = "example2"
#db_obj.deleteRecord(table,"stock",stock)

#table = "data_guru_and_dividends"
#print db_obj.getLastValueUsingField(table,"stock","MSFTd")

#table = "data_bonds"
#print db_obj.getLastValue("american_bond",table)
