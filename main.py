from flask import Flask,render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# CREATING a database in SQLalchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)
#after this we have to add  fields in database

#FROMAT TO CREATE A TABLE INSIDE SQLITE DATABASE - 
class Todo(db.Model):

    Sno = db.Column(db.Integer, primary_key= True)   
    Title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    Time = db.Column(db.DateTime,default = datetime.utcnow)

    # using this function we are going to return(fetch) the data submitted inside the form

    def __repr__(self) -> str: #USING THIS FUNCTION TO RETURN DATA 
        return f"{self.Sno} - {self.Title}"
    

@app.route("/",methods =['GET','POST'])
def home():
    if request.method =='POST':
        todo_title = request.form['title']
        todo_desc = request.form['desc']
        data  = Todo(Title = todo_title,description = todo_desc )
        db.session.add(data)
        db.session.commit()
    '''
        todo = Todo(Title = "Todo", description = "Testing first Todo!")
    db.session.add(todo) # add new data 
    db.session.commit() #commit the changes in the database 

'''
    alltodo = Todo.query.all()
    return render_template('first.html', alltodo=alltodo)


@app.route("/delete/<int:Sno>")
def delete(Sno):
    todo = Todo.query.get(Sno)  # Use .get() to retrieve the Todo by its primary key (Sno)
    todo = Todo.query.filter_by(Sno= Sno).first() 
    
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@app.route("/update/<int:Sno>",methods =['GET','POST'])
def update(Sno):
    if request.method == 'POST':
        todo_title = request.form['title']
        todo_desc = request.form['desc']
        data  = Todo.query.filter_by(Sno= Sno).first() 
        data.Title = todo_title
        data.description = todo_desc
        db.session.add(data)
        db.session.commit()

        return redirect("/")
    
#    todo = Todo.query.get(Sno)  # Use .get() to retrieve the Todo by its primary key (Sno)
#    todo = Todo.query.filter_by(Sno= Sno).first() 
    todo = Todo.query.get(Sno)
    return render_template("update.html",todo =todo)

@app.route("/dev")
def dev():
    return render_template("dev.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug= True) 