import datetime
import sys
from os import path
import psycopg2
import configparser



config=configparser.ConfigParser()
config.read('webExtract.ini')
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
#sys.path.append(config['ChoprasWebExtract']['custompythonpath'])


from AutoCourseInfo_Export.PostgresHelper import postgresHelper
from AutoCourseInfo_Scrapy.CourseInfoExtract.CourseInfoExtract.spiders import *


class interactUser():



    def getUniversityList(self):

        #write stored procedure for faster callback to server and fro.
        post=postgresHelper()

        post.connect()
        
        query='SELECT   "UniversityName" FROM    "ChoprasData"."UniversityMaster"'
        try:
            d={}
            post.cursor.execute(query)
            res=post.cursor.fetchall()
            for x   in  range(0,res.__len__()):                
                d[x]=res[x]
               

            post.cursor.close()
            post.closeConnection()
            return d
            
        except  (Exception, psycopg2.DatabaseError) as error:
            #TO DO: log exception to database.
            post.cursor.close()
            post.closeConnection()
            print(error) 
        
    
    def getUniversityChoice(self,universityList):

        post=postgresHelper()
        post.connect()
        

        len=universityList.__len__()
        d={}
        print("\nUniversity available for scheduling :\n")
        for x   in  range(0,len):
            print(str(x)+":"+universityList[x][0]+"\n")
            d[x]=universityList[x]
        
        d[len]="All"
        print(str(len)+":"+d[len]+"\n")


        inputValue=int(input("Enter a number accordingly to select University"))
        selectedUniversityList={}
        if  inputValue==len:
            query='SELECT   "SpiderName" FROM    "ChoprasData"."UniversityMaster"'
            post.cursor.execute(query)
            d.pop(len)
            selectedUniversityList=d
        else:
            query='SELECT   "SpiderName" FROM    "ChoprasData"."UniversityMaster" WHERE "UniversityName"=%s'            
           
            post.cursor.execute(query,(d[inputValue]))
            selectedUniversityList[0]=d[inputValue]
            
            


        
        res=[row[0] for row in post.cursor.fetchall()]        
        post.cursor.close()
        post.closeConnection()
        return self.getScheduleTime(selectedUniversityList,res)
        
        

    def getScheduleTime(self,universityList,spiderPath):        
        scheduledTimeList={}
        
        for x in universityList:
            print("Choose time to run for "+universityList[x][0])
            d={}
            d[1]=datetime.datetime.today()+datetime.timedelta(seconds=60)
            d[2]=datetime.datetime.today()+datetime.timedelta(1)
            scheduleTime=int(input("1:Now\n2:Tomorrow"))
            scheduledTimeList[spiderPath[x]]=d[scheduleTime]
        return scheduledTimeList

    def getUniversityScheduledTime(self):

        post=postgresHelper()
        post.connect()
        
        query='SELECT   "UniversityName","SpiderName","ScheduledTime" FROM    "ChoprasData"."UniversityMaster"'
        try:
            
            d={}
            scheduledTimeList={}
            post.cursor.execute(query)
            res=post.cursor.fetchall()

            for x   in  range(0,res.__len__()):
                scheduledTimeList[res[x][1]]=res[x][2]                

            post.cursor.close()
            post.closeConnection()

            """ for x   in  range(0,res.__len__()):                
                d[x]=res[x] """

            
            return scheduledTimeList
            
        except  (Exception, psycopg2.DatabaseError) as error:
            #TO DO: log exception to database.
            post.cursor.close()
            post.closeConnection()
            print(error) 