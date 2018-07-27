import configparser
import sys
import importlib
import os
config=configparser.ConfigParser()
config.read('webExtract.ini')
sys.path.append(config['ChoprasWebExtract']['custompythonpath'])




import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
import logging
from apscheduler.schedulers.twisted import TwistedScheduler
from scrapy.utils.project import get_project_settings
from scrapy import log, signals
from    threading   import  Thread




from InteractUser  import interactUser
from Scheduler   import scheduler 

     # Get the university list from db.
    # Take the input from the as a choice of university with available scheduling time
    
interact=interactUser()

#read schedule time from db
spiderPath=interact.getUniversityScheduledTime()


#following =involves user selection.
#universityList=interact.getUniversityList()
#spiderPath=interact.getUniversityChoice(universityList)
        

    
schedule=scheduler()


for x   in  spiderPath.items():
    spiderModulePath=x[0].split('.')[0]
    spiderClass=x[0].split('.')[1]
    schedule.addJob(spiderModulePath,spiderClass,x[1])
    
    


schedule.runJob()
        
    


    
""" process = CrawlerProcess()
process.crawl(uToronto.UtorontoSpider)
process.start() """





#logging.basicConfig(filename='Log.txt',level=logging.DEBUG)
""" runner = CrawlerRunner()

d = runner.crawl(uToronto.UtorontoSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run()
13 """


