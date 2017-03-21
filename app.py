from flask import Flask, render_template, request, redirect

app = Flask(__name__)

app.vars = {}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
  return render_template('index.html')

@app.rout('/ticker_plot', methods=['POST'])
def plot_result():
	app.vars['stock_name'] = request.form['stock_name']
	return render_template('ticker_plot.html', name=app.vars['stock_name'])


if __name__ == '__main__':
  app.run(port=33507)
