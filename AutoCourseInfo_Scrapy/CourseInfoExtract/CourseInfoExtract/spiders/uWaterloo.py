import configparser
import sys
import scrapy
import logging
import os
import  inspect
import  uuid
config=configparser.ConfigParser()
config.read("webExtract.ini")
sys.path.append(config["ChoprasWebExtract"]["custompythonpath"])

from bs4                              import BeautifulSoup
from urllib.request                   import urlopen
from urllib.parse                     import urlparse
from AutoCourseInfo_Export.ExportData import exportCrawledLink


class UwaterlooSpider(scrapy.Spider):
    name                    = "uOfWaterloo"
    universityParentSite    = "https://uwaterloo.ca/"
    allowed_domains         = ["www.uwaterloo.ca"]
    start_urls              = ["http://uwaterloo.ca/"]
    secondStageCrawledLinks = [] 
    
    stageCount=0
    
    
    ParentID=uuid.uuid4()
    ChildID=None



    def parse(self, response):
        self.createNestedRelation(response)
        self.ChildID=uuid.uuid4()
        print("Started Parsing"+self.universityParentSite)
        for url in response.xpath('//a[contains(@href,"/future-students")]/@href').extract():
            if "http" not in url:
                exportCrawledLink.exportCrawledLinkToFile(self,"UOfWaterloo.txt",self.universityParentSite+url)
                yield scrapy.Request(url=self.universityParentSite+url,callback=self.parse,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":self.universityParentSite+url}})
            else:
                
                exportCrawledLink.exportCrawledLinkToFile(self,"UOfWaterloo.txt",url)
                yield scrapy.Request(url=url,callback=self.parse,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":url}})  
         
           

    def parseUOfWaterlooSecondStageCrawling(self,response):
        
        self.createNestedRelation(response)
        for url in response.xpath('//a[contains(@href,"/academics")]/@href').extract():
            if "http" not in url:
                exportCrawledLink.exportCrawledLinkToFile(self,"UOfWaterloo.txt",self.universityParentSite+url)
                                       
                yield scrapy.Request(self.universityParentSite+url,callback=self.parseUOfWaterlooThirdStageCrawling,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":self.universityParentSite+url}})
                
            else:
                exportCrawledLink.exportCrawledLinkToFile(self,"UOfWaterloo.txt",url)
                              
                yield scrapy.Request(url,callback=self.parseUOfWaterlooThirdStageCrawling,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":url}})

        #self.parseUOfTorontoThirdStageCrawling(self.secondStageCrawledLinks)   
        
    def parseUOfWaterlooThirdStageCrawling(self,response):


        self.createNestedRelation(response)

        academicsRegExp='//a[contains(@href,"/academics")]/@href'
        undergradRegExp='//a[contains(@href,"/progs")]/@href'
        gradRegExp='//a[contains(@href,"/Pages/Programs")]/@href'

        academicsExtract=response.xpath(academicsRegExp).extract()
        gradExtract=response.xpath(gradRegExp).extract()        
        undergradExtract=response.xpath(undergradRegExp).extract()
        
        for url in academicsExtract:
            if "http" not in url:
                exportCrawledLink.exportCrawledLinkToFile(self,"UOfWaterloo.txt",self.universityParentSite+url)                
                yield scrapy.Request(self.universityParentSite+url,callback=self.parseUOfWaterlooThirdStageCrawling,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":self.universityParentSite+url}})                                               
            else:
                exportCrawledLink.exportCrawledLinkToFile(self,"UOfWaterloo.txt",url)                
                yield scrapy.Request(url,callback=self.parseUOfWaterlooThirdStageCrawling,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":url}})                            
                
        
        for url in  undergradExtract:
            
            exportCrawledLink.exportCrawledLinkToFile(self,"UOfWaterloo.txt",url)
            yield scrapy.Request(url,callback=self.parseUOfWaterlooThirdStageCrawling,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":url}})   
        
        for url in gradExtract:
            
            exportCrawledLink.exportCrawledLinkToFile(self,"UOfWaterloo.txt",url)
            yield scrapy.Request(url,callback=self.parseUOfWaterlooThirdStageCrawling,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":url}})


    """ def scrapTheDataFromCrawledLink(self,url):
        html=urlopen(url)
        res=BeautifulSoup(html.read(),"html5lib")
        tags=res.findAll("td")
        for tag in tags:
            if  tag.get_text().find("Application deadlines"):
           
                exportCrawledLink.exportBeautifulSoupData(self,res.get_text(),os.path.split((urlparse(url).path))[1]+".txt",url)   """



    def scrapTheDataFromCrawledLink(self,response,ParentID,ChildID,ParentURL,ChildURL):
        exportCrawledLink.exportCrawledLinkToDatabase(self,str(ParentID),str(ChildID),response.body,ParentURL,ChildURL,3)        


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