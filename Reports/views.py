from turtle import color
from urllib.request import Request
from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd


#https://www.kaggle.com/code/kanncaa1/plotly-tutorial-for-beginners/notebook
'''
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
   database="imageauditor"
)

mycursor = mydb.cursor()
 mycursor.execute("select * from auth_user")

    for x in mycursor:
        print(x)

'''
import pyodbc 

con = pyodbc.connect('Driver={SQL Server};'
                      'Server=LHR-TCH-USMAN;'
                      'Database=SocialCRM_JAZZ_V3;'
                      'Trusted_Connection=yes;')

def connect(query):
    cursor = con.cursor()
    print('Connection to db successful')
    #cmd = (query)
    #results = cursor.execute(cmd).fetchall()
    df = pd.read_sql(query, con)
    return df



def home(request):
    df=connect('SELECT * FROM PostsTwitter')
    total_posts=df.shape[0]
    print("total_posts",total_posts)
    datacolumns=df.columns
    if request.method=="POST":
        From=request.POST['startDate']
        To=request.POST['endDate']
        #    From = "2022-01-17"
        #    To = "2022-01-25"
        print(From,To)
        query = f"SELECT * FROM PostsTwitter where CreatedDate >= '{From}' AND CreatedDate <= '{To}'"
        print(query)
        df=connect(query)
        print(df)
        #df = df[(df['CreatedDate'] >= From) & (df['CreatedDate'] <= To)]
        print("df",df.shape[0])
        
    #    2022-01-17 11:49:21.000
    #    2022-01-25 18:23:00.000
    #    for column in data:
    #             if column=="sentiment"
    #                 counts=dataset[column].value_counts()
    #    Pos=counts['Positive']
    #    Neg=counts['Negative']
    #    Neu=counts['Neutral']
        x=['Created Date']
        y=[df.shape[0]]
        fig1 = go.Bar(x=x, y=y,name="Sentiment Analysis",marker_color=['green'])
        #fig2 = go.Pie(labels=x, values=y,name="Sentiment Analysis",marker=dict(colors=['green']))
        #fig2 = px.pie(values=y, names=x)
        layout = {
            'title': 'Data From Selected Dates',
            'xaxis_title': 'Dates',
            'yaxis_title': 'values',
            'height': 400,
            'width': 500,
        }
        bar_div=plot({'data':fig1,'layout': layout},output_type='div')
        #pie_div=plot({'data':fig2,'layout': layout},output_type='div')
        
        context={'bar_div':bar_div}
        return render(request, 'admin.html',context)
    x=['Total Posts']
    y=[total_posts]
    layout = {
               'title': 'Tweeter Posts Count',
                'xaxis_title': 'Posts',
                'yaxis_title': 'count',
                'height': 400,
                'width': 500,
           }
    fig = go.Bar(x=x, y=y,name="Tweeter Posts Count",marker_color=['green'])
    Tweets_div=plot({'data':fig,'layout': layout},output_type='div')
    return render(request, 'admin.html',context={'datacolumns':datacolumns,'Tweets_div':Tweets_div})