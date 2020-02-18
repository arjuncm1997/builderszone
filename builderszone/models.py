from builderszone import db,login_manager, app
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

 
@login_manager.user_loader
def load_user(id):
    return Login.query.get(int(id))






class Login(db.Model, UserMixin):

    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    lincese = db.Column(db.String(80),default='NULL')
    phone = db.Column(db.String(80),default='NULL')
    address = db.Column(db.String(80),default='NULL')
    status=db.Column(db.String(80),default='NULL')
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    usertype = db.Column(db.String(80), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Login.query.get(user_id)

    def __repr__(self):
        return f"Login('{self.username}', '{self.password}','{self.usertype}','{self.email}', '{self.image_file}')"





class Materials(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    brand = db.Column(db.String(80))
    price = db.Column(db.String(80))
    image = db.Column(db.String(20), default='default.jpg')
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namee= db.Column(db.VARCHAR)
    email= db.Column(db.VARCHAR)
    phone= db.Column(db.Integer)
    subject= db.Column(db.VARCHAR)
    message= db.Column(db.VARCHAR)
    usertype= db.Column(db.VARCHAR)

class Gallery(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.VARCHAR)
    img = db.Column(db.String(20), nullable=False, default='default.jpg')
    
    def __repr__(self):
        return f"Gallery('{self.name}', '{self.img}')"


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(200))
    name = db.Column(db.String(20))
    desc = db.Column(db.String(50))
    numemp = db.Column(db.String(200))
    empcost = db.Column(db.String(200))
    empcost1 = db.Column(db.String(200))
    days = db.Column(db.String(200))
    matcost = db.Column(db.String(200))
    mat1 = db.Column(db.String(200))
    mat2 = db.Column(db.String(200))
    mat3 = db.Column(db.String(200))
    mat4 = db.Column(db.String(200))
    mat5 = db.Column(db.String(200))
    mat6 = db.Column(db.String(200))
    mat7 = db.Column(db.String(200))
    mat8 = db.Column(db.String(200))
    mat9 = db.Column(db.String(200))
    mat10 = db.Column(db.String(200))
    mat1q = db.Column(db.String(200))
    mat2q= db.Column(db.String(200))
    mat3q = db.Column(db.String(200))
    mat4q= db.Column(db.String(200))
    mat5q= db.Column(db.String(200))
    mat6q= db.Column(db.String(200))
    mat7q= db.Column(db.String(200))
    mat8q= db.Column(db.String(200))
    mat9q= db.Column(db.String(200))
    mat10q= db.Column(db.String(200))
    addcost  = db.Column(db.String(200))
    totalcost = db.Column(db.String(20))
    image = db.Column(db.String(20),nullable=False,default= 'default.jpg')



class Sort(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projectowner = db.Column(db.String(200))
    projectname= db.Column(db.String(200))
    projectid = db.Column(db.String(200))
    sortowner = db.Column(db.String(200))
    matcost = db.Column(db.String(200))
    mat1 = db.Column(db.String(200))
    mat2 = db.Column(db.String(200))
    mat3 = db.Column(db.String(200))
    mat4 = db.Column(db.String(200))
    mat5 = db.Column(db.String(200))
    mat6 = db.Column(db.String(200))
    mat7 = db.Column(db.String(200))
    mat8 = db.Column(db.String(200))
    mat9 = db.Column(db.String(200))
    mat10 = db.Column(db.String(200))
    mat1q = db.Column(db.String(200))
    mat2q= db.Column(db.String(200))
    mat3q = db.Column(db.String(200))
    mat4q= db.Column(db.String(200))
    mat5q= db.Column(db.String(200))
    mat6q = db.Column(db.String(200))
    mat7q= db.Column(db.String(200))
    mat8q = db.Column(db.String(200))
    mat9q= db.Column(db.String(200))
    mat10q= db.Column(db.String(200))
    addcost  = db.Column(db.String(200))
    totalcost = db.Column(db.String(20))
    action = db.Column(db.String(20))
    payment = db.Column(db.String(20))
    booking = db.Column(db.String(20))
    amount = db.Column(db.String(200))



class Credit(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    sortid = db.Column(db.String)
    sortowner = db.Column(db.String)
    projectowner = db.Column(db.String)
    name = db.Column(db.String(200))
    card = db.Column(db.String(200))
    cvv = db.Column(db.String(200))
    expdate = db.Column(db.String(200))
    amount = db.Column(db.String(200))


class Pay(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    sortid = db.Column(db.String)
    sortowner = db.Column(db.String)
    projectowner = db.Column(db.String)
    name = db.Column(db.String(200))
    card = db.Column(db.String(200))
    cvv = db.Column(db.String(200))
    validdate = db.Column(db.String(200))
    amount = db.Column(db.String(200))
