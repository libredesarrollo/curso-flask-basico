from my_app import db
from my_app.auth.model.user import User

from decimal import Decimal

from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, DecimalField, SelectField, HiddenField, FormField, FieldList, validators
from wtforms.validators import InputRequired, NumberRange, ValidationError, DataRequired 
from flask_user.forms import RegisterForm, ChangeUsernameForm

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    #file = db.Column(db.String(255))
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'),
        nullable=False)
    #category = db.relationship('Category', backref='products',lazy=True)

    def __init__(self, name, price, category_id):
        self.name = name
        self.price = price
        self.category_id = category_id
        #self.file = file

    def __repr__(self):
        return '<Product %r>' % (self.name)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'price': self.price,
            'name': self.name
        }

class ProductForm(FlaskForm):
    name = StringField('Nombre', validators=[InputRequired()])
    price = DecimalField('Precio', validators=[InputRequired(), NumberRange(min=Decimal('0.0'))])
    category_id = SelectField('Categoría', coerce=int)
    file = FileField('Archivo') #, validators=[FileRequired()]

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    products = db.relationship('Product', backref='category',lazy=True)
    #products = db.relationship('Product',lazy='dynamic', backref=db.backref('category',lazy='select'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % (self.name)

def check_category2(form, field):
    res = Category.query.filter_by(name = field.data).first()
    if res:
        raise ValidationError("La categoría: %s ya fue tomada" % field.data)

def check_category(contain=True):
    def _check_category(form, field):
        print(form.id.data)
        if contain:
            res = Category.query.filter(Category.name.like("%"+field.data+"%")).first()
        else:
            res = Category.query.filter(Category.name.like(field.data)).first()


        # validacion para cuando queremos CREAR un registro con el mismo nombre
        if res and form.id.data == "":
            raise ValidationError("La categoría: %s ya fue tomada" % field.data)

        # validacion para cuando queramos ACTUALIZAR un registro con el mismo nombre
        # ya existe un categoria con el mismo nombre a la categoria que queremos actualizar
        if res and form.id.data and res.id != int(form.id.data):
            raise ValidationError("La categoría: %s ya fue tomada" % field.data)
        
    return _check_category

class PhoneForm(FlaskForm):
    phoneCode = StringField("Código teléfono")
    countryCode = StringField("Código país")
    phone = StringField("Teléfono")

class PhoneForm2(FlaskForm):
    phoneCode2 = StringField("Código teléfono2")

class CategoryForm(PhoneForm):#, PhoneForm2
    name = StringField('Nombre', validators=[InputRequired(), check_category(contain=False)])
    id = HiddenField('Id')
    recaptcha = RecaptchaField()
    #phonelist = FormField(PhoneForm)
    #phones = FieldList(FormField(PhoneForm))

class CustomRegisterForm(RegisterForm):
    # Add a country field to the Register form
    country = StringField('Country', validators=[DataRequired()])

class CustomChangeUsernameForm(ChangeUsernameForm):

    new_username = StringField('New Username', validators=[
        validators.DataRequired('Username is required'),
    ])

    def validate_new_username(form, field):

        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('This Username is already in use. Please try another one.')
