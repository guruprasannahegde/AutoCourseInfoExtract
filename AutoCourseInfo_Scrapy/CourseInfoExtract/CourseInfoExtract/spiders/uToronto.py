# -*- coding: utf-8 -*-
import  configparser
import  sys
import  scrapy
import  logging
import  os
import  json
from    anytree import  Node,RenderTree
import  uuid
import  inspect
config=configparser.ConfigParser()
config.read("webExtract.ini")
sys.path.append(config["ChoprasWebExtract"]["custompythonpath"])


from    bs4                                 import  BeautifulSoup
from    urllib.request                      import  urlopen
from    urllib.parse                        import  urlparse
from    AutoCourseInfo_Export.ExportData    import  exportCrawledLink
from    scrapy                              import  settings
from    AutoCourseInfo_Scrapy.CourseInfoExtract import  RelationalEntities

class UtorontoSpider(scrapy.Spider):
    
    
    name                =   "uOfToronto"    
    universityParentSite=   "https://www.utoronto.ca"
    allowed_domains     =   ["www.utoronto.ca"]
    start_urls          =   ["https://www.utoronto.ca/"]
    secondStageCrawledLinks=[]    
    
    buildParentChildRelation=RelationalEntities.BuildParentChildRelation()
    
    stageCount=0
    
    
    ParentID=uuid.uuid4()
    ChildID=None

    

    def parse(self, response):
        self.createNestedRelation(response)
        print("Started Parsing"+self.universityParentSite)
        regExp="/future-students"
        futureStudentsArray=response.xpath('//a[contains(@href,"'+regExp+'")]/@href').extract()
        self.ChildID=uuid.uuid4()
        for url in futureStudentsArray:
            if "http" not in url:
                exportCrawledLink.exportCrawledLinkToFile(self,"UOfToronto.txt",self.universityParentSite+url)
                yield scrapy.Request(self.universityParentSite+url,callback=self.parseUOfTorontoSecondStageCrawling,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":self.universityParentSite+url,"regExp":regExp}})
            else:                
                exportCrawledLink.exportCrawledLinkToFile(self,"UOfToronto.txt",url)
                yield scrapy.Request(url,callback=self.parseUOfTorontoSecondStageCrawling,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":url,"regExp":regExp}})


    def parseUOfTorontoSecondStageCrawling(self,response):
        
        self.createNestedRelation(response)        
        regExp="/academics"
        for url in response.xpath('//a[contains(@href,"/academics")]/@href').extract():
            if "http" not in url:
                
                exportCrawledLink.exportCrawledLinkToFile(self,"UOfToronto.txt",self.universityParentSite+url)
                yield scrapy.Request(self.universityParentSite+url,callback=self.parseUOfTorontoThirdStageCrawling,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":self.universityParentSite+url,"regExp":regExp}})
                
            else:
                exportCrawledLink.exportCrawledLinkToFile(self,"UOfToronto.txt",url)
                yield scrapy.Request(url,callback=self.parseUOfTorontoThirdStageCrawling,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":url,"regExp":regExp}})

        


    def parseUOfTorontoThirdStageCrawling(self,response):
       
        self.createNestedRelation(response)
        academicsRegExp='//a[contains(@href,"/academics")]/@href'
        undergradRegExp='//a[contains(@href,"/progs")]/@href'
        gradRegExp='//a[contains(@href,"/Pages/Programs")]/@href'

        academicsExtract=response.xpath(academicsRegExp).extract()
        gradExtract=response.xpath(gradRegExp).extract()        
        undergradExtract=response.xpath(undergradRegExp).extract()
        
        for url in academicsExtract:
            if "http" not in url:
                exportCrawledLink.exportCrawledLinkToFile(self,"UOfToronto.txt",self.universityParentSite+url)                
                yield scrapy.Request(self.universityParentSite+url,callback=self.parseUOfTorontoThirdStageCrawling,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":self.universityParentSite+url,"regExp":academicsRegExp}})                                               
            else:
                exportCrawledLink.exportCrawledLinkToFile(self,"UOfToronto.txt",url)                
                yield scrapy.Request(url,callback=self.parseUOfTorontoThirdStageCrawling,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":url,"regExp":academicsRegExp}})                            
                
        
        for url in  undergradExtract:
            exportCrawledLink.exportCrawledLinkToFile(self,"UOfToronto.txt",url)
            yield scrapy.Request(url,callback=self.parseUOfTorontoThirdStageCrawling,dont_filter=True,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":url,"regExp":undergradRegExp}})   
        
        for url in gradExtract:
            exportCrawledLink.exportCrawledLinkToFile(self,"UOfToronto.txt",url)
            yield scrapy.Request(url,callback=self.parseUOfTorontoThirdStageCrawling,dont_filter=True,meta={'info':{"methodName":inspect.stack()[0][3],"Level":self.stageCount,"Parent":response.request.url,"ParentID":self.ChildID,"Child":url,"regExp":gradRegExp}})   
                    
        

    """ def scrapTheDataFromCrawledLink(self,url):
        html=urlopen(url)
        res=BeautifulSoup(html.read(),"html5lib")
        tags=res.findAll("td")
        for table in res.findAll('table'):
            for tr in table.findAll('tr')[1:]:
                exportCrawledLink.exportBeautifulSoupData(self,tr.get_text(),os.path.split((urlparse(url).path))[1]+".txt",url)
        #for tag in tags:
        #    if  tag.get_text().find("Application deadlines"):
                #self.log(os.path.split((urlparse(url).path))[1]) """
                
    def scrapTheDataFromCrawledLink(self,response,ParentID,ChildID,ParentURL,ChildURL):
        exportCrawledLink.exportCrawledLinkToDatabase(self,str(ParentID),str(ChildID),response.body,ParentURL,ChildURL,1)        


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

        
       
    
                    
        
        

