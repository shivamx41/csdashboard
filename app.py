from flask import Flask,render_template, request,redirect,url_for 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from plotly import graph_objs as go
import plotly
import plotly.express as px
import json
# import streamlit as st
# from plotly import express as px

app = Flask(__name__)
data =pd.read_csv("inningsI.csv")
data1 =pd.read_csv("inningsII.csv")

@app.route('/')
def Index():
        df = data.groupby(["batsman"],as_index=False).sum()
        
        df1 = data1.groupby(["batsman"],as_index=False).sum()
       
        df2 = data.groupby(["HOWOUTS"],as_index=False).count()
        df3 = data1.groupby(["HOWOUTS"],as_index=False).count()
        
        df4 = data.groupby(["over_num"],as_index=False).sum()
        df5 = data1.groupby(["over_num"],as_index=False).sum()
        
        df6 = data.groupby(["bowler"],as_index=False).sum()
        df7 = data1.groupby(["bowler"],as_index=False).sum()
        
        df8 = data.groupby(["batsman","bowler"],as_index=False).sum()
        df9 = data1.groupby(["batsman","bowler"],as_index=False).sum()
        # return render_template("demo.html",inn1_batsman = inn_1_labels,inn1_runs = inn_run_1,
        #                        inn2_batsman = inn_2_labels, inn2_runs=inn_run_2)
        
# saving the dataframe
        
        df.to_csv('inn1_bar_batsmanrun.csv')
        df1.to_csv('inn2_bar_batsmanrun.csv')
        df2.to_csv('inn1_howout.csv')
        df3.to_csv('inn2_howout.csv')
        df4.to_csv('run_overs_1.csv')
        df5.to_csv('run_overs_2.csv')
        df6.to_csv('bowler_vertbar1.csv')
        df7.to_csv('bowler_vertbar2.csv')
        df8.to_csv('wagon_bat_bowl_partner1.csv')
        df9.to_csv('wagon_bat_bowl_partner2.csv')
        
        return render_template("dashboard.html")
@app.post('/wagon1')
def wagonwheel1():
        batsman1 = request.form['batsman1']
        bowler1 = request.form['bowler1']
        # print(batsman,bowler)
        df = data
        df= df[(df['batsman'] == batsman1 ) & (df["bowler"] == bowler1)]
        df11 = df.groupby(["run"],as_index=False).sum()
        df1 = df.groupby(["batsman","bowler"],as_index=False).sum()
       
        df11.to_csv('wagon1runs.csv')
        df1.to_csv('wagon.csv')
   
        return render_template('dashboard.html')
@app.post('/wagon2')
def wagonwheel2():
        
        batsman2 = request.form['batsman2']
        bowler2 = request.form['bowler2']
        df2 = data1
        df2= df2[(df2['batsman'] == batsman2 ) & (df2["bowler"] == bowler2)]
        df21 = df2.groupby(["run"],as_index=False).sum()
        df2 = df2.groupby(["batsman","bowler"],as_index=False).sum()
       
        df21.to_csv('wagon2runs.csv')
        df2.to_csv('wagon2.csv')
        return render_template('dashboard.html')
       
@app.route('/chartjsdemo')
def chjs():
    return render_template("demo.html")
@app.route('/dashboard')
def charts():
        #Accenture batsman barchart
        df = data.groupby(["batsman"],as_index=False).sum()
        labels = df["batsman"]
        size = df["run"]
        fig = px.bar(x=labels, y=size, height=400)
        fig.layout.update(title_text='ACCENTURE BATSMAN WITH RUNS')
        acc_bar_plot = json.dumps(fig,cls= plotly.utils.PlotlyJSONEncoder)
        
        # Royal enfield batsman barchart
        df2  = data1.groupby(["batsman"],as_index=False).sum()
        labels = df2["batsman"]
        size = df2["run"]
        fig = px.bar(x=labels, y=size, height=400)
        fig.layout.update(title_text='ROYALENFIELD BATSMAN WITH RUNS')
        re_bar_plot = json.dumps(fig,cls= plotly.utils.PlotlyJSONEncoder)
        
        #Innings I Wickets
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Overs'], y=data['run'], name="ACCENTURE RUNS"))
        # fig.add_trace(go.Scatter(x=data1['Overs'], y=data1['run'], name="ROYALENFIELD"))
        fig.add_trace(go.Scatter(x=data['Overs'], y=data['wickets'], name="WICKETS"))
        fig.layout.update(title_text='Wickets Timeseries For ACCENTURE', xaxis_rangeslider_visible=True)
        acc_wicket_plot = json.dumps(fig,cls= plotly.utils.PlotlyJSONEncoder)
        
        #Innings II Wickets
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data1['Overs'], y=data1['run'], name="ROYALENFIELD RUNS"))
        # fig.add_trace(go.Scatter(x=data1['Overs'], y=data1['run'], name="ROYALENFIELD"))
        fig.add_trace(go.Scatter(x=data1['Overs'], y=data1['wickets'], name="WICKETS"))
        fig.layout.update(title_text='Wickets Timeseries For ROYAL ENFIELD', xaxis_rangeslider_visible=True)
        re_wicket_plot = json.dumps(fig,cls= plotly.utils.PlotlyJSONEncoder)
        
        
        #Innings I Howout
        fig = px.scatter(data, x="howout", y="Overs", color="HOWOUTS", symbol="HOWOUTS")
        fig.layout.update(title_text='ACCENTURE TEAM WICKETS', xaxis_rangeslider_visible=True)
        acc_howout = json.dumps(fig,cls= plotly.utils.PlotlyJSONEncoder)
        
        #innings II Howout
        fig = px.scatter(data1, x="howout", y="Overs", color="HOWOUTS", symbol="HOWOUTS")
        fig.layout.update(title_text='ROYALENFIELD TEAM WICKETS', xaxis_rangeslider_visible=True)
        re_howout = json.dumps(fig,cls= plotly.utils.PlotlyJSONEncoder)
       
            
        return render_template("index.html",acc_bar = acc_bar_plot ,re_bar = re_bar_plot,acc_wicket = acc_wicket_plot,
                               re_wicket = re_wicket_plot, acc_howout = acc_howout,
                               re_howout = re_howout)
        # return render_template("index.html")
    

if __name__ == '__main__':
    app.run(debug = True)