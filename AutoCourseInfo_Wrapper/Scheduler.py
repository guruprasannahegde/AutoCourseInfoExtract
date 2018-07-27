from apscheduler.schedulers.twisted import TwistedScheduler
from scrapy.utils.project import get_project_settings
from    threading   import  Thread
import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
from scrapy import log, signals
import importlib

class scheduler():

    def __init__(self):
        self.modulePath="AutoCourseInfo_Scrapy.CourseInfoExtract.CourseInfoExtract.spiders."
        self.sched = TwistedScheduler()
        self.process = CrawlerRunner(get_project_settings())

    def addJob(self,spiderModulePath,spiderClass,scheduleTime):
        # Create Spider Object dynamically by importing module.
        try:
            module=self.modulePath+spiderModulePath
            module=importlib.import_module(module)
            class_ = getattr(module, spiderClass)
            instance = class_()
            self.sched.add_job(self.process.crawl, 'date', args=[instance], run_date=scheduleTime)
            
        except(Exception) as error:
            print(error)

    def runJob(self):
        try:            
            self.sched.start()                          
            d=self.process.join()            
            d.addBoth(lambda _:reactor.stop())                        
            reactor.run()
            
        except(Exception) as error:
            print(error)
