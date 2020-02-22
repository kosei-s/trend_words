from flask import Flask, render_template, request
import requests, bs4
import json
import urllib.parse

app = Flask(__name__)

urls = [
    'https://trends.google.co.jp/trends/?geo=JP',
    'https://search.yahoo.co.jp/#!/web'
]
titles = [
    'Google Trends',
    'Yahoo! 急上昇ワード'
]

@app.route('/')
def index():
    return render_template('index.html', urls=urls, titles=titles)

@app.route('/list', methods=['POST'])
def list():
    elems_list = []

    # PhantomJS Cloud用のKey (自身のもの)
    phantomjs_key = 'ak-8dpg0-2qazt-9hcfv-ye32h-npvc1'

    # Google Trends

    # JS動作後のページを取得
    payload = {'url': urls[0], 'renderType': 'HTML', 'outputAsJson': 'true'}
    payload = json.dumps(payload) # JSONパース
    payload = urllib.parse.quote(payload, safe='') # URIパース
    urls[0] = "https://phantomjscloud.com/api/browser/v2/" + phantomjs_key + "/?request=" + payload

    res = requests.get(urls[0])
    soup = bs4.BeautifulSoup(res.json()['content']['data'], 'html.parser')
    elems_list.append(soup.select('.recently-trending-list-item'))

    # Yahoo! 急上昇ワード

    # JS動作後のページを取得
    payload = {'url': urls[1], 'renderType': 'HTML', 'outputAsJson': 'true'}
    payload = json.dumps(payload) # JSONパース
    payload = urllib.parse.quote(payload, safe='') # URIパース
    urls[1] = "https://phantomjscloud.com/api/browser/v2/" + phantomjs_key + "/?request=" + payload

    res = requests.get(urls[1])
    soup = bs4.BeautifulSoup(res.json()['content']['data'], 'html.parser')
    elems_list.append(soup.select('p.que_2 a')) # ここはYahoo用のを見つける
    

    # debug
    #print(len(elems_list[0]))
    #print(soup_list[0].text)
    
    return render_template('list.html', urls=urls, titles=titles, elems_list=elems_list)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)