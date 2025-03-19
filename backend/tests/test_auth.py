from models import db, Benutzer, Rolle

def test_signup(client):
    response = client.post('/auth/signup', json={
        'name': 'New User',
        'email': 'newuser@example.com',
        'password': 'newpassword'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Benutzer erfolgreich registriert!'

    # Verify user is in the database
    user = Benutzer.query.filter_by(email='newuser@example.com').first()
    assert user is not None
    assert user.name == 'New User'
    assert user.check_password('newpassword')

def test_signup_existing_user(client):
    user = Benutzer(name='Existing User', email='existing@example.com', rolle=Rolle.STUDENT)
    user.password = 'password'
    db.session.add(user)
    db.session.commit()

    response = client.post('/auth/signup', json={
        'name': 'Existing User',
        'email': 'existing@example.com',
        'password': 'password'
    })
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Benutzer existiert bereits!'

def test_signin(client):
    user = Benutzer(name='Test User', email='test@example.com', rolle=Rolle.STUDENT)
    user.password = 'password'
    db.session.add(user)
    db.session.commit()

    response = client.post('/auth/signin', json={
        'email': 'test@example.com',
        'password': 'password'
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_signin_invalid_credentials(client):
    response = client.post('/auth/signin', json={
        'email': 'invalid@example.com',
        'password': 'password'
    })
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Ungültige Anmeldedaten!'
