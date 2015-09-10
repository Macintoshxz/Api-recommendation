from flask import Flask
from flask import jsonify
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template

from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017,socketKeepAlive=True)
dbwekey = client.get_database('wekeypedia')
reco_col = dbwekey.get_collection('recommendation')


def get_recommendation(domain,title):
    reco = reco_col.find_one({'title':title})
    if reco == None:
        reco={}
    else:
        reco = reco.get('links')
    return reco


@app.route("/api/<domain>/<title>/<start>/<end>")
def api(domain,title,start='0',end='10'):
    values = get_recommendation(domain,title)
    reco = sorted(values,key=lambda x:x['score'],reverse=True)[int(start):int(end)]
    recomm = { 'domain':domain,
               'title':title, 
               'start':start,
               'end':end,
               'recommendation':reco}
    return jsonify(recomm)


@app.route("/<domain>//<start>/<end>",methods=['GET'])
@app.route("/<domain>/<title>/<start>/<end>",methods=['GET'])
def display(domain='en',title='',start='0',end='10'):
    if title!='':
        values = get_recommendation(domain,title)
        reco=sorted(values,key=lambda x:x['score'],reverse=True)[int(start):int(end)]
        if len(reco)==0:
            text = 'The page "%s" with domain "%s" has not been found.' % (title,domain)
            return render_template('main.html',message={'title':'Page not found','text':text})
        return render_template('main.html',entries=reco,domain=domain,title=title,start=start,end=end)
    else:
        text = 'You need to precise a title.'
        return render_template('main.html',message={'title':'No page title precised.','text':text})


@app.route("/", methods=['POST'])
def form(domain='',title=''):
    if request.method == 'POST':
        start_form=request.form['start']
        end_form=request.form['end']
        return redirect(url_for('display',domain=request.form['domain'],
                    title=request.form['title'],start=start_form,end=end_form))


@app.route("/", methods=['GET'])
def index():
    return render_template('main.html')

if __name__ == "__main__":
  app.run(debug=True)
