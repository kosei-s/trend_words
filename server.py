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
    res_list = []
    soup_list = []

    phantomjs_key = 'ak-8dpg0-2qazt-9hcfv-ye32h-npvc1'

    # Google Trends
    payload = {'url': urls[0], 'renderType': 'HTML', 'outputAsJson': 'true'}
    payload = json.dumps(payload) # JSONパース
    payload = urllib.parse.quote(payload, safe='') # URIパース
    urls[0] = "https://phantomjscloud.com/api/browser/v2/" + phantomjs_key + "/?request=" + payload


    for i in range(len(urls)):
        res_list.append(requests.get(urls[i]))
        soup_list.append(bs4.BeautifulSoup(res_list[i].text))
    
    # 基本、動的サイトなのでうまくスクレイピングできない
    # seleniumとphantomjsを使う

    elems_list = []

    # Google Trends
    soup_list[0] = bs4.BeautifulSoup(res_list[0].json()['content']['data'], 'html.parser')
    elems_list.append(soup_list[0].select('.recently-trending-list-item'))

    # debug
    #print(len(elems_list[0]))
    #print(soup_list[0].text)
    
    return render_template('list.html', urls=urls, titles=titles, elems_list=elems_list, text=soup_list[0].text)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)