from flask import Flask, render_template, g, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)
# 创建数据库管理类
db = SQLAlchemy(app)

# 创建flask脚本管理类
manager = Manager(app)

# 创建数据库迁移类
Migrate(app, db)

# 将数据库迁移命令添加到脚本
manager.add_command("db", MigrateCommand)

# 配置类
class Config():
    SECRET_KEY = "JNDJFNNNFDNF"
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@192.168.35.158:3306/flaskbook"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

app.config.from_object(Config)

# 创建数据库模型
class Author(db.Model):
    __tablename__ = "fb_author"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30), unique=True)
    book = db.relation("Book", backref="author")
    mobile = db.Column(db.String(12), unique=True)

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
@app.route('/', methods=["GET", "POST"])
def index():
    form = BookSubmit()
    if form.validate_on_submit():
        book =  form.book.data
        author = form.author.data
        add_book(book, author)


    book_li = Book.query.filter_by(is_del=False).all()
    books_info = list()
    for book in book_li:
        book_info = {
            "book_id": book.id,
            "book": book.book,
            "author": book.author.author
        }
        books_info.append(book_info)

    data = {
        "form": form,
        "books_info": books_info
    }
    return render_template("index.html", **data)

@app.route("/delete/<int:bookid>")
def delete(bookid):
    Book.query.filter_by(id=bookid).update({"is_del": True})
    db.session.commit()
    return redirect(url_for("index"))

def add_book(book, author):
    # 判断书籍是否存在
    flag = Book.query.filter_by(book=book).first()
    if flag is None:
        #不存在
        # 向数据库中添加信息
        curent_author = Author(author=author)
        db.session.add(curent_author)
        db.session.commit()
        curent_book = Book(book=book, author_id = curent_author.id)
        db.session.add(curent_book)
        db.session.commit()
    else:
        #存在
        if flag.is_del:
            flag.is_del = False
            db.session.add(flag)
            db.session.commit()
        else:
            flash("已经存在!")


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
    manager.run()
