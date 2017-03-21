from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import simplejson as json

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
	payload = {'date.gte': '20170101', 'ticker': app.vars['stock_name'], 'api_key': app.api_key}
	r = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?', params=payload)
	app.url = r.url

	columns = []

	for ii in range(len(r.json()['datatable']['columns'])):
		columns.append(r.json()['datatable']['columns'][ii]['name'])
	df = pd.DataFrame(r.json()['datatable']['data'], columns=columns)
	df = df.set_index(pd.DatetimeIndex(df['date']))
	date = df.ix[0, 'date']
	name = df.ix[0, 'ticker']
	open_price = df.ix[0, 'open']

	return render_template('ticker_plot.html', name=name, date=date, open_price=open_price)


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
  #app.run(port=33507)
