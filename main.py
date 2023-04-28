from flask import Flask, render_template, redirect
import json
from forms.register import RegisterForm
from forms.login import LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'QaWszxcHANTERSPEEKi3noff_0207wiLLBeFinE'

flag = False
is_authenticated = False


@app.route('/', methods=['GET', 'POST'])
def main_page():
    global flag, is_authenticated
    with open('inform.about_community.txt', 'r', encoding='utf-8') as txt:
        data = [string.strip('\n') for string in txt.readlines()]
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if is_authenticated is not True:
            with open('db/db_sess.json', 'r', encoding='utf-8') as query:
                users = json.load(query)["database"]["users"]
            if not users:
                return render_template('index.html', title='Главная', inform=data, form=login_form,
                                       message='Пользователь не найден!', is_authenticated=is_authenticated)
            for user in users:
                if user["login"] == login_form.login.data and user["password"] == login_form.password.data:
                    current_user = users[users.index(user)]
                    is_authenticated = True
                    return render_template('index.html', title='Главная', inform=data, form=login_form,
                                           is_autorization=f'С возвращением, {current_user["name"]}!',
                                           is_authenticated=is_authenticated)
            if is_authenticated is False:
                return render_template('index.html', title='Главная', inform=data, form=login_form,
                                       message='Пользователь не найден!', is_authenticated=is_authenticated)
        return render_template('index.html', title='Главная', inform=data, form=login_form,
                               message='Вы уже вошли в аккаунт!', is_authenticated=is_authenticated)
    return render_template('index.html', title='Главная', inform=data, form=login_form,
                           is_authenticated=is_authenticated)


@app.route('/about_community')
def about_community():
    with open('inform.about_community.txt', 'r', encoding='utf-8') as txt:
        data = [string.strip('\n') for string in txt.readlines()]
    return render_template('about_community.html', title='О сообществе', inform=data, is_authenticated=is_authenticated)


@app.route('/releases')
def releases():
    with open('all_releases.json', 'r', encoding='utf-8') as jsn_file:
        data = json.load(jsn_file)
        dict_data = data['releases'][0]
    return render_template('releases.html', title='Релизы', dict_inform=dict_data, is_authenticated=is_authenticated)


@app.route('/all_tracks')
def all_tracks():
    return render_template('all_tracks.html', title='Все треки', is_authenticated=is_authenticated)


@app.route('/favourites')
def favourites():
    return render_template('favourites.html', title='Избранное', is_authenticated=is_authenticated)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data == form.check_password.data:
            with open("db/db_sess.json", "r", encoding='utf-8') as read:
                data = json.load(read)
                dict_data = dict(zip(['name', 'login', 'email', 'password'],
                                     [form.name.data, form.login.data, form.email.data, form.password.data]))
                data["database"]["users"].append(dict_data)
            with open("db/db_sess.json", "w", encoding='utf-8') as write:
                json.dump(data, write)
            return redirect('/')
        return render_template('register.html', title='Регистрация', form=form, message='Пароли не совпадают!')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
def logout():
    global is_authenticated
    # with open('db/db_sess.json', 'r', encoding='utf-8') as query:
    #     data = json.load(query)
    #     del data['database']['users'][data['database']['users'].index(main_page()[1])]
    # with open('db/db_sess.json', 'w', encoding='utf-8') as write:
    #     json.dump(data, write)
    is_authenticated = False
    return redirect("/")


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')


