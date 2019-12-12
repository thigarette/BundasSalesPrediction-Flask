from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired
import model as bundas
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'

csrf = CSRFProtect(app)

user_item_details = {}

print('lol')
class PredictionForm(FlaskForm):
    max_price = FloatField('Max Price', validators=[DataRequired])
    fat_content = SelectField('Fat Content',
                           choices=[('Low Fat', 'Low Fat'), ('Regular', 'Regular')])
    visibility = FloatField('Visibility', validators=[DataRequired])
    category = SelectField('Category',
                           choices=[('Baking Goods', 'Baking Goods'),
                                    ('Breads', 'Breads'),
                                    ('Breakfast', 'Breakfast'),
                                    ('Canned', 'Canned'),
                                    ('Dairy', 'Dairy'),
                                    ('Frozen Foods', 'Frozen Foods'),
                                    ('Fruits and Vegetables', 'Fruits and Vegetables'),
                                    ('Hard Drinks', 'Hard Drinks'),
                                    ('Health and Hygiene', 'Health and Hygiene'),
                                    ('Household', 'Household'),
                                    ('Meat', 'Meat'),
                                    ('Others', 'Others'),
                                    ('Seafood', 'Seafood'),
                                    ('Snack Foods', 'Snack Foods'),
                                    ('Soft Drinks', 'Soft Drinks'),
                                    ('Starchy Foods', 'Starchy Foods')])
    store_size = SelectField('Store Size',
                             choices=[('Small', 'Small'), ('Medium', 'Medium'), ('High', 'High'), ('Unknown', 'Unknown')])
    store_location_type = SelectField('Store Location Type',
                                      choices=[('Tier 1', 'Tier 1'), ('Tier 2', 'Tier 2'), ('Tier 3', 'Tier 3')])
    store_type = SelectField('Store Type',
                             choices=[('Supermarket Type 1', 'Supermarket Type 1'), ('Supermarket Type 2', 'Supermarket Type 2'), ('Supermarket Type 3', 'Supermarket Type 3'), ('Grocery Store', 'Grocery Store')])
    submit = SubmitField('Make Prediction')


@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        max_price = request.form["max_price"]
        fat_content = request.form["fat_content"]
        visibility = request.form["visibility"]
        category = request.form["category"]
        store_size = request.form["store_size"]
        store_location_type = request.form["store_location_type"]
        store_type = request.form["store_type"]

        user_item_details = {
            "FatContent": [fat_content],
            "Visibility": [visibility],
            "Category": [category],
            "Max_Price": [max_price],
            "Store_Size": [store_size],
            "Store_Location_Type": [store_location_type],
            "Store_Type": [store_type]
        }
        # user_item_details.extend([visibility, max_price, fat_content, category, store_size, store_location_type, store_type])
        encoded_item_details = bundas.preprocess_input(user_item_details)
        sales_prediction = bundas.model_predict(encoded_item_details)
        pred = sales_prediction[0].astype(str)
        print(sales_prediction[0])
        return "<p>Sales Prediction is "+pred+"</p>"
    form = PredictionForm()
    return render_template('custom.html', form=form)


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(threaded=True, port=5000)
