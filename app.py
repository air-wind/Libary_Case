from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)

# 配置类
class Config():
    SECRET_KEY = "JNDJFNNNFDNF"
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@192.168.35.158:3306/flaskbook"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

app.config.from_object(Config)

# 数据类
db = SQLAlchemy(app)
class Author(db.Model):
    __tablename__ = "fb_author"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30), unique=True)
    book = db.relation("Book", backref="author")

class Book(db.Model):
    __tablename__ = "fb_book"
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String(30), unique=True)
    is_del = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey("fb_author.id"))

# 模板类
class BookSubmit(FlaskForm):
    author = StringField(label="作者", validators=[DataRequired("请输入作者名称")])
    book = StringField(label="图书", validators=[DataRequired("请输入图书名称")])

    submit = SubmitField(label="提交")

# 路由
@app.route('/')
def index():
    form = BookSubmit()
    book_li = Book.query.filter_by(is_del=False).all()
    books_info = list()
    for book in book_li:
        book_info = {
            "book": book.book,
            "author": book.author.author
        }
        books_info.append(book_info)

    data = {
        "form": form,
        "books_info": books_info
    }
    if form.validate_on_submit():
        pass
    return render_template("index.html", **data)


if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    # au_xi = Author(author='我吃西红柿')
    # au_qian = Author(author='萧潜')
    # au_san = Author(author='唐家三少')
    # db.session.add_all([au_xi, au_qian, au_san])
    # db.session.commit()
    #
    # bk_xi = Book(book='吞噬星空', author_id=au_xi.id)
    # bk_xi2 = Book(book='寸芒', author_id=au_qian.id)
    # bk_qian = Book(book='飘渺之旅', author_id=au_qian.id)
    # bk_san = Book(book='冰火魔厨', author_id=au_san.id)
    # db.session.add_all([bk_xi, bk_xi2, bk_qian, bk_san])
    # db.session.commit()
    app.run()
