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

def home(request):
    dataset=pd.read_csv("static\R_U_Dataset.csv")
    datacolumns=dataset.columns
    print("datacolumns",datacolumns)
    if request.method=="POST":
           data=request.POST.getlist('listcolumns')
           for column in data:
                      if column=="sentiment":
                                 counts=dataset[column].value_counts()
           Pos=counts['Positive']
           Neg=counts['Negative']
           print("Neg",Neg)
           Neu=counts['Neutral']
           x=['Positive','Negative','Neutral']
           y=[Pos,Neg,Neu]
           fig = go.Bar(x=x, y=y,name="Sentiment Analysis",marker=dict(color='green'))
           layout1 = {
               'title': 'Sentiment Analysis',
                'xaxis_title': 'labels',
                'yaxis_title': 'values',
                'height': 420,
             'width': 560,
           }
           bar_div=plot({'data':fig,'layout': layout1},output_type='div')
           return render(request, 'admin.html',context={'bar_div':bar_div})
    """ 
    View demonstrating how to display a graph object
    on a web page with Plotly. 
 
    data=pd.read_csv("static\R_U_Dataset.csv")
    datacolumns=data.columns
    print("datacolumns",datacolumns)
    #df=pd.DataFrame(df)
    """
    
        #df=pd.DataFrame(data)
    #fig = px.bar(x=Positive, y=Negative,z=Neutral)
    # Generating some data for plots.
    x = [i for i in range(0, 11)]
    #print("x",x)
    y1 = [3*i for i in x]
    #print("y1",y1)
    y2 = [i**2 for i in x]
    #print("y2",y2)
    y3 = [10*i for i in x]
    #print("y3",y3)

    # List of graph objects for figure.
    # Each object will contain on series of data.
    graphs = []

    # Adding linear plot of y1 vs. x.
    graphs.append(
        go.Scatter(x=x, y=y1, mode='lines', name='Line y1')
    )

    # Adding scatter plot of y2 vs. x. 
    # Size of markers defined by y2 value.
    graphs.append(
        go.Scatter(x=x, y=y2, mode='markers', opacity=0.8, 
                   marker_size=y2, name='Scatter y2')
    )

    # Adding bar plot of y3 vs x.
    graphs.append(
        go.Bar(x=x, y=y3, name='Bar y3')
    )

    # Setting layout of the figure.
    layout = {
        'title': 'Title of the figure',
        'xaxis_title': 'X',
        'yaxis_title': 'Y',
        'height': 420,
        'width': 560,
    }


    # Getting HTML needed to render the plot.
    plot_div = plot({'data': graphs, 'layout': layout}, 
                    output_type='div')

 
    return render(request, 'admin.html',context={'plot_div':plot_div,'datacolumns':datacolumns})



def Graph(request):
    data=request.POST.getlist('listcolumns')
    dataset=pd.read_csv("static\R_U_Dataset.csv")
    for column in data:
        if column=="sentiment":
            counts=dataset[column].value_counts()
    counts=Pos=counts['Positive']

    Neg=counts['Negative']
    print("Neg",Neg)
    Neu=counts['Neutral']
    x=['Positive','Negative','Neutral']
    y=[Pos,Neg,Neu]
    
    return render(request, 'base.html',context={})