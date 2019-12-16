from flask import Flask, jsonify, request
import requests
import pika
import json
import os
import subprocess

from html.parser import HTMLParser

from .config import Config

app = Flask(__name__)

app.config.from_object(Config())
app.logger.info("Connecting db to: {}".format(app.config['SQLALCHEMY_DATABASE_URI']))

from .models import db

# db.init_app(app)

# app.config.from_object(os.environ['APP_SETTINGS'])
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


db.init_app(app)


class MyHTMLParser(HTMLParser):
    # def handle_starttag(self, tag, attrs):
    #     if tag == 'script':        
    #       print("Start ===> ", tag)

    # def handle_endtag(self, tag):
    #     if tag == 'script':
    #       print ("End ===> ", tag)
    parsed = "{}"

    def handle_data(self, data):
        START = 'wb.product.DomReady.init'
        END = '});'
        DATA = 'data:'
        startCode = data.find(START)
        if startCode != -1:
            endCode = data.find(END, startCode)
            rawCode = data[startCode:endCode]
            dataStartOffset = rawCode.find(DATA)
            dataRawCode = rawCode[dataStartOffset + 6:]
            dataEndOffset = dataRawCode.find("\n")
            self.parsed = json.loads(dataRawCode[:dataEndOffset - 1])
        # print("Data ==> ", data)

    def get_parsed(self):
        return self.parsed


# channel = None

# # Step #2
# def on_connected(connection):
#     """Called when we are fully connected to RabbitMQ"""
#     # Open a channel
#     connection.channel(on_channel_open)

# # Step #3
# def on_channel_open(new_channel):
#     """Called when our channel has opened"""
#     global channel
#     channel = new_channel
#     channel.queue_declare(queue="test", durable=True, exclusive=False, auto_delete=False, callback=on_queue_declared)

# # Step #4
# def on_queue_declared(frame):
#     """Called when RabbitMQ has told us our Queue has been declared, frame is the response from RabbitMQ"""
#     channel.basic_consume('test', handle_delivery)

# # Step #5
# def handle_delivery(channel, method, header, body):
#     """Called when we receive a message from RabbitMQ"""
#     print(body)

# # Step #1: Connect to RabbitMQ using the default parameters
# parameters = pika.ConnectionParameters()
# connection = pika.SelectConnection(parameters, on_connected)

# try:
#     # Loop so we can communicate with RabbitMQ
#     connection.ioloop.start()
# except KeyboardInterrupt:
#     # Gracefully close the connection
#     connection.close()
#     # Loop until we're fully closed, will stop on its own
#     connection.ioloop.start()


@app.route('/')
def hello_world():
    # print(subprocess.call(["ls", "-la"]))
    # res = subprocess.call(["node", "index.js"])
    # print(res)
    # print(subprocess.Popen("node index.js", stdout=PIPE).stdout.read())
    # print(os.popen("node index.js").read())


    # print(subprocess.call("node index.js", shell=True)) 
    # return os.popen("node index.js").read()
    return 'start'
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/rpc')
def show_rpc():
    credentials = pika.PlainCredentials(username='guest', password='guest')
    # credentials = pika.PlainCredentials(username='user', password='bitnami')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',
                                                                    5672,
                                                                    '/',
                                                                    credentials))
    print("======================>>>>>>>>")    
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello from Pytnon!')
    print(" [x] Sent 'Hello World!'")
    connection.close()

    # credentials = pika.PlainCredentials('guest', 'guest')
    # parameters = pika.ConnectionParameters('localhost',
    #                                 5672,
    #                                 '/',
    #                                 credentials)

    # connection = pika.BlockingConnection(parameters)

    # channel = connection.channel()

    # channel.queue_declare(queue='hello')

    # channel.basic_publish(exchange='',
    #                 routing_key='hello',
    #                 body='Hello W0rld!')
    # print(" [x] Sent 'Hello World!'")
    # connection.close()
    
    return 'RPC'


@app.route('/post/<int:post_id>', methods=['POST', 'DELETE'])
def show_post(post_id):
    if request.method == 'POST':
        return 'Post %d' % post_id
    else:
        return 'Delete %d' % post_id

@app.route('/posted/', methods=['POST'])
def show_my_post():
    # show the post with the given id, the id is an integer
    return 'Post test'


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath

@app.route('/search')
def get_data():
    resp = requests.get('https://www.shopstyle.com/api/v2/site/search?abbreviatedCategoryHistogram=true&cat=mens-clothes&includeLooks=true&includeProducts=true&includeSavedQueryId=true&limit=40&locales=all&pid=shopstyle&useElasticsearch=true&view=web').content
    return resp

@app.route('/products')
def get_products():
    resp = requests.get('https://www.shopstyle.com/api/v2/products?abbreviatedCategoryHistogram=true&cat=mens-jeans&device=desktop&includeLooks=true&includeProducts=true&includeSavedQueryId=true&limit=40&locales=all&maxNumFilters=1000&numLooks=20&offset=40&pid=shopstyle&prevCat=mens-clothes&productScore=LessPopularityEPC&url=%2Fbrowse%2Fmens-jeans&useElasticsearch=true&view=web').content
    return resp

@app.route('/recommends')
def get_providers():
    resp = requests.get('https://www.wildberries.ru/recommendations/providers').content
    return resp


@app.route('/target')
def get_targets():
    result = []
    # for i in range(1400, 1500):
    for i in range(1400, 1420):
      resp = requests.get(f"https://www.wildberries.ru/catalog/{i}/detail.aspx")
      content = resp.content
      if resp.status_code == 404:
        continue
      parser = MyHTMLParser()
      parser.feed(content.decode('utf-8'))
      res = parser.get_parsed()
      result.append(res)
    # r.html.render()
    # print(r.content.decode('utf-8'))
    # driver = webdriver.Firefox()
    # driver.get('https://www.wildberries.ru/catalog/4316944/detail.aspx')
    # print(driver.page_source)
    return jsonify(result)
