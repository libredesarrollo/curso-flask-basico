import json

from my_app.product.models import Category
from my_app.rest_api.helper.request import sendResJson
from my_app import app, db

from flask import request
from flask.views import MethodView

class CategoryApi(MethodView):
    def get(self, id=None):
        categories = Category.query.all()

        if id:
            category = Category.query.get(id)
            res = categoryToJson(category)
        else:
            res = []
            for c in categories:
                res.append(categoryToJson(c))

        return sendResJson(res,None,200)

def categoryToJson(category: Category):
    return {
                'id': category.id,
                'name': category.name
            }


category_view = CategoryApi.as_view('category_view')
app.add_url_rule('/api/categories/',
view_func=category_view,
methods=['GET'])
app.add_url_rule('/api/categories/<int:id>',
view_func=category_view,
methods=['GET'])




