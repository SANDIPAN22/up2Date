from bs4 import BeautifulSoup as soup
import requests
import html5lib
from flask import Flask, render_template, request
from flask_mail import *
app=Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='ioticsnetrobosphere@gmail.com'
app.config['MAIL_PASSWORD']='zvckjwddyqnqfhbf'
app.config['MAIL_USE_SSL']=True
mail=Mail(app)

def getBody(url):
    url1=url
    r=requests.get(url1)
    s = soup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib 
    # print(s.prettify()) 
    tab=s.find('div',attrs={'class':'story_list row margin_b30'})
    centralcontainer=[]
    for row in tab.findAll('div',attrs={'class':'caption_box'}):
        container={}
        
        container['Headline']=row.find('span',attrs={'news_listing'}).text
        container['link']=row.a['href']
        container['Updated by']=((row.find('div',attrs={'dateline'}).text).split(',')[0]).split('by')[1]
        container['Updated at']=(row.find('div',attrs={'dateline'}).text).split(',')[1]
        container['Catagory']=(row.find('a',attrs={'class':'catname'}).text)
        centralcontainer.append(container)
    return centralcontainer
def getS(data):
    c=1
    cs='''Hey Learner; 
               Your Latest Reports are mentioned below. 
                
                '''
    for x in data:

        es=f''' 
            {c}. HEADLINE: {x['Headline']}
            UPDATED BY: {x['Updated by']}
            UPDATED AT: {x['Updated at']}
            FULL ARTICLE LINK: {x['link']}
            SUB-CATAGORY: {x['Catagory']}


        '''
        cs=cs+es
        c+=1
    ce='''


                created by upto2Date (~ sandipan)
    '''
    cs=cs+ce
    return cs



@app.route('/')
def home():
    return(render_template('mailclient.html'))
@app.route('/action/', methods=['POST'])
def action():
    q=request.form['qu']
    rec=request.form['recs']
    re=list(rec.split(','))
    sub="Top Up2Date Results on technology "+q
    msg=Message(sub,recipients=re,sender='ioticsnetrobosphere@gmail.com')
    if(q=='Featured'):
        url='https://gadgets.ndtv.com/features'
    elif(q=='Tech Reviews'):
        url='https://gadgets.ndtv.com/reviews'
    elif(q=='Tech Opinions'):
        url='https://gadgets.ndtv.com/opinion'
    elif(q=='Tech News'):
        url='https://gadgets.ndtv.com/news'
    
    s=getS(getBody(url))
    print(s)
    msg.body=s

    try:
        mail.send(msg)
        return (render_template('suc.html'))
    except:
        return (render_template('fail.html'))

if __name__=="__main__":
    app.run(debug='ON')








    
