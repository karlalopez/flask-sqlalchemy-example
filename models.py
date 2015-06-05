from app import db


class Dessert(db.Model):
    # See http://flask-sqlalchemy.pocoo.org/2.0/models/#simple-example
    # for details on the column types.

    # We always need an id
    id = db.Column(db.Integer, primary_key=True)

    # A dessert has a name, a price and some calories:
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    calories = db.Column(db.Integer)

    def __init__(self, name, price, calories):
        self.name = name
        self.price = price
        self.calories = calories

    def calories_per_dollar(self):
        if self.calories:
            return self.calories / self.price


class Menu(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name


def create_dessert(new_name, new_price, new_calories):
    # Create a dessert with the provided input.

    # We need every piece of input to be provided.

    # Can you think of other ways to write this following check?
    if new_name is None or new_price is None or new_calories is None:
        raise Exception("Need name, price and calories!")

    # They can also be empty strings if submitted from a form
    if new_name == '' or new_price == '' or new_calories == '':
        raise Exception("Need name, price and calories!")

    # Check for price
    if int(new_price) > 50:
        raise Exception("A bit too pricey!")

    # Check for calories
    if int(new_calories) > 1000:
        raise Exception("No one should eat that")

    #Check duplicates
    if Dessert.query.filter_by(name=new_name).first():
        raise Exception("Already in the database")


    # This line maps to line 16 above (the Dessert.__init__ method)
    dessert = Dessert(new_name, new_price, new_calories)

    # Actually add this dessert to the database
    db.session.add(dessert)

    # Save all pending changes to the database

    try:
        db.session.commit()
        return dessert
    except:
        # If something went wrong, explicitly roll back the database
        db.session.rollback()


def edit_dessert(dessert, new_name, new_price, new_calories):
    # Edit a dessert with the provided input.


    # Can you think of other ways to write this following check?
    if new_name is None or new_price is None or new_calories is None:
        raise Exception("Need name, price and calories!")

    # They can also be empty strings if submitted from a form
    if new_name == '' or new_price == '' or new_calories == '':
        raise Exception("Need name, price and calories!")

    # Check for price
    if int(new_price) > 50:
        raise Exception("A bit too pricey!")

    # Check for calories
    if int(new_calories) > 1000:
        raise Exception("No one should eat that")

    # This line maps to line 16 above (the Dessert.__init__ method)
    dessert.name = new_name
    dessert.price = new_price
    dessert.calories = new_calories

    # Save all pending changes to the database

    try:
        db.session.commit()
        return dessert
    except:
        # If something went wrong, explicitly roll back the database
        db.session.rollback()



def delete_dessert(id):

    dessert = Dessert.query.get(id)

    if dessert:
        # We store the name before deleting it, because we can't access it
        # afterwards.
        dessert_name = dessert.name
        db.session.delete(dessert)

        try:
            db.session.commit()
            return "Dessert {} deleted".format(dessert_name)
        except:
            # If something went wrong, explicitly roll back the database
            db.session.rollback()
            return "Something went wrong"
    else:
        return "Dessert not found"


if __name__ == "__main__":

    # Run this file directly to create the database tables.
    print "Creating database tables..."
    db.create_all()
    print "Done!"
