import  os
import  json
import  psycopg2
from    .PostgresHelper    import  postgresHelper



class exportCrawledLink:

    def __init__(self):
        pass

    
    def exportCrawledLinkToFile(self,fileName,pageCrawledName):
        
        with open(os.path.join(os.path.dirname(__file__),"\\ChoprasWebExtract\\AutoCourseInfoExtract\\AutoCourseInfo_Export\\UniversityCrawledFiles\\"+fileName),"a+")   as  f:
            f.seek(0,0)
            line_found=any(pageCrawledName in line for line in f)
            if  not  line_found:
                f.seek(0, os.SEEK_END)                        
                f.write("\n"+pageCrawledName+"\n")              

    def exportCrawledLinkToDatabase(self,parentID,childID,responseData,ParentURL,ChildURL,UniversityID):
        #create a json object with parent and child id relation.
        dataToStore={}
        dataToStore['ParentKey']=parentID
        dataToStore['ChildKey']=childID 
        dataToStore['ParentURL']=ParentURL
        dataToStore['ChildURL']=ChildURL       
        dataToStore['Data']=responseData.decode("utf-8","ignore").replace('\n', '').replace('"','\'')#replace('\n', '') ##str(responseData).replace("\\n","")
        jsonData=json.dumps(dataToStore)


        post=postgresHelper()
        post.connect()

        query =  """INSERT INTO "ChoprasData"."ScrapedData"("ParentID","ChildID","JsonData","ParentURL","ChildURL","UniversityID") VALUES(%s,%s,%s,%s,%s,%s)"""
        
        
        try:
            # push jsonData to db
            post.cursor.execute(query, (parentID,None if childID=="None" else childID,jsonData,ParentURL,ChildURL,UniversityID))
            post.connection.commit()

        except  (Exception, psycopg2.DatabaseError) as error:
            #TO DO: log exception to database.
            print(error)        
        
        post.cursor.close()
        post.closeConnection()
        
        

    def exportBeautifulSoupData(self,dataToWrite,fileName,pageCrawledName): 
        with open(os.path.join(os.path.dirname(__file__),"\\ChoprasWebExtract\\AutoCourseInfoExtract\\AutoCourseInfo_Export\\UniversityCrawledFiles\\"+fileName),"a+")   as  f:
            f.seek(0,0)
            f.write(dataToWrite)
            #line_found=any(pageCrawledName in line for line in f)
            """ if  not  line_found:
                f.seek(0, os.SEEK_END)                        
                f.write("\n"+pageCrawledName+"\n") """