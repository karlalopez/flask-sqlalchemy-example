from flask import render_template, request, redirect, session

from models import *
from users import *
from app import app


@app.route('/')
def index():
    if session.get('username'): # this will be executed if 'username' is present in the session
        print "Logged-in: Found session"
        username = session['username']

        user_id = get_user_id(username)

        desserts = get_desserts(user_id)

        return render_template('index.html', desserts=desserts, username=username)
    else:
        print "Logged-in: No session"
        return render_template('login.html', error="Please login.")


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/submit-login', methods=['POST'])
def submit_login():
    #get form info
    user_username = request.form.get('username_field')
    user_password = request.form.get('password_field')

    print user_username

    # check for username
    user_login = get_user_by_username(user_username)
    if user_login:
        # check for password
        print "username is ok"
        print user_login.password
        print user_password
        if user_login.password == user_password:
            print "password is ok"
            session['username'] = user_username
            return redirect('/')
        else:
            print "password does not match"
            return render_template('login.html', error="Login credentials don't not work")
    else:
        print "password does not match"
        return render_template('login.html', error="Login credentials don't not work")


@app.route('/signup')
def signup_():
    return render_template('signup.html')

@app.route('/submit-signup', methods=['POST'])
def submit_signup():
    #get form info
    user_username = request.form.get('username_field')
    user_password = request.form.get('password_field')
    user_email = request.form.get('email_field')
    user_name = request.form.get('name_field')
    user_avatar = request.form.get('avatar_field')

    print user_username

    # check for duplicated username
    if get_user_by_username(user_username):
        return render_template('signup.html',error="Username already exists")

    # check for duplicated email
    elif get_user_by_email(user_email):
        return render_template('signup.html',error="Email already exists")

    # if no duplicates, create user
    else:
        try:
            user = create_user(user_username, user_email, user_password, user_name, user_avatar)
            session['username'] = user_username
            return redirect('/')
        except Exception as e:
            # Oh no, something went wrong!
            # We can access the error message via e.message:
            return render_template('signup.html', error=e.message)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if session.get('username'): # this will be executed if 'username' is present in the session
        print "Logged-in: Found session"
        username = session['username']

        if request.method == 'GET':
            return render_template('add.html')

        # Because we 'returned' for a 'GET', if we get to this next bit, we must
        # have received a POST

        # Get the incoming data from the request.form dictionary.
        # The values on the right, inside get(), correspond to the 'name'
        # values in the HTML form that was submitted.

        dessert_name = request.form.get('name_field')
        dessert_price = request.form.get('price_field')
        dessert_cals = request.form.get('cals_field')
        dessert_origin = request.form.get('origin_field')
        dessert_image_url = request.form.get('image_url_field')

        user_id = get_user_id(username)

        # Now we are checking the input in create_dessert, we need to handle
        # the Exception that might happen here.

        # Wrap the thing we're trying to do in a 'try' block:
        try:
            dessert = create_dessert(dessert_name, dessert_price, dessert_cals, dessert_origin, dessert_image_url, user_id)
            return render_template('add.html', dessert=dessert, username=username)
        except Exception as e:
            # Oh no, something went wrong!
            # We can access the error message via e.message:
            return render_template('add.html', error=e.message, username=username)

    else:
        print "Logged-in: No session"
        return render_template('login.html', error="Please login.")



@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if session.get('username'): # this will be executed if 'username' is present in the session
        print "Logged-in: Found session"
        username = session['username']

        # We could define this inside its own function but it's simple enough
        # that we don't really need to.

        dessert = Dessert.query.get(id)

        user_id = get_user_id(username)

        if request.method == 'GET':
            if dessert is None:
                return render_template('edit.html',dessert=dessert, error="The dessert ID do not exist.", username=username)
            if dessert.user_id != user_id:
                dessert = None
                return render_template('edit.html',dessert=dessert, error="You can't edit this dessert.", username=username)
            else:
                return render_template('edit.html',dessert=dessert, error=None, username=username)

        # Because we 'returned' for a 'GET', if we get to this next bit, we must
        # have received a POST

        # Get the incoming data from the request.form dictionary.
        # The values on the right, inside get(), correspond to the 'name'
        # values in the HTML form that was submitted.

        dessert_name = request.form.get('name_field')
        dessert_price = request.form.get('price_field')
        dessert_cals = request.form.get('cals_field')
        dessert_origin = request.form.get('origin_field')
        dessert_image_url = request.form.get('image_url_field')

        # Now we are checking the input in create_dessert, we need to handle
        # the Exception that might happen here.

        # Wrap the thing we're trying to do in a 'try' block:
        try:
            dessert = edit_dessert(dessert, dessert_name, dessert_price, dessert_cals, dessert_origin, dessert_image_url)
            return render_template('edit.html', dessert=dessert, success=True, username=username)
        except Exception as e:
            # Oh no, something went wrong!
            # We can access the error message via e.message:
            return render_template('edit.html', dessert=dessert, error=e.message, username=username)
    else:
        print "Logged-in: No session"
        return render_template('login.html', error="Please login.")



@app.route('/desserts/<id>')
def view_dessert(id):
    if session.get('username'): # this will be executed if 'username' is present in the session
        print "Logged-in: Found session"
        username = session['username']

        dessert = Dessert.query.get(id)

        user_id = get_user_id(username)


        if dessert is None:
            return render_template('details.html',dessert=dessert, error="The dessert ID do not exist.", username=username)
        if dessert.user_id != user_id:
            dessert = None
            return render_template('details.html',dessert=dessert, error="You can't view this dessert.", username=username)
        else:
            return render_template('details.html',dessert=dessert, error=None, username=username)

    else:
        print "Logged-in: No session"
        return render_template('login.html', error="Please login.")


@app.route('/delete/<id>')
def delete(id):
    if session.get('username'): # this will be executed if 'username' is present in the session
        print "Logged-in: Found session"
        username = session['username']

        user = get_user_by_username(username)
        user_id = user.id

        user_id = get_user_id(username)

        desserts = get_desserts(user_id)

        error = delete_dessert(id, user_id)


        return render_template('index.html', desserts=desserts, error="You can't edit this dessert.", username=username)
    else:
        print "Logged-in: No session"
        return render_template('login.html', error="Please login.", username=username)


@app.route('/search', methods=['POST'])
def search():
    if session.get('username'): # this will be executed if 'username' is present in the session
        print "Logged-in: Found session"
        username = session['username']

        # Because we 'returned' for a 'GET', if we get to this next bit, we must
        # have received a POST

        term = request.form.get('term')
        dessert = Dessert.query.filter_by(name=term).first()
        print

        if dessert:
            return render_template('details.html', dessert=dessert, username=username)
        else:
            # Oh no, something went wrong!
            # We can access the error message via e.message:
            return render_template('details.html', dessert=dessert, error="Name does not exist", username=username)
    else:
        print "Logged-in: No session"
        return render_template('login.html', error="Please login.")

@app.route('/order/<field>')
def order(field):
    if session.get('username'): # this will be executed if 'username' is present in the session
        print "Logged-in: Found session"
        username = session['username']

        if field == "name" or field == "price" or field == "calories":
            desserts = Dessert.query.order_by(field)
            return render_template('index.html', desserts=desserts)
        else:
            desserts = Dessert.query.all()
            return render_template('index.html', desserts=desserts)
    else:
        print "Logged-in: No session"
        return render_template('login.html', error="Please login.")

@app.route('/logout')
def logout_user():
    if session.get('username'): # this will be executed if 'username' is present in the session
        username = session['username']
        print "Logout: Deleting settion"
        del session['username']
    return redirect("/")
