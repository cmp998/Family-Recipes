from pyrebase import pyrebase
from forms import CreateRecipeForm
import databaseconfig as cfg

config = {
    "apiKey": cfg.firebase["apiKey"],
    "authDomain": cfg.firebase["authDomain"],
    "databaseURL": cfg.firebase["databaseURL"],
    "projectId": cfg.firebase["projectId"],
    "storageBucket": cfg.firebase["storageBucket"],
    "messagingSenderId": cfg.firebase["messagingSenderId"],
    "appId": cfg.firebase["appId"],
    "measurementId": cfg.firebase["measurementId"]}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
from flask import *
app = Flask(__name__)
app.config['SECRET_KEY'] = cfg.firebase["secret_key"]
    
#print(db.child('recipes').get().val())

@app.route('/', methods=['GET', 'POST'])
def display():
    recipe_list = db.child('recipes').get().val()
    if recipe_list == None:
        return render_template('index.html')

    return render_template('index.html', reps=db.child('recipes').get().val())
    #return redirect(url_for('index'), reps=db.child('recipes').get().val())

@app.route('/create', methods=['GET', 'POST'])
def createRecipe():
    form = CreateRecipeForm()
    if form.validate_on_submit():
        #Add the recipe, maybe check that it doesn't exist already - 
        db.child("recipes").push({
            'title': form.title.data,
            'description' : form.description.data,
            'instructions': form.instructions.data.split(","),
            'ingredients': form.ingredients.data.split(","),
            'author': 'FILLER',
            'notes' : form.notes.data
        })
        #return redirect(url_for('index', reps=db.child('recipes').get().val(), notification=form.title.data))
        return render_template('create.html', title='New Recipe', form=form, notification=form.title.data)
    else:
        return render_template('create.html', title='New Recipe', form=form)


if __name__ == '__main__':
	app.run()