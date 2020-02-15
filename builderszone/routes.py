import os 
from flask import Flask, flash, session
from flask import render_template, flash, redirect, request, abort, url_for
from builderszone import app,db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from builderszone.models import  Materials, Feedback, Gallery, Login, Project
from PIL import Image
from builderszone.forms import Material,RegistrationForm,LoginForm, Imageadd, RequestResetForm,ResetPasswordForm, Imageupdate, Accountform, Projects
from random import randint
from flask_mail import Message

@app.route('/')
def index():
    gallery=Gallery.query.all()
    return render_template('index.html', gallery=gallery)

@app.route('/playout')
def playout():
    return render_template("playout.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route("/plogin", methods=['GET', 'POST'])
def plogin():
    form = LoginForm()
    if form.validate_on_submit():
        user = Login.query.filter_by(email=form.email.data, usertype= 'architect',status = 'approved' ).first()
        user1 = Login.query.filter_by(email=form.email.data, usertype= 'user').first()
        user2 = Login.query.filter_by(email=form.email.data, usertype= 'admin').first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/aindex')
        if user1 and bcrypt.check_password_hash(user1.password, form.password.data):
            login_user(user1, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/uindex')
        if user2 and user2.password== form.password.data:
            login_user(user2, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/admin')
        if user2 and bcrypt.check_password_hash(user2.password, form.password.data):
            login_user(user2, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/admin')

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('plogin.html', title='Login', form=form)




@app.route("/registerarchitect", methods=['GET', 'POST'])
def registerarchitect():  
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new = Login(username= form.username.data, email=form.email.data, password=hashed_password,address = form.address.data, lincese = form.lincense.data , phone = form.contact.data,usertype= 'architect' )
        db.session.add(new)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect('/login')
    return render_template('registerarchitect.html',title='Register', form=form)

@app.route('/registeruser', methods=['GET','POST'])
def registeruser():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new = Login(username= form.username.data,email=form.email.data, password=hashed_password, address = 'null', lincese ='null' , phone = 'null'  ,    usertype= 'user', )
        db.session.add(new)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect('/plogin')
    return render_template('registeruser.html',title='Register', form=form)




@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')

@app.route('/registerwithpayment')
def registerwithpayment():
    return render_template("registerwithpayment.html")



@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/userlogin')
def userlogin():
    return render_template("userlogin.html")

@app.route('/adminlogin')
def adminlogin():
    return render_template("adminlogin.html")

@app.route('/architectlogin')
def architectlogin():
    return render_template("architectlogin.html")

@app.route('/aindex')
@login_required
def aindex():
    archi=Login.query.all()
    return render_template('aindex.html',archi=archi)

@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/architectview')
def architectview():
    archi=Login.query.filter_by(usertype='architect',status='approved').all()
    return render_template('architectview.html', archi=archi)

@app.route('/userview')
def userview():
    user = Login.query.filter_by(usertype= 'user').all()
    return render_template('userview.html', user= user)



@app.route('/projectadd',methods=['POST','GET'])
@login_required
def projectadd():
    material = Materials.query.all()
    form= Projects()
    view=""
    cost1 = ""
    if form.validate_on_submit():
        if form.pic.data:
            pic = save_picture(form.pic.data)
            view = pic
        empcost =  int(form.numemp.data)* int(form.days.data) +int(form.empcost.data)
        mat1=form.mat1.data
        mat11=Materials.query.get_or_404(mat1)
        mat1cost=int(mat11.price)*int(form.mat1q.data)
        mat2=form.mat2.data
        mat22=Materials.query.get_or_404(mat2)
        mat2cost=int(mat22.price)*int(form.mat2q.data)
        mat3=form.mat3.data
        mat33=Materials.query.get_or_404(mat3)
        mat3cost=int(mat33.price)*int(form.mat3q.data)
        mat4=form.mat4.data
        mat44=Materials.query.get_or_404(mat4)
        mat4cost=int(mat44.price)*int(form.mat4q.data)
        mat5=form.mat5.data
        mat55=Materials.query.get_or_404(mat5)
        mat5cost=int(mat55.price)*int(form.mat5q.data)
        matcost = int(mat1cost)+int(mat2cost)+int(mat3cost)+int(mat4cost)+int(mat5cost)
        totalcost = int(empcost)+int(matcost)+int(form.addcost.data)
        project = Project(owner = current_user.username,name= form.name.data, desc = form.desc.data,days=form.days.data, totalcost=totalcost ,addcost=form.addcost.data ,numemp =form.numemp.data ,empcost=  empcost  , matcost=  matcost  ,mat1= form.mat1.data  , mat2= form.mat2.data  ,mat3= form.mat3.data   ,mat4=form.mat4.data, mat5=form.mat5.data   ,mat1q= form.mat1q.data  , mat2q= form.mat2q.data  ,mat3q= form.mat3q.data   ,mat4q=form.mat4q.data, mat5q=form.mat5q.data   ,image = view)
        db.session.add(project)
        db.session.commit()
        return redirect('/aindex')
    return render_template('projectadd.html',form=form, material = material)




@app.route('/alayout')
def alayout():
    return render_template("alayout.html")



@app.route('/materialsadd',methods=['POST','GET'])
def materialsadd():
    form=Material()
    view=" "
    print("hello0")
    if form.validate_on_submit():
        if form.pic.data:
            pic = save_picture(form.pic.data)
            view = pic
        print(view)  
    
        gallery = Materials(name=form.name.data,brand=form.brand.data,price=form.price.data,image=view )
       
        db.session.add(gallery)
        db.session.commit()
        flash('image added')
        return redirect('/materialsview')
            
    return render_template('materialsadd.html',form=form)


@app.route('/uindex',methods=['POST','GET'])
@login_required
def uindex():
    if request.method=='POST':
        name= request.form['name1']
        email= request.form['email1']
        phone= request. form['phone1']
        subject= request. form['subject1']
        message= request. form['message1']
        new1 = Feedback(namee=name,email=email,phone=phone,subject=subject,message=message)
        try:
            db.session.add(new1)
            db.session.commit()
            return redirect('/uindex')

        except:
            return 'not add'  
    else:
        gallery=Gallery.query.all()
        material=Materials.query.all()
        user= Login.query.all()
        project = Project.query.all()
        return render_template('uindex.html',material=material,gallery=gallery,user=user,project=project)
    


@app.route('/materialsview')
def materialsview():
    material=Materials.query.all()
    return render_template('materialsview.html',material=material)



@app.route('/viewimage')
def viewimage():
    gallery=Gallery.query.all()
    return render_template('viewimage.html',gallery=gallery)



@app.route('/imageadd',methods=['POST','GET'])
def imageadd():
    form=Imageadd()

    if form.validate_on_submit():

        if form.pic.data:
            pic_file = save_picture(form.pic.data)
            view = pic_file
        print(view)  
    
        gallery = Gallery(name=form.name.data,img=view )
       
        db.session.add(gallery)
        db.session.commit()
        print(gallery)
        flash('image added')
        return redirect('/viewimage')
            
    return render_template('imageadd.html',form=form)


@app.route("/view/<int:id>", methods=['GET', 'POST'])
def update_post(id):
    gallery = Gallery.query.get_or_404(id)
    form = Imageupdate()
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            gallery.img = picture_file
        gallery.name = form.name.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/viewimage')
    elif request.method == 'GET':
        form.name.data = gallery.name
    image_file = url_for('static', filename='pics/' + gallery.img)
    return render_template('galleryupdate.html',form=form)
                           
@app.route("/view/<int:id>/.te")
def deleteimage(id):
    gallery =Gallery.query.get_or_404(id)
    db.session.delete(gallery)
    db.session.commit()
    flash('image has been deleted!', 'success')
    return redirect('/viewimage')


@app.route('/feedback')
def feedback():
    feedback1=Feedback.query.all()
    return render_template("feedback.html",feedback=feedback1)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delet = Materials.query.get_or_404(id)

    try:
        db.session.delete(task_to_delet)
        db.session.commit()
        return redirect('/materialsview')
    except:
        return 'There was a problem deleting that task'

@app.route('/materialsupdate/<int:id>', methods=['GET', 'POST'])
def update(id):
    material = Materials.query.get_or_404(id)
    
    form = Material()
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            material.image = picture_file
        material.name = form.name.data
        material.brand = form.brand.data
        material.price = form.price.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/materialsview')
    elif request.method == 'GET':
        form.name.data = material.name
        form.brand.data = material.brand
        form.price.data = material.price
    image_file = url_for('static', filename='pics/' + material.image)
    return render_template('materialsupdate.html',form=form, material=material)

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def save_picture(form_picture):
    random_hex = random_with_N_digits(14)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(random_hex) + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('resettoken', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)




@app.route("/resetrequest", methods=['GET', 'POST'])
def resetrequest():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Login.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect('/plogin')
    return render_template('resetrequest.html', title='Reset Password', form=form)




@app.route("/resetpassword/<token>", methods=['GET', 'POST'])
def resettoken(token):
    user = Login.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect('/resetrequest')
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect('/plogin')
    return render_template('resetpassword.html', title='Reset Password', form=form)






@app.route("/account1/<int:id>", methods=['GET', 'POST'])
def account1(id):
    form = Accountform()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit() 
        user = Login.query.filter_by(email=form.email.data, usertype= 'user').first()
        architect = Login.query.filter_by(email=form.email.data, usertype= 'architect').first()
        admin = Login.query.filter_by(email=form.email.data, usertype= 'admin').first()
        if user:
            return redirect('/uindex')
        if architect:
            return redirect('/aindex')
        if admin:
            return redirect('/admin')

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)







@app.route('/achangepassword', methods=['GET', 'POST'])
def achangepassword():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        flash('Your Password Has Been Changed')
        return redirect('/plogin')
    elif request.method == 'GET':
        hashed_password = current_user.password  
    return render_template('achangepassword.html', form=form)



@app.route('/aapprove')
def aapprove():
    user = Login.query.filter_by(usertype='architect',status = 'NULL')
    return render_template("aapprove.html",user=user)


@app.route('/aapprove1/<int:id>', methods= ['GET','POST'])
def aapprove1(id):
    log = Login.query.get_or_404(id)
    log.status = 'approved'
    approvemail(id)
    db.session.commit()
    return redirect('/aapprove')



def approvemail(id):
    log = Login.query.get_or_404(id)
    msg = Message('successful',
                  recipients=[log.email])
    msg.body = f''' your Account has been approved '''
    mail.send(msg) 


@app.route('/uprojectprofile/<int:id>')
def uprojectprofile(id):
    project=Project.query.get_or_404(id)
    mat1 = Materials.query.get_or_404(project.mat1)
    mat2 = Materials.query.get_or_404(project.mat2)
    mat3 = Materials.query.get_or_404(project.mat3)
    mat4 = Materials.query.get_or_404(project.mat4)
    mat5 = Materials.query.get_or_404(project.mat5)
    return render_template("uprojectprofile.html",project=project,mat1=mat1,mat2=mat2,mat3=mat3,mat4=mat4,mat5=mat5)