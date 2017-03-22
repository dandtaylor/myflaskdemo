import requests
import pandas as pd


#from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.charts import TimeSeries
#from bokeh.resources import CDN

api_key = 'swyvAF4r6aUr5ZpLCube'
app_vars = {}
app_vars['stock_name'] = 'MSFT'
payload = {'date.gte': '20170101', 'ticker': app_vars['stock_name'],
           'api_key': api_key}
r = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?',
                    params=payload)
url = r.url
print(url)

columns = []
for ii in range(len(r.json()['datatable']['columns'])):
	columns.append(r.json()['datatable']['columns'][ii]['name'])
df = pd.DataFrame(r.json()['datatable']['data'], columns=columns)
df = df.set_index(pd.DatetimeIndex(df['date']))
date = df.ix[0, 'date']
name = df.ix[0, 'ticker']
open_price = df.ix[0, 'open']

TOOLS = ('hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo, \
         reset,tap,save,box_select,poly_select,lasso_select')
data = dict(df=df['close'], Date=df['date'])
p = TimeSeries(data, x='Date', title="test MFST plot", ylabel='Closing Stock Prices')
script, div  = components(p)
#print(script)
#print(div)
print(df['close'])