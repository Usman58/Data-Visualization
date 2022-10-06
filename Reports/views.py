from asyncio.windows_events import NULL
from email import message
from multiprocessing import context
from turtle import color
from urllib.request import Request
from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
#https://www.kaggle.com/code/kanncaa1/plotly-tutorial-for-beginners/notebook


import pyodbc 

def ServerConnect(query):
    con = pyodbc.connect('Driver={SQL Server};'
                      'Server=LHR-TCH-USMAN;'
                      'Trusted_Connection=yes;')
    df = pd.read_sql(query, con)
    return df



def DBConnect(query,dbName):
    DBName=f"Database={dbName}"
    con = pyodbc.connect('Driver={SQL Server};'
                      'Server=LHR-TCH-USMAN;'
                      f"{DBName};"
                      'Trusted_Connection=yes;')

    print('Connection to db successful',DBName)
    #cmd = (query)
    #results = cursor.execute(cmd).fetchall()
    df = pd.read_sql(query, con)
    return df


dbName=None
def home(request):
    db_List = ServerConnect('SELECT * FROM sys.databases')
    db_List=db_List['name']
    if request.method=="POST":
        db_List=None
        dbName=request.POST['dbName']
        tablesList=DBConnect('SELECT * FROM information_schema.tables',dbName)
        tablesList=tablesList['TABLE_NAME']
        selected_db=dbName
        context={'tablesList':tablesList,'db_List':db_List,'selected_db':selected_db}
        return render(request, 'admin.html',context)
    
    context={'db_List':db_List}
    return render(request, 'admin.html',context)


def TableData(request):
    print("Table data")
    if request.method=="POST":
        tableName=request.POST['tableName']
        dbName=request.POST['db']
        df=DBConnect(f'SELECT * FROM {tableName}',dbName)
        df.fillna("-",inplace=True)
        Table=df.head(3)
        context={'tableName':tableName,'Table':Table,"db":dbName}
        return render(request, 'admin.html',context)


def SummarizeData(request):
    print("Summarizing data...")
    if request.method=="POST":
        dbName=request.POST['db']
        print("dbName",dbName)
        tableName=request.POST['tableName']
        print("tableName",tableName)
        #summarize_name=request.POST['name']
        #print("summarize_name",summarize_name)
        df=DBConnect(f'SELECT * FROM {tableName}',dbName)
        Table=df.describe()
        context={'Table':Table,'table':tableName,'db':dbName}
        return render(request,'SummarizeDashboard.html',context)
    return render(request, 'SummarizeDashboard.html')   
        
def VisualizeData(request):
    print("Visualizing data...")
    if request.method=="POST":
        dbName=request.POST['db']
        column=request.POST['column']
        print("dbName",dbName)
        tableName=request.POST['table']
        print("tableName",tableName)
        #summarize_name=request.POST['name']
        #print("summarize_name",summarize_name)
        df=DBConnect(f'SELECT {column} FROM {tableName}',dbName)
        Table=df.describe()
        layout = {
               'title': f'{column}',
                'xaxis_title': 'x',
                'yaxis_title': 'x',
                'height': 400,
                'width': 500,
           }
        x=[]
        y=[]
        for index, row in Table.iterrows():
            x.append(index)
            for cell in row:
                y.append(cell)
       
        print("x===>",x)         
        print("y===>",y)  

        print("describe",Table)
        fig = go.Bar(x=x, y=y,name=f"{tableName}",marker_color='green')
        bar_div=plot({'data':fig,'layout': layout},output_type='div')

        context={'Table':Table,'bar_div':bar_div}
        return render(request,'SummarizeDashboard.html',context)
    return render(request, 'SummarizeDashboard.html')   
        
    
def JoinTables(request):
    if request.method=="POST":
        tableName=request.POST['tableName']
        dbName=request.POST['db']
        print("dbNAme===>",dbName)
        tablesList=DBConnect('SELECT * FROM information_schema.tables',dbName)
        tablesList=tablesList['TABLE_NAME']
        #df=DBConnect(f'SELECT {column} FROM {tableName}',dbName)
        #df=DBConnect(f'SELECT * FROM Orders INNER JOIN Customers ON Orders.CustomerID=Customers.CustomerID',dbName)
        print("JoinTables")
        context={'tableName':tableName,'tablesList':tablesList,'db':dbName}
        return render(request, 'JoinData.html',context)
def SelectedTables(request):
    table1Name=request.POST['table1']
    dbName=request.POST['db']
    table2Name=request.POST['table2']
    print("dbNAme===>",dbName)
    table1=DBConnect(f'SELECT * FROM {table1Name}',dbName)
    table2=DBConnect(f'SELECT * FROM {table2Name}',dbName)
    table1.fillna("-",inplace=True)
    table2.fillna("-",inplace=True)
    table1=table1.columns
    table2=table2.columns
    #df=DBConnect(f'SELECT {column} FROM {tableName}',dbName)
    #df=DBConnect(f'SELECT * FROM Orders INNER JOIN Customers ON Orders.CustomerID=Customers.CustomerID',dbName)
    print("JoinTables")
    context={'table1Name':table1Name,'table2Name':table2Name,'table1':table1,'table2':table2,'db':dbName}
    return render(request, 'JoinData.html',context)

def JoinResult(request):
    print("request.POST",request.POST)
    table1coulmn=request.POST['table1coulmn']
    table2column=request.POST['table2coulmn']
    table1Name=request.POST['table1Name']
    table2Name=request.POST['table2Name']
    dbName=request.POST['db']
    print("dbNAme===>",dbName)
    #df=DBConnect(f'SELECT {column} FROM {tableName}',dbName)
    df=DBConnect(f'SELECT * FROM {table1Name} INNER JOIN {table2Name} ON {table1Name}.{table1coulmn}={table2Name}.{table2column}',dbName)
    print("JoinTables")
    df.fillna("-",inplace=True)
    Table=df.head(3)
    context={'Table':Table}
    return render(request, 'JoinData.html',context)

def FiltersPage(request):
    table=request.POST['tableName']
    dbName=request.POST['db']
    df=DBConnect(f'SELECT * FROM {table}',dbName)
    columns=df.columns
    context={'table':table,'db':dbName,'columns':columns}
    return render(request, 'FiltersPage.html',context)
    
def FiltersDataByDate(request):
        column=request.POST['column']
        From=request.POST['startDate']
        From=pd.to_datetime(From)
        To=request.POST['endDate']
        dbName=request.POST['db']
        table=request.POST['table']
        To=pd.to_datetime(To)
        print(From,To)
        query = f"SELECT {column} FROM {table} where CreatedDate >=  '{From}' AND CreatedDate <= '{To}' "
        print(query)
        df=DBConnect(query,dbName)
        df.fillna("-",inplace=True)
        columns=df.columns
        Table=df.head(5)
        context={'Table':Table,'columns':columns,'table':table,'db':dbName}
        return render(request, 'FiltersPage.html',context)

 