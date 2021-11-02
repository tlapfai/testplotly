# testplotly

https://dash.plotly.com/basic-callbacks

from django.shortcuts import render

from plotly.offline import plot
import plotly.graph_objs as go

import dash_core_components as dcc
import dash_html_components as html

from django_plotly_dash import DjangoDash
#from dash import dcc, html

import plotly.express as px

import QuantLib as ql



def index(request):

    strike = 100.0
    maturity = ql.Date(15,12,2021)
    option_type = ql.Option.Call

    payoff = ql.PlainVanillaPayoff(option_type, strike)
    #binaryPayoff = ql.CashOrNothingPayoff(option_type, strike, 1)

    europeanExercise = ql.EuropeanExercise(maturity)
    europeanOption = ql.VanillaOption(payoff, europeanExercise)

    today = ql.Date().todaysDate()
    riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
    dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
    volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), 0.1, ql.Actual365Fixed()))
    a = ql.SimpleQuote(110)
    initialValue = ql.QuoteHandle(a)
    process = ql.BlackScholesMertonProcess(initialValue, dividendTS, riskFreeTS, volatility)

    engine = ql.AnalyticEuropeanEngine(process)
    europeanOption.setPricingEngine(engine)
    
    x_data = list(range(80, 120+1))
    y_data = []
    for x in x_data:
        a.setValue(x)
        y = float(europeanOption.gamma())*1000000
        y_data.append(y)
        
    data1 = go.Scatter(x=x_data, y=y_data, mode='lines', name=f'Strike={str(strike)}', opacity=0.8, marker_color='green')
    
    payoff = ql.PlainVanillaPayoff(option_type, 105)
    europeanOption = ql.VanillaOption(payoff, europeanExercise)
    europeanOption.setPricingEngine(engine)
    y_data2 = []
    for x in x_data:
        a.setValue(x)
        y = float(europeanOption.gamma())*1000000
        y_data2.append(y)
    data2 = go.Scatter(x=x_data, y=y_data2, mode='lines', name=f'Strike={str(110)}', opacity=0.8, marker_color='red')
    
       
    #------------------------------
    dataPx = px.scatter(x=x_data, y=y_data)
    dataPx2 = px.scatter(x=x_data, y=y_data2)
    app = DjangoDash('gamma_curve')
    #app = dash.Dash()
    app.layout = html.Div([ html.H1(children='Gamma Plot', style={'textAlign':'center'}), 
            dcc.Graph(id="gamma_graph_id", figure=dataPx), 
            html.Table([html.Thead(html.Tr([html.Th("A"), html.Th("B"), html.Th("C")]))], id="gamma_table",
                style = {"border" : "1px solid black", "width" : "100%"})
            ], 
        className = "gamma_plot", 
        style = { "width" : "50%" }
        )
        
    #plot_div = plot([data1, data2], output_type='div')
    
    #return render(request, "index.html", context={'plot_div': plot_div})
    return render(request, "myplotly/index.html")
    
    
-------------------------

{%load plotly_dash%}

<!DOCTYPE html>
<html>
    <head>
        <title>I come from template inside!!</title>
		{% plotly_header %}
    </head>
    <body>
		ABC<br>
		
		
		{%plotly_direct name="gamma_curve" %}<br>
		DEF<br>
		
    </body>
	{% plotly_footer %}
</html>
