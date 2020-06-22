from flask import render_template, flash, redirect, url_for #Blueprint, url_for, redirect, request, session
from numerology import app

############### Microblog things
from numerology import db
from numerology.forms import RegistrationForm
from numerology.forms import LoginForm
from flask_login import current_user, login_user
from numerology.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
################################

#from DBcm import UseDatabase, ConnectionError, CredentialsError, SQLError
#from __init__ import app
import datetime

#import urllib.parse as urlparse
#from urllib.parse import parse_qs
#import json
#from newmerolgy import *

#from hello import contains_y,jeff, life_number,your_personal,real,hearts_d,image_num,bddict,year_num,lesson,debt
#from hello import check_karma,peak,digit_sum,b_t_ms
#import mysql.connector
#from mysql.connector import Error

x = datetime.datetime.now()
year_now = x.year


#main = Blueprint('main', __name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',year_now=year_now)

###################### Microblog things
@app.route('/users')
@login_required
def users():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('users/users.html', title='users page',posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users'))
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('users')
        return redirect(next_page)
    
    return render_template('users/login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('users/register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users'))
###########################################################
#@main.route('/')
#def index():
#    return render_template('index.html',year_now=year_now)

'''
@main.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        
        #call DB
        try:
            with UseDatabase(app.config['dbconfig']) as cursor:
                _SQL = """select * from users where id = %s"""
                cursor.execute(_SQL, [session['id']])
                user = cursor.fetchone()
                
        except ConnectionError as err:
                print('Is your database switched on? Error:', str(err))
        except CredentialsError as err:
                print('User-id/Password issues. Error:', str(err))
        except SQLError as err:
                print('Is your query correct? Error:', str(err))
        except Exception as err:
                print('Something went wrong: ', str(err))
        
        # Show the profile page with account info
        return render_template('profile_page.html', user=user,year_now=year_now)
    # User is not loggedin redirect to login page
    return redirect(url_for('auth.login'))
    
def log_question(res: str) -> None:
    with open('question.log', 'a') as log:
        print(res, file=log)
        
   
# log the response from payservice   
def log_receivepayment(req: 'flask_request') -> None:
    
    #get the amonut paid
    url = req.url
    parsed = urlparse.urlparse(url)
    component = parse_qs(parsed.query)['resp'][0]
    res = json.loads(component)
    
    #with open('receivepayment.log', 'a') as log:
        #print(res, file=log)

    if res == 740:
        number_of_quesion = 1
    elif res == 2410:
       number_of_quesion = 5
    elif res == 4170:
        number_of_quesion = 10
        
    #call DB
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """select * from users where id = %s"""
            cursor.execute(_SQL, [session['id']])
            user = cursor.fetchone()
            
    except ConnectionError as err:
            print('Is your database switched on? Error:', str(err))
    except CredentialsError as err:
            print('User-id/Password issues. Error:', str(err))
    except SQLError as err:
            print('Is your query correct? Error:', str(err))
    except Exception as err:
            print('Something went wrong: ', str(err))
    
    
    #call DB insert number of question bought
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """UPDATE users SET number_of_quesion = %s WHERE id = %s"""
        data_tuple = (number_of_quesion, session['id'])
        cursor.execute(_SQL, data_tuple)

    ##################################
           
    
@main.route('/paysuccess')
def paysuccess():
    if 'loggedin' in session:
        
        log_receivepayment(request)
        
        return redirect(url_for('main.profile'))
    return redirect(url_for('auth.login'))


@main.route('/payment')
def payment():
    return render_template('payment.html')
    
@main.route('/profile', methods=['POST'])
def profile_post():
    
    if request.method == 'POST' and 'loggedin' in session:
        #call DB
        try:
            with UseDatabase(app.config['dbconfig']) as cursor:
                _SQL = """select * from users where id = %s"""
                cursor.execute(_SQL, [session['id']])
                user = cursor.fetchone()
                
        except ConnectionError as err:
                print('Is your database switched on? Error:', str(err))
        except CredentialsError as err:
                print('User-id/Password issues. Error:', str(err))
        except SQLError as err:
                print('Is your query correct? Error:', str(err))
        except Exception as err:
                print('Something went wrong: ', str(err))
                
    if user[11] != 0:

        question = request.form['ask']
        log_question(question)
        
        number_of_quesion = user[11] - 1
        
        #call DB insert number of question bought
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """UPDATE users SET number_of_quesion = %s WHERE id = %s"""
            data_tuple = (number_of_quesion, session['id'])
            cursor.execute(_SQL, data_tuple)
            
        return redirect(url_for('main.profile'))
    else:
        msg = 'You Have Not A Enough Question'
        
    return render_template('profile_page.html', user=user, msg=msg, year_now=year_now)
    
@main.route('/viewquestions')
def view_the_log() -> str:
    with open('question.log') as log:
        contents = log.read()
        return contents
    
    
@main.route('/payfailed')
def payfailed():
    return render_template('payfailed.html')


#-------------------Numerology Readings----------------------#

@main.route('/event')
def event():
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        
        #call DB
        try:
            with UseDatabase(app.config['dbconfig']) as cursor:
                _SQL = """select * from users where id = %s"""
                cursor.execute(_SQL, [session['id']])
                user = cursor.fetchone()
                
        except ConnectionError as err:
                print('Is your database switched on? Error:', str(err))
        except CredentialsError as err:
                print('User-id/Password issues. Error:', str(err))
        except SQLError as err:
                print('Is your query correct? Error:', str(err))
        except Exception as err:
                print('Something went wrong: ', str(err))
    #(14, 'Uchechukwu', 'Emeka', 'Okwu', '1982-02-22', '01:24', 'Owerri, Imo, Nigeria', '08136767311', 'support@wec.org.ng', '12345', 'princely', 0, '', '')            
    FN = user[1]
    MN = user[2]
    LN = user[3]
    
    #DOB = user[4]
    bty = user[4][0:4] #1982
    btm = user[4][5:7] #02
    btd = user[4][8:10] #22
    
    #TOB = user[5]
    #POB = user[6]

    #event = numerology(FN,MN,LN,btd,btm,bty)[3]
     #[exp11,sU,iM1,lp,Mrity,phy,men,emo,intt,one,two,thr,fou,fiv,six,sev,eig,nin,ps,cH,cH1,cH2,cH3,Essence,pynum,uniynum,pina,
     # rc,pmonth,uniday,pday,Gpina,Gcha,Gper_pi,Gper_cha,k_day,k_pday,year_now]
    
    e = numerology(FN,MN,LN,btd,btm,bty)[3]
    
    return render_template('newuser/event.html',exp11=e[0],sU=e[1],iM1=e[2],lp=e[3],Mrity=e[4],phy=e[5],men=e[6],emo=e[7],intt=e[8],one=e[9],
                            two=e[10],thr=e[11],fou=e[12],fiv=e[13],six=e[14],sev=e[15],eig=e[16],nin=e[17],ps=e[18],cH=e[19],cH1=e[20],cH2=e[21],cH3=e[22],
                            Essence=e[23],pynum=e[24],uniynum=e[25],pina=e[26],rc=e[27],pmonth=e[28],uniday=e[29],pday=e[30],Gpina=e[31],Gcha=e[32],Gper_pi=e[33],
                            Gper_cha=e[34],k_day=e[35],k_pday=e[36],year_now=e[37])



@main.route('/reading')
def reading():
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        
        #call DB
        try:
            with UseDatabase(app.config['dbconfig']) as cursor:
                _SQL = """select * from users where id = %s"""
                cursor.execute(_SQL, [session['id']])
                user = cursor.fetchone()
                
        except ConnectionError as err:
                print('Is your database switched on? Error:', str(err))
        except CredentialsError as err:
                print('User-id/Password issues. Error:', str(err))
        except SQLError as err:
                print('Is your query correct? Error:', str(err))
        except Exception as err:
                print('Something went wrong: ', str(err))
    
    FN = user[1]
    MN = user[2]
    LN = user[3]
    
    #DOB = user[4]
    bty = user[4][0:4] #1982
    btm = user[4][5:7] #02
    btd = user[4][8:10] #22
    
    r = numerology(FN,MN,LN,btd,btm,bty)[0]
    
    #[exp,exp11, sU, sU1, iM, iM1,hP, ln, lp,bd1, lb, cH, cH1, cH2, cH3, LEB, Mrity,cha,btd1,bd22,p1,peak,p11,p2,p22,p3,p33,p4,p44,year_now]
    
    return render_template('newuser/reading.html', exp=r[0],exp11=r[1], sU=r[2], sU1=r[3], iM=r[4], iM1=r[5],
        hP=r[6], ln=r[7], lp=r[8],bd1=r[9], lb=r[10], cH=r[11], cH1=r[12], cH2=r[13], cH3=r[14], LEB=r[15], 
        Mrity=r[16],cha=r[17],btd1=r[18],bd22=r[19],p1=r[20],peak=r[21],p11=r[22],p2=r[23],p22=r[24],p3=r[25],
        p33=r[26],p4=r[27],p44=r[28],year_now=r[29],FN=FN,MN=MN,LN=LN,btd=btd,btm=btm,bty=bty,
        life_number=life_number,b_t_ms=b_t_ms,bddict=bddict,year_num=year_num,py_num=py_num,lesson=lesson,karma=karma,karma1=karma1,
        karma2=karma2,debt=debt,your_personal=your_personal,real=real,hearts_d=hearts_d,image_num=image_num,)
        
        
@bp.route('/reading1')
def reading1():
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        
        #call DB
        try:
            with UseDatabase(app.config['dbconfig']) as cursor:
                _SQL = """select * from users where id = %s"""
                cursor.execute(_SQL, [session['id']])
                user = cursor.fetchone()
                
        except ConnectionError as err:
                print('Is your database switched on? Error:', str(err))
        except CredentialsError as err:
                print('User-id/Password issues. Error:', str(err))
        except SQLError as err:
                print('Is your query correct? Error:', str(err))
        except Exception as err:
                print('Something went wrong: ', str(err))
    
    FN = user[1]
    MN = user[2]
    LN = user[3]
    
    #DOB = user[4]
    bty = user[4][0:4] #1982
    btm = user[4][5:7] #02
    btd = user[4][8:10] #22
    
    r = numerology(FN,MN,LN,btd,btm,bty)[1]
    
    return render_template('newuser/reading1.html',FN=FN,lp=lp,A=A,B=B,C=C,D=D,E=E,F=F,G=G,H=H,I=I,Rall=Rall,R1all=R1all,R2all=R2all,
    R3all=R3all,R4all=R4all,R5all=R5all,R6all=R6all,R7all=R7all,p=p,missing_numbers=missing_numbers,bash1=bash1,bash2=bash2,bash3=bash3,
    bash4=bash4,bash5=bash5,bash6=bash6,bash7=bash7,bash8=bash8,bash9=bash9,year_now=year_now)
'''