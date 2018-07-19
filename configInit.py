import configparser

config=configparser.ConfigParser()
config['ChoprasWebExtract']={}
config['ChoprasWebExtract']['custompythonpath']="D:\\ChoprasWebExtract\\AutoCourseInfoExtract"


config['ChoprasSharedServer']={}
config['ChoprasSharedServer']['host']="172.16.70.64"
config['ChoprasSharedServer']['database']="Chopras_WebExtract"
config['ChoprasSharedServer']['user']="postgres"
config['ChoprasSharedServer']['password']="Brillio@1117"



with open('D:\\ChoprasWebExtract\\AutoCourseInfoExtract\\webExtract.ini','w') as configfile:
    config.write(configfile)



