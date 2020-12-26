
from flask import request
from flask_restful import Resource, abort, reqparse, fields, marshal_with
from flask_httpauth import HTTPBasicAuth

from my_app.product.models import Category
from my_app.auth.model.user import User
from my_app import user_manager
from my_app import db

resource_fields = {
    'id': fields.Integer,
    'name' : fields.String
}

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()

    if not user or not user_manager.verify_password(password_hash=user.password, password=password):
        return False

    #if username == "admin":
        #return True
    return True

class Base:
    def category_to_json(self,category):
        return {
            'id': category.id,
            'name': category.name,
        }

    def abort_if_doesnt_exist(self, id, json=True):
        category = Category.query.get(id)
        if category is None:
            abort(404, message="Categoría {} no existe".format(id))
        if json:
            return self.category_to_json(category)

        return category

class CategoryRestFul(Resource,Base):

    @auth.login_required
    @marshal_with(resource_fields, envelope="categoria")
    def get(self, id):
        return self.abort_if_doesnt_exist(id,False)

    @marshal_with(resource_fields, envelope="categoria")
    def patch(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help="No mandastes el nombre")#type=int
        args = parser.parse_args()

        #if not "name" in request.form:
        #    return abort(400, message="No esta presente el nombre")

        c = self.abort_if_doesnt_exist(id, False)

        c.name = args['name'] #request.form

        db.session.add(c)
        db.session.commit()

        return self.abort_if_doesnt_exist(c.id,False)

    def delete(self, id):

        c = self.abort_if_doesnt_exist(id, False)

        db.session.delete(c)
        db.session.commit()

        return {'msj':'ok'}


class CategoryRestFulList(Resource,Base):

    @marshal_with(resource_fields, envelope="categorias")
    def get(self):
        return Category.query.all()
        """res = []
        for c in categories:
            res.append(self.category_to_json(c))
        return res"""

    @marshal_with(resource_fields, envelope="categoria")
    def post(self):

        #if not "name" in request.form:
        #    return abort(400, message="No esta presente el nombre")
        
        parser = reqparse.RequestParser()
        parser.add_argument('name',required=True, help="No mandastes el nombre")
        args = parser.parse_args()

        c = Category(args['name'])
        db.session.add(c)
        db.session.commit()

        return c

class CategoryRestFulListSearch(Resource,Base):

    @marshal_with(resource_fields, envelope="categoria")
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('search',required=True, help="Tienes que especificar la busqueda")
        args = parser.parse_args()

        return Category.query.filter(Category.name.like('%{0}%'.format(args['search']))).all()