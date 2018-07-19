import os
import configparser
import sys
import scrapy
import uuid
import json
import  inspect

from AutoCourseInfo_Export.ExportData import exportCrawledLink 


class UarizonaSpider(scrapy.Spider):

    name                        =  "ArizonaStateUniversity"
    universityParentSite        =  "https://www.asu.edu"
    allowed_domains             =  ["www.asu.edu"]
    start_urls                  =  ["https://www.asu.edu/"]

    stageCount=0
    
    
    ParentID=uuid.uuid4()
    ChildID=None

    s1 = 'asu.edu'

    def parse(self, response):
        self.createNestedRelation(response)
        self.ChildID=uuid.uuid4()
        print("Started Parsing"+self.universityParentSite)
        for url in response.xpath('//a[contains(@href,"academics")]/@href').extract():
            if  'http' not in url:
                exportCrawledLink.exportCrawledLinkToFile(self,"ArizonaStateUniversity.txt",self.universityParentSite+url)
                yield scrapy.Request(self.universityParentSite+url, callback=self.parseofArizonaSecondStage,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":self.universityParentSite+url}})
            else:
                exportCrawledLink.exportCrawledLinkToFile(self,"ArizonaStateUniversity.txt",url)
                yield scrapy.Request(url, callback=self.parseofArizonaSecondStage,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":url}})


    def parseofArizonaSecondStage(self,response):
        self.createNestedRelation(response)
        
      
        for url in  response.xpath('//a[contains(@href,"/programs")]/@href').extract():
            if 'http' not in url:
                exportCrawledLink.exportCrawledLinkToFile(self,"ArizonaStateUniversity.txt",url)
                yield scrapy.Request(url,callback=self.parseofArizonaThirdStage,dont_filter=True,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":self.universityParentSite+url}})
            else:               
                exportCrawledLink.exportCrawledLinkToFile(self,"ArizonaStateUniversity.txt",url)
                yield scrapy.Request(url,callback=self.parseofArizonaThirdStage,dont_filter=True,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":url}})

    def parseofArizonaThirdStage(self,response):
        self.createNestedRelation(response)
        for url in response.xpath('//a[contains(@href,"/webapp4") and contains(@href,"/programs")]/@href').extract():
            if 'http' not in url:
                exportCrawledLink.exportCrawledLinkToFile(self,"ArizonaSateUniversity.txt",url)
                yield scrapy.Request(url,callback=self.parseofArizonaFourthStage, dont_filter=True ,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":self.universityParentSite+url}})
            else:
                exportCrawledLink.exportCrawledLinkToFile(self,"ArizonaStateUniversity.txt",url)
                yield scrapy.Request(url,callback=self.parseofArizonaFourthStage,dont_filter=True,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":url}})   


    def parseofArizonaFourthStage(self,response):
        self.createNestedRelation(response)
       
        undergardExtract = response.xpath('//a[contains(@href,"/programs") and contains(@href,"/undergrad")]/@href').extract()
   
    #    print (undergardExtract)
        
        gradExtract      = response.xpath('//a[contains(@href,"/programs") and contains(@href,"/graduate")]/@href').extract()
        missing_url      = 'https://webapp4.asu.edu'
       
        for url in undergardExtract:
            if 'http' not in url:
                exportCrawledLink.exportCrawledLinkToFile(self,"ArizonaStateUniversity.txt", missing_url+url)
                yield scrapy.Request(missing_url+url,callback=self.parseofArizonaFourthStage, dont_filter=True,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":self.universityParentSite+url}})
            else:
                exportCrawledLink.exportCrawledLinkToFile(self,"ArizonaStateUniversity.txt",url)
                yield scrapy.Request(url,callback=self.parseofArizonaFourthStage,dont_filter=True,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":url}})

        for url in gradExtract:
            if 'http' not in url:
               exportCrawledLink.exportCrawledLinkToFile(self,"ArizonaStateUniversity.txt",missing_url+url)
               yield scrapy.Request(missing_url+url,callback=self.parseofArizonaFourthStage,dont_filter=True,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":self.universityParentSite+url}})
            else:
                exportCrawledLink.exportCrawledLinkToFile(self,"ArizonaStateUniversity.txt",url)
                yield scrapy.Request(url,callback=self.parseofArizonaFourthStage,dont_filter=True,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":url}})


   
    def scrapTheDataFromCrawledLink(self,response,ParentID,ChildID,ParentURL,ChildURL):
        exportCrawledLink.exportCrawledLinkToDatabase(self,str(ParentID),str(ChildID),response.body,ParentURL,ChildURL,2)        



    def createNestedRelation(self,response):
        #build relation
        if(self.stageCount==0):
            self.scrapTheDataFromCrawledLink(response,self.ParentID,self.ChildID,self.universityParentSite,None)
            self.stageCount=+1    
        else:
            if  (self.stageCount==1):
                self.scrapTheDataFromCrawledLink(response,self.ParentID,self.ChildID,response.meta["info"]["Parent"],response.meta["info"]["Child"])
                self.stageCount=self.stageCount+1
            else:
                self.ParentID=response.meta["info"]["ParentID"]
                self.ChildID=uuid.uuid4()
                self.scrapTheDataFromCrawledLink(response,self.ParentID,self.ChildID,response.meta["info"]["Parent"],response.meta["info"]["Child"])                
