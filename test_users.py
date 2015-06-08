""" Test file for models.py.

    When models.py is complete, this file should completely pass.

    NOTE:
    To make these tests accurate, this file DELETES all content in the
    database first.
"""
import traceback

from users import *


def check_test(func):
    """ This is a decorator that simply prints out whether the function
        it calls succeeded or not. You don't need to edit this.
    """
    def func_wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            print ":) {} passed".format(func.__name__)
        except AssertionError:
            traceback.print_exc()
            print ":( {} failed".format(func.__name__)
    return func_wrapper


@check_test
def test_connection():
    # No longer needed, but let's update this to delete everything so we can
    # test
    User.query.delete()
    db.session.commit()


@check_test
def test_create():
    # Test that the create user function finishes cleanly
    result = create_user('test', 'test', 'test', 'test', 'test')
    # assert is a special Python keyword that throws an error if the thing it
    # is testing turns out not to be True. Our check_test decorator looks for
    # errors and tells us the test failed if it found any errors like this.
    assert result is not None
    assert isinstance(result, User)
    assert result.username == 'test'


@check_test
def test_create_worked():
    result = get_user_by_username('test')
    assert result is not None


@check_test
def test_get_user_by_id():
    result = get_user(1)
    assert result is not None


@check_test
def test_list_users():
    result = list_users()
    assert isinstance(result, list)   # isinstance says "is it of this type"
    assert len(result) > 0


@check_test
def test_update_user():
    result = update_user(1, password='newpass')
    assert result is not None
    assert isinstance(result, User)
    assert result.password == 'newpass'


for item in dir():
    """ Loop through all the defined items we know about (functions, etc).
        If the name starts with test_, assume it's a test function and run it!
    """
    if item.startswith('test_'):
        globals()[item]()
