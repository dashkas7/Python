from flask import Flask, render_template, request, url_for

app = Flask(__name__)

# модель MVC
    # model
    # view
    # controller
    
#app = Flask(__name__, static_folder=os.path.join(BASE_DIR, 'static'), template_folder=os.path.join(BASE_DIR, 'templates'))
users = [ 'user1', 'user2', 'user3', 'user4', 'user5' ]

@app.route("/")
def index():
    return render_template('1.html', admin=True, q=22222)

@app.route("/forma1/", methods=['GET','POST'])
def forma1():
    if request.method == 'POST':
        if request.form.get('login')=='qqq':
            return redirect(url_for('index'))
        else:
    return render_template('forma1.html', err='Неправильный пароль')
                                                              
    # else:
        return render_template('forma1.html', err=err, login=login)


@app.route("/message/<login>/<mes>/")
def message(login,mes):
    return render_template('mes.html',user=login, mes = mes)
    
    
    
@app.route("/users/")
def users_():
    return render_template('users.html', users=users)


@app.route("/test/<int:num>/")
def test(num):
    return 'test' * num
   # return render_template('test.html')

   
   
   
@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red; text-align:center; font-size:48px">Такой страницы не существует</h1>'




app.run(debug=True) 