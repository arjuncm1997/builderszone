import os 
from flask import Flask, flash, session
from flask import render_template, flash, redirect, request, abort, url_for
from builderszone import app,db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from builderszone.models import  Materials, Feedback, Gallery, Login, Sort,Project, Credit, Pay
from PIL import Image
from builderszone.forms import Material,RegistrationForm,LoginForm,Cod,Amountform, Creditcard,Paypal,Imageadd, RequestResetForm,ResetPasswordForm, Imageupdate, Accountform, Projects
from random import randint
from flask_mail import Message

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        name= request.form['name1']
        email= request.form['email1']
        phone= request. form['phone1']
        subject= request. form['subject1']
        message= request. form['message1']
        new1 = Feedback(namee=name,email=email,phone=phone,subject=subject,message=message,usertype='public')
        try:
            db.session.add(new1)
            db.session.commit()
            return redirect('/')

        except:
            return 'not add'  
    else:
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
        new = Login(username= form.username.data, email=form.email.data, password=form.password.data,address = form.address.data, lincese = form.lincense.data , phone = form.contact.data,usertype= 'architect' )
        db.session.add(new)
        db.session.commit()
        flash('Your account has been created! waiting for approval', 'success')
        return redirect('/plogin')
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
@app.route('/architectreject')
def architectreject():
    archi=Login.query.filter_by(usertype='architect',status='rejected').all()
    return render_template('architectreject.html', archi=archi)

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
        empcost1 =  int(form.numemp.data)* int(form.days.data) *int(form.empcost.data)
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
        mat6=form.mat6.data
        mat66=Materials.query.get_or_404(mat6)
        mat6cost=int(mat66.price)*int(form.mat6q.data)
        mat7=form.mat7.data
        mat77=Materials.query.get_or_404(mat7)
        mat7cost=int(mat77.price)*int(form.mat7q.data)
        mat8=form.mat8.data
        mat88=Materials.query.get_or_404(mat8)
        mat8cost=int(mat88.price)*int(form.mat8q.data)
        mat9=form.mat9.data
        mat99=Materials.query.get_or_404(mat9)
        mat9cost=int(mat99.price)*int(form.mat9q.data)
        mat10=form.mat10.data
        mat1010=Materials.query.get_or_404(mat10)
        mat10cost=int(mat1010.price)*int(form.mat10q.data)
        matcost = int(mat1cost)+int(mat2cost)+int(mat3cost)+int(mat4cost)+int(mat5cost)+int(mat6cost)+int(mat7cost)+int(mat8cost)+int(mat9cost)+int(mat10cost)
        totalcost = int(empcost1)+int(matcost)+int(form.addcost.data)
        project = Project(owner = current_user.username,name= form.name.data, desc = form.desc.data,days=form.days.data, totalcost=totalcost ,addcost=form.addcost.data ,numemp =form.numemp.data ,empcost1=  empcost1  , empcost =form.empcost.data,matcost=  matcost  ,mat1= form.mat1.data  , mat2= form.mat2.data  ,mat3= form.mat3.data   ,mat4=form.mat4.data, mat5=form.mat5.data ,mat6=form.mat6.data , mat7=form.mat7.data,mat8=form.mat8.data,mat9=form.mat9.data,mat10=form.mat10.data,mat1q= form.mat1q.data  , mat2q= form.mat2q.data  ,mat3q= form.mat3q.data   ,mat4q=form.mat4q.data, mat5q=form.mat5q.data  , mat6q=form.mat6q.data , mat7q=form.mat7q.data, mat8q=form.mat8q.data, mat9q=form.mat9q.data, mat10q=form.mat10q.data,image = view)
        db.session.add(project)
        db.session.commit()
        return redirect('/aindex')
    return render_template('projectadd.html',form=form, material = material)



@app.route('/aprojectsview')
def aprojectsview():
    project=Project.query.all()
    return render_template("aprojectsview.html",project=project)

@app.route('/aprojectsedit/<int:id>',methods=['POST','GET'])
@login_required
def aprojectsedit(id):
    material = Materials.query.all()
    form= Projects()
    view=""
    cost1 = ""
    mat11=""
    project = Project.query.get_or_404(id)
    if form.validate_on_submit():
        if form.pic.data:
            pic = save_picture(form.pic.data)
            project.image = pic
        empcost1 =  int(form.numemp.data)* int(form.days.data) *int(form.empcost.data)
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
        mat6=form.mat6.data
        mat66=Materials.query.get_or_404(mat6)
        mat6cost=int(mat66.price)*int(form.mat6q.data)
        mat7=form.mat7.data
        mat77=Materials.query.get_or_404(mat7)
        mat7cost=int(mat77.price)*int(form.mat7q.data)
        mat8=form.mat8.data
        mat88=Materials.query.get_or_404(mat8)
        mat8cost=int(mat88.price)*int(form.mat8q.data)
        mat9=form.mat9.data
        mat99=Materials.query.get_or_404(mat9)
        mat9cost=int(mat99.price)*int(form.mat9q.data)
        mat10=form.mat10.data
        mat1010=Materials.query.get_or_404(mat10)
        mat10cost=int(mat1010.price)*int(form.mat10q.data)
        matcost = int(mat1cost)+int(mat2cost)+int(mat3cost)+int(mat4cost)+int(mat5cost)+int(mat6cost)+int(mat7cost)+int(mat8cost)+int(mat9cost)+int(mat10cost)
        totalcost = int(empcost1)+int(matcost)+int(form.addcost.data)
        project.name = form.name.data
        project.desc = form.desc.data
        project.days = form.days.data
        project.totalcost = totalcost
        project.addcost=form.addcost.data
        project.numemp =form.numemp.data 
        project.empcost1= empcost1
        project.empcost=  form.empcost.data 
        project.matcost=  matcost  
        project.mat1= form.mat1.data  
        project.mat2= form.mat2.data  
        project.mat3= form.mat3.data   
        project.mat4=form.mat4.data
        project.mat5=form.mat5.data   
        project.mat1q= form.mat1q.data  
        project.mat2q= form.mat2q.data  
        project.mat3q= form.mat3q.data   
        project.mat4q=form.mat4q.data
        project.mat5q=form.mat5q.data 
        db.session.commit()
        return redirect('/aprojectsview')
    elif request.method == 'GET':
        form.name.data = project.name
        form.desc.data = project.desc
        form.days.data = project.days
        form.numemp.data = project.numemp
        form.empcost.data = project.empcost
        form.addcost.data = project.addcost
        form.mat1q.data = project.mat1q
        form.mat2q.data = project.mat2q
        form.mat3q.data = project.mat3q
        form.mat4q.data = project.mat4q
        form.mat5q.data = project.mat5q
        form.mat6q.data = project.mat6q
        form.mat7q.data = project.mat7q
        form.mat8q.data = project.mat8q
        form.mat9q.data = project.mat9q
        form.mat10q.data = project.mat10q
        mat1 = project.mat1
        mat11= Materials.query.get_or_404(mat1)
        mat2 = project.mat2
        mat22= Materials.query.get_or_404(mat2)
        mat3 = project.mat3
        mat33= Materials.query.get_or_404(mat3)
        mat4 = project.mat1
        mat44= Materials.query.get_or_404(mat4)
        mat5 = project.mat5
        mat55= Materials.query.get_or_404(mat5)
        mat6 = project.mat6
        mat66= Materials.query.get_or_404(mat6)
        mat7 = project.mat7
        mat77= Materials.query.get_or_404(mat7)
        mat8 = project.mat8
        mat88= Materials.query.get_or_404(mat8)
        mat9 = project.mat9
        mat99= Materials.query.get_or_404(mat9)
        mat10 = project.mat10
        mat1010= Materials.query.get_or_404(mat10)

    return render_template('aprojectsedit.html',project=project,view=view,form=form, material = material,mat11=mat11,mat22=mat22,mat33=mat33,mat44=mat44,mat55=mat55,mat66=mat66,mat77=mat77,mat88=mat88,mat99=mat99,mat1010=mat1010)


@app.route('/aprojectdelete/<int:id>')
def aprojectdelete(id):
    delete = Project.query.get_or_404(id)
    try:
        db.session.delete(delete)
        db.session.commit()
        return redirect('/aprojectsview')
    except:
        return 'can not delete'

@app.route('/usort/<int:id>',methods=['POST','GET'])
def usort(id):
    material = Materials.query.all()
    project = Project.query.get_or_404(id)
    form=Projects()
    if form.validate_on_submit():
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
        mat6=form.mat6.data
        mat66=Materials.query.get_or_404(mat6)
        mat6cost=int(mat66.price)*int(form.mat6q.data)
        mat7=form.mat7.data
        mat77=Materials.query.get_or_404(mat7)
        mat7cost=int(mat77.price)*int(form.mat7q.data)
        mat8=form.mat8.data
        mat88=Materials.query.get_or_404(mat8)
        mat8cost=int(mat88.price)*int(form.mat8q.data)
        mat9=form.mat9.data
        mat99=Materials.query.get_or_404(mat9)
        mat9cost=int(mat99.price)*int(form.mat9q.data)
        mat10=form.mat10.data
        mat1010=Materials.query.get_or_404(mat10)
        mat10cost=int(mat1010.price)*int(form.mat10q.data)
        matcost = int(mat1cost)+int(mat2cost)+int(mat3cost)+int(mat4cost)+int(mat5cost)+int(mat6cost)+int(mat7cost)+int(mat8cost)+int(mat9cost)+int(mat10cost)
        totalcost = int(project.empcost1)+int(matcost)+int(project.addcost)
        sort = Sort(projectowner= project.owner,sortowner = current_user.username,projectname=project.name,projectid= project.id,totalcost=totalcost , matcost=  matcost  ,mat1= form.mat1.data  , mat2= form.mat2.data  ,mat3= form.mat3.data   ,mat4=form.mat4.data, mat5=form.mat5.data   ,mat1q= form.mat1q.data  , mat2q= form.mat2q.data  ,mat3q= form.mat3q.data   ,mat4q=form.mat4q.data, mat5q=form.mat5q.data)
        db.session.add(sort)
        db.session.commit()
        return redirect('/uindex')
    elif request.method == 'GET':
        form.name.data = project.name
        form.desc.data = project.desc
        form.days.data = project.days
        form.numemp.data = project.numemp
        form.empcost.data = project.empcost
        form.addcost.data = project.addcost
        form.mat1q.data = project.mat1q
        form.mat2q.data = project.mat2q
        form.mat3q.data = project.mat3q
        form.mat4q.data = project.mat4q
        form.mat5q.data = project.mat5q
        form.mat6q.data = project.mat6q
        form.mat7q.data = project.mat7q
        form.mat8q.data = project.mat8q
        form.mat9q.data = project.mat9q
        form.mat10q.data = project.mat10q
        mat1 = project.mat1
        mat11= Materials.query.get_or_404(mat1)
        mat2 = project.mat2
        mat22= Materials.query.get_or_404(mat2)
        mat3 = project.mat3
        mat33= Materials.query.get_or_404(mat3)
        mat4 = project.mat1
        mat44= Materials.query.get_or_404(mat4)
        mat5 = project.mat5
        mat55= Materials.query.get_or_404(mat5)
        mat6 = project.mat6
        mat66= Materials.query.get_or_404(mat6)
        mat7 = project.mat7
        mat77= Materials.query.get_or_404(mat7)
        mat8 = project.mat8
        mat88= Materials.query.get_or_404(mat8)
        mat9 = project.mat9
        mat99= Materials.query.get_or_404(mat9)
        mat10 = project.mat10
        mat1010= Materials.query.get_or_404(mat10)
    return render_template("usort.html",form=form ,material=material,project=project,mat11=mat11,mat22=mat22,mat33=mat33,mat44=mat44,mat55=mat55,mat66=mat66,mat77=mat77,mat88=mat88,mat99=mat99,mat1010=mat1010)


@app.route('/usorted')
def usorted():
    sort = Sort.query.filter_by(sortowner=current_user.username).all()

    return render_template("usorted.html",sort=sort)


@app.route('/usortedprofile/<int:id>')
def usortedprofile(id):
    sort = Sort.query.get_or_404(id)
    projectid = sort.projectid
    project=Project.query.get_or_404(projectid)
    mat1=Materials.query.get_or_404(sort.mat1)
    mat2=Materials.query.get_or_404(sort.mat2)
    mat3=Materials.query.get_or_404(sort.mat3)
    mat4=Materials.query.get_or_404(sort.mat4)
    mat5=Materials.query.get_or_404(sort.mat5)
    mat6 = Materials.query.get_or_404(project.mat6)
    mat7 = Materials.query.get_or_404(project.mat7)
    mat8 = Materials.query.get_or_404(project.mat8)
    mat9 = Materials.query.get_or_404(project.mat9)
    mat10 = Materials.query.get_or_404(project.mat10)
    return render_template("usortedprofile.html",sort=sort,project=project,mat1=mat1,mat2=mat2,mat3=mat3,mat4=mat4,mat5=mat5,mat6=mat6,mat7=mat7,mat8=mat8,mat9=mat9,mat10=mat10)    



@app.route('/auserrequest')
def auserrequest():
    sort = Sort.query.filter_by(projectowner=current_user.username).all()
    return render_template("auserrequest.html",sort=sort)

@app.route('/auserrequestprofile/<int:id>')
def auserrequestprofile(id):
    sort = Sort.query.get_or_404(id)
    projectid = sort.projectid
    project=Project.query.get_or_404(projectid)
    mat1=Materials.query.get_or_404(sort.mat1)
    mat2=Materials.query.get_or_404(sort.mat2)
    mat3=Materials.query.get_or_404(sort.mat3)
    mat4=Materials.query.get_or_404(sort.mat4)
    mat5=Materials.query.get_or_404(sort.mat5)
    mat6 = Materials.query.get_or_404(project.mat6)
    mat7 = Materials.query.get_or_404(project.mat7)
    mat8 = Materials.query.get_or_404(project.mat8)
    mat9 = Materials.query.get_or_404(project.mat9)
    mat10 = Materials.query.get_or_404(project.mat10)
    return render_template("auserrequestprofile.html",sort=sort,project=project,mat1=mat1,mat2=mat2,mat3=mat3,mat4=mat4,mat5=mat5,mat6=mat6,mat7=mat7,mat8=mat8,mat9=mat9,mat10=mat10)    

@app.route('/auserapprove/<int:id>',methods=['POST','GET'])
def auserapprove(id):
    sort = Sort.query.get_or_404(id)
    sort.action = 'approved'
    db.session.commit()
    return redirect('/auserrequest')

@app.route('/auserreject/<int:id>',methods=['POST','GET'])
def auserreject(id):
    sort = Sort.query.get_or_404(id)
    sort.action = 'rejected'
    db.session.commit()
    return redirect('/auserrequest')
    
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
        new1 = Feedback(namee=name,email=email,phone=phone,subject=subject,message=message,usertype='user')
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
    feedback1=Feedback.query.filter_by(usertype='public').all()
    return render_template("feedback.html",feedback=feedback1)
@app.route('/ufeedback')
def ufeedback():
    feedback1=Feedback.query.filter_by(usertype='user').all()
    return render_template("ufeedback.html",feedback=feedback1)

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
    password = log.password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    log.password = hashed_password
    log.status = 'approved'
    approvemail(id,password)
    db.session.commit()
    return redirect('/aapprove')

@app.route('/areject/<int:id>', methods= ['GET','POST'])
def areject(id):
    log = Login.query.get_or_404(id)
    log.status = 'rejected'
    rejectmail(id)
    db.session.commit()
    return redirect('/aapprove')

def rejectmail(id):
    log = Login.query.get_or_404(id)
    msg = Message('successful',
                  recipients=[log.email])
    msg.body = f''' your Account has been rejected '''
    mail.send(msg) 

def approvemail(id,password):
    log = Login.query.get_or_404(id)
    print(password)
    msg = Message('successful',
                  recipients=[log.email])
    msg.body = f''' your Account has been approved .. 
        username is {log.username} and password is {password}'''
    mail.send(msg) 


@app.route('/uprojectprofile/<int:id>')
def uprojectprofile(id):
    project=Project.query.get_or_404(id)
    mat1 = Materials.query.get_or_404(project.mat1)
    mat2 = Materials.query.get_or_404(project.mat2)
    mat3 = Materials.query.get_or_404(project.mat3)
    mat4 = Materials.query.get_or_404(project.mat4)
    mat5 = Materials.query.get_or_404(project.mat5)
    mat6 = Materials.query.get_or_404(project.mat6)
    mat7 = Materials.query.get_or_404(project.mat7)
    mat8 = Materials.query.get_or_404(project.mat8)
    mat9 = Materials.query.get_or_404(project.mat9)
    mat10 = Materials.query.get_or_404(project.mat10)
    return render_template("uprojectprofile.html",project=project,mat1=mat1,mat2=mat2,mat3=mat3,mat4=mat4,mat5=mat5,mat6=mat6,mat7=mat7,mat8=mat8,mat9=mat9,mat10=mat10)




@app.route('/payment/<int:id>')
def payment(id):
    form = Cod()
    form1 = Creditcard()
    form2 = Paypal()
    sort = Sort.query.get_or_404(id)
    return render_template('payment.html',sort = sort,form=form,form1 =form1,form2=form2)


# def sendmail():
#     msg = Message('successful',
#                   recipients=[current_user.email])
#     msg.body = f''' your Order Succsessfully Completed...   Track Your Order   'http://127.0.0.1:5000/login' '''
#     mail.send(msg)

@app.route('/creditcard/<int:id>',methods = ['GET','POST'])
@login_required
def creditcard(id):
    form = Cod()
    form1 = Creditcard()
    form2 = Paypal()
    sort = Sort.query.get_or_404(id)
    if form1.validate_on_submit():
        sort.payment = 'credit card'
        sort.booking = 'booked'
        sendmail()
        db.session.commit()
    if form1.validate_on_submit():
        credit = Credit(sortid = sort.id,sortowner=current_user.username,projectowner=sort.projectowner,name = form1.name.data,card= form1.number.data ,cvv=form1.cvv.data , expdate=form1.date.data)
        db.session.add(credit)
        db.session.commit()
        return redirect('/successfull')
    return render_template('payment.html',sort = sort,form=form ,form1 =form1,form2=form2)

@app.route('/paypal/<int:id>',methods = ['GET','POST'])
@login_required
def paypal(id):
    form = Cod()
    form1 = Creditcard()
    form2 = Paypal()
    sort = Sort.query.get_or_404(id)
    if form2.validate_on_submit():
        sort.payment = 'credit card'
        sort.booking = 'booked'
        sendmail()
        db.session.commit()
    if form2.validate_on_submit():
        pay = Pay(sortid = sort.id,sortowner = current_user.username,projectowner=sort.projectowner,name = form2.name.data,card= form2.number.data ,cvv=form2.cvv.data , validdate=form2.date.data)
        db.session.add(pay)
        db.session.commit()
        return redirect('/successfull')
    return render_template('payment.html',sort=sort,form=form ,form1 =form1,form2=form2)


def sendmail():
    msg = Message('successful',
                  recipients=[current_user.email])
    msg.body = f''' your transaction completed successfullyy '''
    mail.send(msg)



@app.route('/successfull')
@login_required
def successful1():
    return render_template("successfull.html")


@app.route('/ubookedproject')
def ubookedproject():
    sort = Sort.query.filter_by(sortowner=current_user.username,booking='booked').all()
    return render_template("ubookedproject.html",sort=sort)


@app.route('/abookedproject')
def abookedproject():
    sort = Sort.query.filter_by(projectowner=current_user.username,booking='booked').all()
    return render_template("abookedproject.html",sort=sort)

@app.route('/uamount/<int:id>',methods = ['GET','POST'])
def uamount(id):
    form=Amountform()
    sort=Sort.query.get_or_404(id)
    if form.validate_on_submit():
        sort.amount = form.amount.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/payment/'+str(sort.id))
    return render_template("uamount.html",form=form)


