from flask import Flask, request, jsonify, send_file, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine
import pandas as pd
import urllib
import io
import seaborn as sns
import matplotlib.pyplot as plt

env = 'dev'
if env == "dev":
    BASE_URL = "http://localhost:5000/"
params = urllib.parse.quote_plus(
    r'Driver={ODBC Driver 17 for SQL Server};Server=tcp:7atom7.database.windows.net,1433;Database=adfolkstest;Uid=adfolks;Pwd=Atoms$41995;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine_azure = create_engine(conn_str, echo=True).connect()
#from flask_restful import Resource, Api

# Init App
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', base_url=BASE_URL)


@app.route('/totalrevenue', methods=['GET'])
def get_total_revenue_year():
    res = pd.read_sql_query(
        'select pyear,sum(qty_total) as total_qty, sum(revenue_total) as revenue_total from final_report group by pyear', engine_azure)
    return res.to_json()


@app.route('/images', methods=['GET'])
def get_image():
    res = pd.read_sql_query('select * from final_report', engine_azure)
    print(res)
    bytes_image = io.BytesIO()
    sns.set_style('darkgrid')
    plt.figure(num=None, figsize=(30, 16), dpi=80,
               facecolor='w', edgecolor='k')
    sns.barplot(x='product_name', y='qty_total', hue='pyear', data=res)
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return send_file(bytes_image, attachment_filename='graph.png', mimetype='image/png')


@app.route('/inventory', methods=['GET'])
def get_inventory():
    res = pd.read_sql_query('select * from inventory_graph', engine_azure)
    #res = None
    bytes_image = io.BytesIO()
    sns.set_style('darkgrid')
    plt.figure(num=None, figsize=(30, 16), dpi=80,
               facecolor='w', edgecolor='k')
    sns.barplot(x='product_name', y='inventory_remaining',
                hue='pyear', data=res)
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return send_file(bytes_image, attachment_filename='inventory_remaining.png', mimetype='image/png')


@app.route('/inventory_test', methods=['GET'])
def inventory_test():
    res = pd.read_sql_query('select * from inventory_stats', engine_azure)
    print(res)
    return res.to_json()


@app.route('/wholetable', methods=['GET'])
def get():
    res = pd.read_sql_query('select * from final_report', engine_azure)
    print(res)
    return res.to_json()


@app.route('/totrevenueproduct', methods=['GET'])
def totrevenueproduct():
    res = pd.read_sql_query(
        'select pid,product_name, sum(revenue_total) as total_revenue from final_report group by pid, product_name \
            order by total_revenue desc', engine_azure)
    return res.to_json()


@app.route('/totrevenueproductyearwise', methods=['GET'])
def gettotrevenueproductyearwise():
    res = pd.read_sql_query('select pid,product_name,pyear, sum(revenue_total) as total_revenue \
from final_report \
group by pid, product_name,pyear \
order by total_revenue desc', engine_azure)
    return res.to_json()


@app.route('/totalquantityproduct', methods=['GET'])
def totalquantityproduct():
    res = pd.read_sql_query('select pid,product_name, sum(qty_total) as total_quantity \
from final_report \
group by pid, product_name \
order by total_quantity desc\
', engine_azure)
    return res.to_json()


# Run Server
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
