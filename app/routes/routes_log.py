from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.models import User, Family
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, ManageUserDataForm

@app.route('/login', methods=['GET', 'POST'])
def login():
    # We can use '.is_authenticated' because we defined the model 'User'
    # with the class 'UserMixin'
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # The 'validate_on_submit()' method handles submissions and implicitly handles the 'request'
    # object, so we don't have to import the object 
    if form.validate_on_submit():
        # We query the database for a 'User' with the email adress submitted by
        # the form LoginForm()
        # Check if the input is an email address
        if '@' in form.identificator.data:
            user = User.query.filter_by(email=form.identificator.data).first()
        else:
            user = User.query.filter_by(username=form.identificator.data).first()
        
        # We check if no user was found with the given email or if the password in 
        # LoginForm() does not match the password in the database for the user
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        print(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        family_name = form.family_name.data
        new_family = form.new_family_name.data
        
        if family_name:
            family = Family.query.filter_by(name=form.family_name.data).first()
            if family:
                user = User(username=form.username.data, email=form.email.data, alias=form.alias.data, family_id=family.id, is_admin=False)
            else:
                flash('The provided family code does not match any existing family. Please check the family code or create a new family.')
                return redirect(url_for('register'))
            
        elif new_family:
            existing_family = Family.query.filter_by(name=form.new_family_name.data).first()
            if existing_family:
                flash('The provided new family name is already taken. Please choose another name or join an existing family.')
                return redirect(url_for('register'))
            else:
                print(new_family)
                family = Family(name=form.new_family_name.data)
                db.session.add(family)
                db.session.commit()
                user = User(username=form.username.data, email=form.email.data, alias=form.alias.data, family_id=family.id, is_admin=True)
        else:
            flash('Please provide a family name or create a new family')
            return redirect(url_for('register'))
            
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route('/manage_user_data', methods=['GET', 'POST'])
@login_required
def manage_user_data():
    form = ManageUserDataForm()

    if form.validate_on_submit():
        changes_made = False

        if form.alias.data:
            current_user.alias = form.alias.data
            changes_made = True

        if form.email.data:
            current_user.email = form.email.data
            changes_made = True

        if form.current_password.data and form.new_password.data:
            if current_user.check_password(form.current_password.data):
                current_user.set_password(form.new_password.data)
                changes_made = True
            else:
                flash('Incorrect current password. Please try again.')

        if changes_made:
            db.session.commit()
            flash('Your user data has been updated.')
            return redirect(url_for('index'))

    elif request.method == 'GET': # This line is not strictly necessary
        form.alias.data = current_user.alias
        form.email.data = current_user.email

    return render_template('manage_user_data.html', form=form)
