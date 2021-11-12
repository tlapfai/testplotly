from django.shortcuts import render

from plotly.offline import plot
import plotly.graph_objs as go

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from django_plotly_dash import DjangoDash
#from dash import dcc, html

import plotly.express as px

import QuantLib as ql

import numpy as np


def index(request):

    strike = 100.0
    maturity = ql.Date(15,12,2021)
    option_type = ql.Option.Call

    
    #binaryPayoff = ql.CashOrNothingPayoff(option_type, strike, 1)



    
    #volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), 0.1, ql.Actual365Fixed()))
    
    

    
    

        
    #data1 = go.Scatter(x=x_data, y=y_data, mode='lines', name=f'Strike={str(strike)}', opacity=0.8, marker_color='green')
    
    # payoff = ql.PlainVanillaPayoff(option_type, 105)
    # europeanOption = ql.VanillaOption(payoff, europeanExercise)
    # europeanOption.setPricingEngine(engine)
    # y_data2 = []
    # for x in x_data:
        # a.setValue(x)
        # y = float(europeanOption.gamma())*1000000
        # y_data2.append(y)
    #data2 = go.Scatter(x=x_data, y=y_data2, mode='lines', name=f'Strike={str(110)}', opacity=0.8, marker_color='red')
    

    #------------------------------
    #dataPx = px.line(x=x_data, y=y_data, labels={'x': 'Spot', 'y': "Gamma"})
    #dataPx2 = px.line(x=x_data, y=y_data2, labels={'x': 'Spot', 'y': "Gamma"})
    app = DjangoDash('gamma_curve')
    app.layout = html.Div([ html.H4(children='Valuation', style={'textAlign':'center'}), 
                            dcc.Graph(id="gamma-graph"), 
                            html.Table([
                                html.Label('Measure'), 
                                dcc.RadioItems(id='measure', value='NPV', 
                                            options=[{'label':'NPV', 'value':'NPV'}, 
                                                    {'label':'Delta', 'value':'Delta'}, 
                                                    {'label':'Gamma', 'value':'Gamma'},
                                                    {'label':'Vega', 'value':'Vega'}]), 
                                ], 
                                style = {"border" : "1px solid skyblue", "width" : "100%" }
                                ), 
                            html.Table([
                                html.Label('Volatility'), 
                                dcc.Slider(id='vol-slider', min=1, max=20, value=5, marks={str(i):str(i) for i in range(1,21)}, step=None), 
                                ], 
                                style = {"border" : "1px solid skyblue", "width" : "100%" }
                                ),
                            html.Table([
                                html.Label('Strike'), 
                                dcc.Input(id='k-slider', type='number', value=100, min=80, max=120, step=0.01), 
                                ], 
                                style = {"border" : "1px solid skyblue", "width" : "100%" }
                                ),
                            ],
                        className = "gamma_plot", 
                        style = { "width" : "auto" }
            )
    
    today = ql.Date().todaysDate()
    riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
    dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
    europeanExercise = ql.EuropeanExercise(maturity)
    
    
    
    @app.callback(Output('gamma-graph', 'figure'), Input('measure', 'value'), Input('vol-slider', 'value'), Input('k-slider', 'value'))
    def update_figure(measure, selected_vol, selected_k):
        x_data = np.linspace(80, 120, 81)#list(range(80, 120+1))
        a = ql.SimpleQuote(110)
        initialValue = ql.QuoteHandle(a)
        payoff = ql.PlainVanillaPayoff(option_type, selected_k)
        europeanOption = ql.VanillaOption(payoff, europeanExercise)
        volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), selected_vol*0.01, ql.Actual365Fixed()))
        process = ql.BlackScholesMertonProcess(initialValue, dividendTS, riskFreeTS, volatility)
        engine = ql.AnalyticEuropeanEngine(process)
        europeanOption.setPricingEngine(engine)
        
        if measure == 'NPV':
            fun = europeanOption.NPV
        elif measure == 'Delta':
            fun = europeanOption.delta
        elif measure == 'Gamma':
            fun = europeanOption.gamma
        elif measure == 'Vega':
            fun = europeanOption.vega
        
        y_data = []
        for x in x_data:
            a.setValue(x)
            y = float(fun())*1000000
            y_data.append(y)

        fig = px.line(x=x_data, y=y_data, labels={'x': 'Spot', 'y': measure})
        fig.update_layout(transition_duration=500)
        return fig
    
    #plot_div = plot([data1, data2], output_type='div')
    
    #return render(request, "index.html", context={'plot_div': plot_div})
    return render(request, "myplotly/index.html")
