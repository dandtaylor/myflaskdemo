from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import numpy as np
#import simplejson as json

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.charts import TimeSeries
#from bokeh.resources import CDN

app = Flask(__name__)

app.vars = {}
app.api_key = 'swyvAF4r6aUr5ZpLCube'

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/ticker_plot', methods=['POST'])
def plot_result():
	app.vars['stock_name'] = request.form['stock_name']
	payload = {'date.gte': '20170101', 'ticker': app.vars['stock_name'],
                'api_key': app.api_key}
	r = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?',
                    params=payload)
	app.url = r.url

	columns = []

	for ii in range(len(r.json()['datatable']['columns'])):
		columns.append(r.json()['datatable']['columns'][ii]['name'])
	df = pd.DataFrame(r.json()['datatable']['data'], columns=columns)
	df = df.set_index(pd.DatetimeIndex(df['date']))
	date = df.ix[0, 'date']
	name = df.ix[0, 'ticker']
	open_price = df.ix[0, 'open']

	p = figure(x_axis_type='datetime', title='Closing prices for %s' % app.vars['stock_name'].upper(), 
				plot_width=500, plot_height=500)
	p.grid.grid_line_alpha = 0.3
	p.xaxis.axis_label = 'Date'
	p.yaxis.axis_label = 'Closing Price'
	p.line(np.array(df['date'], dtype=np.datetime64), df['close'], color='red')

	script, div  = components(p)

	return render_template('ticker_plot.html', name=name, date=date,
                            open_price=open_price, plot_script=script, plot_div=div)


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
  #app.run(port=33507)
