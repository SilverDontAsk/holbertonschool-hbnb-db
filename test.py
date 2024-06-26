import pytest
from src import create_app, db
from src.models.user import User
from src.models.place import Place
from src.models.review import Review

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')
    testing_client = flask_app.test_client()

    with flask_app.app_context():
        db.create_all()
        yield testing_client
        db.drop_all()

def test_create_review(test_client):
    user = User(id='1', name='John Doe', email='john@example.com')
    place = Place(id='1', name='Test Place', city_id='1', host_id='1')
    db.session.add(user)
    db.session.add(place)
    db.session.commit()

    review_data = {
        'place_id': '1',
        'user_id': '1',
        'comment': 'Great place!',
        'rating': 4.5
    }

    review = Review.create(review_data)
    assert review.id is not None
    assert review.place_id == '1'
    assert review.user_id == '1'
    assert review.comment == 'Great place!'
    assert review.rating == 4.5

def test_update_review(test_client):
    review = Review.query.filter_by(comment='Great place!').first()
    updated_data = {
        'comment': 'Excellent place!',
        'rating': 5.0
    }

    updated_review = Review.update(review.id, updated_data)
    assert updated_review.comment == 'Excellent place!'
    assert updated_review.rating == 5.0

def test_delete_review(test_client):
    review = Review.query.filter_by(comment='Excellent place!').first()
    db.session.delete(review)
    db.session.commit()

    deleted_review = Review.query.get(review.id)
    assert deleted_review is None

