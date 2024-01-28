from flask import Flask,session,render_template,request,redirect,g,url_for,jsonify
from pymongo import MongoClient
from youtubesearchpython import VideosSearch
from youtube_transcript_api import YouTubeTranscriptApi
import wolframalpha
import wikipedia
from translate import Translator
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import requests
import stripe

app=Flask(__name__)
app.secret_key = 'password'
socketio = SocketIO(app)

client=MongoClient()
client=MongoClient("mongodb://localhost:27017/")

db=client['Hackathon']
users=db['users']
chat=db['chat_messages']

client= wolframalpha.Client('6WAEP9-R9GHYET35U')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET','POST'])
def signup():

    if request.method=='POST':

        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['email']
        password = request.form['password']
        confpassword = request.form['confpassword']
        age = request.form['age']
        gender = request.form['gender']
        disability = request.form['disability']
        preflang1 = request.form['preflang1']
        preflang2 = request.form['preflang2']
        hist1=[]
        hist2=[]
        hist3=[]
        subtitle=""
        id=""

        if db.users.find_one({'username': username}):
            correction = "Mail-ID alraedy taken"
            return render_template('signup.html',correction=correction)
        elif password != confpassword:
            correction = "Passwords are not similar"
            return render_template('signup.html',correction=correction)

        user_data = {'username': username, 'password': password,
                     'firstname': firstname, 'lastname': lastname,
                     'history1':hist1,'history2':hist2, 'history3':hist3,
                     'age':age, 'disability':disability, 'subtitle':subtitle,
                     'id':id,'preflang1':preflang1, 'gender':gender, 
                     'preflang2':preflang2,'confpassword':confpassword,"elite":"no"}
        db.users.insert_one(user_data)

        session['user'] = username
        if disability == 'dyslexia':
            return redirect(url_for('dyshome'))
        elif disability == 'deaf':
            return redirect(url_for('hearhome'))
  
        return redirect(url_for('home'))

    return render_template('signup.html')

@app.route('/extrw',methods=['GET','POST'])
def extrw():
    return render_template('extrw.html')

@app.route('/login', methods=['GET','POST'])
def login():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'yukthi@gmail.com':
            return redirect(url_for('admin'))

        user = db.users.find_one(
            {'username': username, 'password': password})

        if user:
            session['user'] = username
            dis = user.get('disability')
            if dis == 'dyslexia':
                return redirect(url_for('dyshome'))
            elif dis == 'deaf':
                return redirect(url_for('hearhome'))
            return redirect(url_for('home'))
        else:
            correction = "Invalid username or password"
            return render_template('login.html',correction=correction)

    return render_template('login.html')

@app.route('/home', methods=['GET','POST'])
def home():
    text = request.data.decode('utf-8')
    # print("Received text:", text)
    if text:
        user = db.users.find_one({'username': 'yukthi@gmail.com'})
        if text == 'button1':
            lilink = user.get('li1')
        elif text == 'button2':
            lilink = user.get('li2')
        elif text == 'button3':
            lilink = user.get('li3')
        elif text == 'button4':
            lilink = user.get('li4')
        elif text == 'button5':
            lilink = user.get('li5')
        elif text == 'button6':
            lilink = user.get('li6')
        elif text == 'button7':
            lilink = user.get('li7')
        elif text == 'button8':
            lilink = user.get('li8')
        elif text == 'button9':
            lilink = user.get('li9')
        elif text == 'button10':
            lilink = user.get('li10')
        elif text == 'button11':
            lilink = user.get('li11')
        elif text == 'button12':
            lilink = user.get('li12')
        elif text == 'button13':
            lilink = user.get('li13')
        elif text == 'button14':
            lilink = user.get('li14')
        elif text == 'button15':
            lilink = user.get('li15')
        elif text == 'button16':
            lilink = user.get('li16')
        elif text == 'button17':
            lilink = user.get('li17')
        elif text == 'button18':
            lilink = user.get('li18')
        elif text == 'button19':
            lilink = user.get('li19')
        elif text == 'button20':
            lilink = user.get('li20')
        elif text == 'button21':
            lilink = user.get('li21')
        user = db.users.find_one({'username': session['user']})
        if user:
            db.users.update_one({'username':session['user']},{'$set':{'courslist':lilink}})
    user = db.users.find_one({'username': session['user']})
    if user:
        age=user.get('age') 
        disability = user.get('disability')
        epass = user.get('elite')
    if request.method == 'POST':
        to_search = request.form['ytsearch']
        playsearch = request.form['ytplay']
        if playsearch:
            return redirect(url_for('extrw'))
        videosSearch = VideosSearch(to_search, limit=7)
        results = videosSearch.result()
        video_links = []
        for result in results['result']:
            video_links.append(result['link'])
        link = video_links[0]
        sep_l = link.split('=')
        id = sep_l[-1]
        try:
            transcript = YouTubeTranscriptApi.get_transcript(id)
        except:
            try:
                link = video_links[1]
                sep_l = link.split('=')
                id = sep_l[-1]
                transcript = YouTubeTranscriptApi.get_transcript(id)
            except:
                link = video_links[2]
                sep_l = link.split('=')
                id = sep_l[-1]
                transcript = YouTubeTranscriptApi.get_transcript(id)
        script = ""
        for text in transcript:
            t = text["text"]
            if t != '[Music]':
                script += t + " "

        subtitle = script

        if subtitle:
            user = db.users.find_one({'username': session['user']})
            if user:
                db.users.update_one({'username':session['user']},{'$set':{'subtitle':subtitle}})
                db.users.update_one({'username':session['user']},{'$set':{'id':id}})
                db.users.update_one({'username':session['user']},{'$set':{'video_links':video_links}})
            return redirect(url_for('extract'))
    return render_template('main.html',age=age,disability=disability,epass=epass)

@app.route('/holistic')
def holistic():
    return render_template('holistic.html')

@app.route('/vocal')
def vocal():
    return render_template('vocal.html')

@app.route('/edit',methods=['GET', 'POST'])
def edit():
    if request.method=='POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['email']
        password = request.form['password']
        confpassword = request.form['confpassword']
        age = request.form['age']
        gender = request.form['gender']
        disability = request.form['disability']
        preflang1 = request.form['preflang1']
        preflang2 = request.form['preflang2']
        user = db.users.find_one({'username': session['user']})
        if user:
            db.users.update_many({'username':session['user']},{'$set':{'username': username, 'password': password,
                     'firstname': firstname, 'lastname': lastname,
                     'age':age, 'disability':disability,
                     'preflang1':preflang1, 'gender':gender, 
                     'preflang2':preflang2,'confpassword':confpassword}})
        if disability == 'dyslexia':
            return redirect(url_for('dyshome'))
        elif disability == 'deaf':
            return redirect(url_for('hearhome'))
  
        return redirect(url_for('home'))
    user = db.users.find_one({'username': session['user']})
    if user:
        username = user.get('username')
        password = user.get('password')
        firstname = user.get('firstname')
        lastname = user.get('lastname')
        age = user.get('age')
        disability = user.get('disability')
        gender = user.get('gender')
        preflang1 = user.get('preflang1')
        preflang2 = user.get('preflang2')
        confpassword = user.get('confpassword')
    return render_template('edit.html',username = username,password=password,firstname=firstname,lastname=lastname,age=age,disability=disability,gender=gender,preflang1=preflang1,preflang2=preflang2,confpassword=confpassword)

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    user = db.users.find_one({'username': session['user']})
    if user:
        subtitle=user.get('subtitle') 
        video_links = user.get('video_links')
        id=user.get('id')
        vll=[]
        for i in video_links:
            sep_l = i.split('=')
            idi = sep_l[-1]
            vll.append(idi)
        id1=vll[1]
        id2=vll[2]
        id3=vll[3]
        id4=vll[4]
        id5=vll[5]
        id6=vll[6]
    return render_template('extract.html', subtitle=subtitle,id=id,id1=id1,id2=id2,id3=id3,id4=id4,id5=id5,id6=id6)

@app.route('/chat', methods=['GET','POST'])
def chat():
    if request.method=='POST':
        msg=request.form['msg']

        user = db.users.find_one(
            {'username': 'madu@gmail.com'})
        
        if user:
            hist1=user.get('history1')
            hist1.append(str(session['user']+" : "+msg))
            db.users.update_one({'username':'madu@gmail.com'},{'$set':{'history1':hist1}})
            no_of_box=len(hist1)
            """<script>
                window.location.href = window.location.href;
            </script>"""
        return render_template('chat1.html',no_of_box=no_of_box,hist1=hist1)
    else:
        user = db.users.find_one({'username': 'madu@gmail.com'})
        if user:
            hist1=user.get('history1')
            no_of_box=len(hist1)
        return render_template('chat1.html',no_of_box=no_of_box,hist1=hist1)

@app.route('/vdoin')
def vdoin():
    return render_template('vdoin.html')

@app.route('/vdocall')
def vdocall():
    return render_template('vdocall.html')

@app.route('/base',methods=['GET', 'POST'])
def base():
    if request.method=='POST':
        roomID = request.form['roomID']
        return redirect("/vdocall?roomID="+roomID)
    return render_template('base.html')

@app.route('/bot',methods=['GET','POST'])
def bot():
    if request.method=='POST':
        query=request.form['dbt']
        try:
            res = client.query(query)
            output = next(res.results).text
        except StopIteration:
            try:
                output = wikipedia.summary(query,sentences=3)
            except wikipedia.exceptions.DisambiguationError as e:
                output = "Sorry, the query is ambiguous. Please provide more context."
            except wikipedia.exceptions.PageError as e:
                output = "Sorry, no information found for the query."
        
        output = f"""Hey Sujay,
        That's a nice question and here is the answer - 
        {output}"""
        # ht_out = f"{output}"
        return jsonify(output = output)
    else:
        return render_template('bot.html')
    # user = db.users.find_one({'username': session['user']})
    # if user:
    #     chat_history = list(db.chat.find({'username': session['user']}))
    #     print(chat_history)
    #     return render_template("bot-new.html", chat_history=chat_history)
    # else:
    #     return "User ID not found or not in session"
    
@app.route('/store_message',methods=['POST'])
def store_message():
    user = db.users.find_one({'username': session['user']})
    query = request.form['dbt']
    try:
        res = client.query(query)
        output = next(res.results).text
    except StopIteration:
        try:
            output = wikipedia.summary(query,sentences=3)
        except wikipedia.exceptions.DisambiguationError as e:
            output = "Sorry, the query is ambiguous. Please provide more context."
        except wikipedia.exceptions.PageError as e:
            output = "Sorry, no information found for the query."
    db.chat.insert_one({'username':user,'Query':query,'Output':output})
    return redirect('/bot-new')

@app.route('/api/get-chat-messages')
def get_chat_messages():
    user = db.users.find_one({'username': session['user']})
    chat_history = list(db.chat.find({'username': user}))
    print(chat_history)
    return jsonify(success=True, messages=chat_history)
    
@app.route('/pre',methods=['GET', 'POST'])
def pre():
    if request.method=='POST':
        difficulty = request.form['difficulty'] 
        user = db.users.find_one({'username': session['user']})
        if user:
            db.users.update_one({'username':session['user']},{'$set':{'difflevel':difficulty}})
        return redirect(url_for('puzzle'))
    return render_template('pre.html')

@app.route('/puzzle',methods=['GET', 'POST'])
def puzzle():
    solist = request.form.getlist('grid_data')
    if solist:
        # print(solist)
        user = db.users.find_one({'username': session['user']})
        if user:
            db.users.update_one({'username':session['user']},{'$set':{'solist':solist}})
    user = db.users.find_one({'username': session['user']})
    if user:
        level = user.get('difflevel')
    level = int(level)/100
    game = Sudoku(3).difficulty(0.5)
    num_board = game.board
    nums = []
    for i in num_board:
        for j in i:
            if j is None:
                nums.append(' ')
            else:
                nums.append(j)
    perfect = game.solve()
    soln_board = perfect.board
    setsoln = []
    for i in soln_board:
        for j in i:
            if j is None:
                setsoln.append(' ')
            else:
                setsoln.append(j)
    user = db.users.find_one({'username': session['user']})
    if user:
        db.users.update_one({'username':session['user']},{'$set':{'perlist':setsoln}})
    return render_template('puzzle.html',nums = nums)

@app.route('/solution',methods=['GET','POST'])
def solution():
    result=""
    user = db.users.find_one({'username': session['user']})
    if user:
        check1 = user.get('solist')
        check2 = user.get('perlist')
    if check1 == check2:
        result ="Congrats You have won "
    else:
        result="Better luck next time"
    return render_template('solution.html',result=result,nums=check2)

@app.route('/find',methods=['GET','POST'])
def find():
    sofindlist = request.form.getlist('grid_data')
    if sofindlist:
        org=[]
        for i in sofindlist:
            for j in i:
                if j==',':
                    org.append(0)
                else:
                    org.append(int(j))
        sublists = [org[i:i+9] for i in range(0, len(org), 9)]
        sublists.pop()
        soll = Sudoku(3,3,board=sublists)
        ans = soll.solve()
        kara = ans.board
        nums=[]
        for i in kara:
            for j in i:
                nums.append(j)
        user = db.users.find_one({'username': session['user']})
        if user:
            db.users.update_one({'username':session['user']},{'$set':{'god':nums}})
        return redirect(url_for('findsolution'))
    return render_template('find.html')

@app.route('/findsolution',methods=['GET','POST'])
def findsolution():
    user = db.users.find_one({'username': session['user']})
    if user:
        nums = user.get('god')
    return render_template('findsolution.html',nums=nums)

@app.route('/landing')
def landing():
    if session['user']:
        session.pop('user', None)
    return render_template('index.html')

def translate_paragraph(paragraph, target_language):
    translator = Translator(to_lang=target_language)
    translation = translator.translate(paragraph)
    return translation

@app.route('/ViewTransactions')
def ViewTransactions():
    return render_template('ViewTransactions.html')

@app.route('/courses',methods=['GET','POST'])
def courses():
    user = db.users.find_one({'username': session['user']})
    if user:
        courlist = user.get('courslist')
    transcript = YouTubeTranscriptApi.get_transcript(courlist[0])
    script = ""
    for text in transcript:
        t = text["text"]
        if t != '[Music]':
            script += t + " "

    subtitle = script
    
    id1=courlist[0]
    id2=courlist[1]
    id3=courlist[2]

    if request.method=='POST':
        target_language = request.form['django']
        url = "https://nlp-translation.p.rapidapi.com/v1/translate"
        querystring = {"text":subtitle,"to":target_language,"from":"en"}

        headers = {
            "X-RapidAPI-Key": "43cc727829msh5644c8389123bf7p18e60cjsnc980a33f130a",
            "X-RapidAPI-Host": "nlp-translation.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        ask = response.json()["translated_text"][target_language]
        return render_template('courses.html',subtitle=ask,id1=id1,id2=id2,id3=id3)

        
    return render_template('courses.html',subtitle=subtitle,id1=id1,id2=id2,id3=id3)

@app.route('/spelltest')
def spelltest():
    return render_template('test1.html')

@app.route('/readtest')
def readtest():
    return render_template('test2.html')

@app.route('/smpl')
def smpl():
    text = request.data.decode('utf-8')
    # print("Received text:", text)
    if text:
        user = db.users.find_one({'username': 'yukthi@gmail.com'})
        if text == 'button1':
            lilink = user.get('li1')
        elif text == 'button2':
            lilink = user.get('li2')
        elif text == 'button3':
            lilink = user.get('li3')
        elif text == 'button4':
            lilink = user.get('li4')
        elif text == 'button5':
            lilink = user.get('li5')
        elif text == 'button6':
            lilink = user.get('li6')
        elif text == 'button7':
            lilink = user.get('li7')
        elif text == 'button8':
            lilink = user.get('li8')
        elif text == 'button9':
            lilink = user.get('li9')
        elif text == 'button10':
            lilink = user.get('li10')
        elif text == 'button11':
            lilink = user.get('li11')
        elif text == 'button12':
            lilink = user.get('li12')
        elif text == 'button13':
            lilink = user.get('li13')
        elif text == 'button14':
            lilink = user.get('li14')
        elif text == 'button15':
            lilink = user.get('li15')
        elif text == 'button16':
            lilink = user.get('li16')
        elif text == 'button17':
            lilink = user.get('li17')
        elif text == 'button18':
            lilink = user.get('li18')
        elif text == 'button19':
            lilink = user.get('li19')
        elif text == 'button20':
            lilink = user.get('li20')
        elif text == 'button21':
            lilink = user.get('li21')
        user = db.users.find_one({'username': session['user']})
        if user:
            db.users.update_one({'username':session['user']},{'$set':{'courslist':lilink}})
    user = db.users.find_one({'username': session['user']})
    if user:
        age=user.get('age') 
        disability = user.get('disability')
    if request.method == 'POST':
        to_search = request.form['ytsearch']
        # print(to_search)
        videosSearch = VideosSearch(to_search, limit=7)
        results = videosSearch.result()
        video_links = []
        for result in results['result']:
            video_links.append(result['link'])
        link = video_links[0]
        sep_l = link.split('=')
        id = sep_l[-1]
        transcript = YouTubeTranscriptApi.get_transcript(id)
        script = ""
        for text in transcript:
            t = text["text"]
            if t != '[Music]':
                script += t + " "

        subtitle = script

        if subtitle:
            user = db.users.find_one({'username': session['user']})
            if user:
                db.users.update_one({'username':session['user']},{'$set':{'subtitle':subtitle}})
                db.users.update_one({'username':session['user']},{'$set':{'id':id}})
                db.users.update_one({'username':session['user']},{'$set':{'video_links':video_links}})
            return redirect(url_for('extract'))
    return render_template('smpl.html',age=age,disability=disability)

@app.route('/admin',methods = ['GET','POST'])
def admin():
    if request.method=='POST':
        courseid = request.form['courseid']
        link1 = request.form['link1']
        link2 = request.form['link2']
        link3 = request.form['link3']
    
        new_l = [link1,link2,link3]

        db.users.update_one({'username':'yukthi@gmail.com'},{'$set':{courseid:new_l}})
    return render_template('admind.html')

@app.route('/hearhome', methods=['GET', 'POST'])
def hearhome():
    text = request.data.decode('utf-8')
    # print("Received text:", text)
    if text:
        user = db.users.find_one({'username': 'yukthi@gmail.com'})
        if text == 'button1':
            lilink = user.get('li1')
        elif text == 'button2':
            lilink = user.get('li2')
        elif text == 'button3':
            lilink = user.get('li3')
        elif text == 'button4':
            lilink = user.get('li4')
        elif text == 'button5':
            lilink = user.get('li5')
        elif text == 'button6':
            lilink = user.get('li6')
        elif text == 'button7':
            lilink = user.get('li7')
        elif text == 'button8':
            lilink = user.get('li8')
        elif text == 'button9':
            lilink = user.get('li9')
        elif text == 'button10':
            lilink = user.get('li10')
        elif text == 'button11':
            lilink = user.get('li11')
        elif text == 'button12':
            lilink = user.get('li12')
        elif text == 'button13':
            lilink = user.get('li13')
        elif text == 'button14':
            lilink = user.get('li14')
        elif text == 'button15':
            lilink = user.get('li15')
        elif text == 'button16':
            lilink = user.get('li16')
        elif text == 'button17':
            lilink = user.get('li17')
        elif text == 'button18':
            lilink = user.get('li18')
        elif text == 'button19':
            lilink = user.get('li19')
        elif text == 'button20':
            lilink = user.get('li20')
        elif text == 'button21':
            lilink = user.get('li21')
        user = db.users.find_one({'username': session['user']})
        if user:
            db.users.update_one({'username':session['user']},{'$set':{'courslist':lilink}})
    user = db.users.find_one({'username': session['user']})
    if user:
        age=user.get('age') 
        disability = user.get('disability')
    if request.method == 'POST':
        to_search = request.form['ytsearch']
        videosSearch = VideosSearch(to_search, limit=7)
        results = videosSearch.result()
        video_links = []
        for result in results['result']:
            video_links.append(result['link'])
        link = video_links[0]
        sep_l = link.split('=')
        id = sep_l[-1]
        transcript = YouTubeTranscriptApi.get_transcript(id)
        script = ""
        for text in transcript:
            t = text["text"]
            if t != '[Music]':
                script += t + " "

        subtitle = script

        if subtitle:
            user = db.users.find_one({'username': session['user']})
            if user:
                db.users.update_one({'username':session['user']},{'$set':{'subtitle':subtitle}})
                db.users.update_one({'username':session['user']},{'$set':{'id':id}})
                db.users.update_one({'username':session['user']},{'$set':{'video_links':video_links}})
            return redirect(url_for('extract'))
    return render_template('hearhome.html',age=age,disability=disability)

@app.route('/heartest')
def heartest():
    return render_template('test3.html')

@app.route('/crypto')
def crypto():
    return render_template('crypto.html')

public_key = "pk_test_51OAc4kSCU9tagpDmW1MEp5JyCw7sfmbVqlxs4SYpfxGpoFsCHxbEzW69eKIWK7Sr1XHWx4CROKSLZZ90h7iAHgtT00Zmb1OGcC"
stripe.api_key = "sk_test_51OAc4kSCU9tagpDmxHbWoT7JizAtvE7yZGeKBKWGE7SfojdYPZPW1AIyjmVcS0bXXZF7S0YUsj9unkcXiOFH3Jvn001ZVKT8ir"

@app.route('/stripe_index')
def stripe_index():
    return render_template('stripe_index.html', public_key=public_key)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/premium')
def premium():
    return render_template('premium.html')

@app.route('/payment', methods=['POST'])
def payment():

    # CUSTOMER INFO
    customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                      source=request.form['stripeToken'])

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=399, 
        currency='INR',
        description='Mentor'
    )

    return redirect(url_for('thankyou'))


@app.route('/dyshome', methods=['GET', 'POST'])
def dyshome():
    text = request.data.decode('utf-8')
    # print("Received text:", text)
    if text:
        user = db.users.find_one({'username': 'yukthi@gmail.com'})
        if text == 'button1':
            lilink = user.get('li1')
        elif text == 'button2':
            lilink = user.get('li2')
        elif text == 'button3':
            lilink = user.get('li3')
        elif text == 'button4':
            lilink = user.get('li4')
        elif text == 'button5':
            lilink = user.get('li5')
        elif text == 'button6':
            lilink = user.get('li6')
        elif text == 'button7':
            lilink = user.get('li7')
        elif text == 'button8':
            lilink = user.get('li8')
        elif text == 'button9':
            lilink = user.get('li9')
        elif text == 'button10':
            lilink = user.get('li10')
        elif text == 'button11':
            lilink = user.get('li11')
        elif text == 'button12':
            lilink = user.get('li12')
        elif text == 'button13':
            lilink = user.get('li13')
        elif text == 'button14':
            lilink = user.get('li14')
        elif text == 'button15':
            lilink = user.get('li15')
        elif text == 'button16':
            lilink = user.get('li16')
        elif text == 'button17':
            lilink = user.get('li17')
        elif text == 'button18':
            lilink = user.get('li18')
        elif text == 'button19':
            lilink = user.get('li19')
        elif text == 'button20':
            lilink = user.get('li20')
        elif text == 'button21':
            lilink = user.get('li21')
        user = db.users.find_one({'username': session['user']})
        if user:
            db.users.update_one({'username':session['user']},{'$set':{'courslist':lilink}})
    user = db.users.find_one({'username': session['user']})
    if user:
        age=user.get('age') 
        disability = user.get('disability')
    if request.method == 'POST':
        to_search = request.form['ytsearch']
        videosSearch = VideosSearch(to_search, limit=7)
        results = videosSearch.result()
        video_links = []
        for result in results['result']:
            video_links.append(result['link'])
        link = video_links[0]
        sep_l = link.split('=')
        id = sep_l[-1]
        transcript = YouTubeTranscriptApi.get_transcript(id)
        script = ""
        for text in transcript:
            t = text["text"]
            if t != '[Music]':
                script += t + " "

        subtitle = script

        if subtitle:
            user = db.users.find_one({'username': session['user']})
            if user:
                db.users.update_one({'username':session['user']},{'$set':{'subtitle':subtitle}})
                db.users.update_one({'username':session['user']},{'$set':{'id':id}})
                db.users.update_one({'username':session['user']},{'$set':{'video_links':video_links}})
            return redirect(url_for('extract'))
    return render_template('dyshome.html',age=age,disability=disability)

user_languages = {} 
user_names = {} 
def translate_message(message, source_language, target_language):
    translator = Translator(to_lang = target_language)
    translated_message = translator.translate(message)
    return translated_message

# def translate_message(message,source_language,target_language):

#     url = "https://nlp-translation.p.rapidapi.com/v1/translate"

#     querystring = {"text":message,"to":target_language,"from":"en"}

#     headers = {
#         "X-RapidAPI-Key": "43cc727829msh5644c8389123bf7p18e60cjsnc980a33f130a",
#         "X-RapidAPI-Host": "nlp-translation.p.rapidapi.com"
#     }

#     response = requests.get(url, headers=headers, params=querystring)

    # return response.json()['translated_text'][target_language]

@app.route('/chatr')
def chatr():
    user = db.users.find_one({'username': session['user']})
    epass=user.get('elite') 
    if epass:
        return render_template('chatr.html')
    else:
        return redirect(url_for('crypto'))

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('message')
def handle_message(data):
    room = data['room']
    message = data['message']
    source_language = user_languages[room]
    user_name = user_names[request.sid]
    
    for client_room, target_language in user_languages.items():
        if client_room != room:  # Exclude the source user's room
            translated_message = translate_message(message, source_language, target_language)
            emit('user_message', {'user': user_name, 'message': translated_message}, room=client_room)

@socketio.on('create')
def handle_create(data):
    room = data['room']
    user_languages[room] = data['language']
    user_names[request.sid] = data['user']
    join_room(room)
    emit('system_message', {'message': f'You have created and joined room {room}.'})
    emit('system_message', {'message': 'Translation is enabled in this room.'}, room=room)

@socketio.on('join')
def handle_join(data):
    room = data['room']
    user_languages[room] = data['language']
    user_names[request.sid] = data['user']
    join_room(room)
    emit('system_message', {'message': f'You have joined room {room}.'})
    emit('system_message', {'message': 'Translation is enabled in this room.'}, room=room)

@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    user_name = user_names[request.sid]
    leave_room(room)
    emit('system_message', {'message': f'{user_name} has left the room.'}, room=room)
    del user_names[request.sid] 
    emit('update_users', {'users': list(user_names.values())}, room=room)  

if __name__ == '__main__':
    socketio.run(app, debug=True)