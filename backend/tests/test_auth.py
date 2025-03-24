from models import db, Benutzer, Rolle
from unittest.mock import patch

def test_signin(client):
    with patch('models.Benutzer.query') as mock_query:
        user = Benutzer(name='Test User', email='test@example.com', rolle=Rolle.STUDENT)
        user.password = 'password'
        mock_query.filter_by.return_value.first.return_value = user

        response = client.post('/auth/signin', json={
            'email': 'test@example.com',
            'password': 'password'
        })
        assert response.status_code == 200
        assert 'access_token' in response.get_json()

def test_signin_invalid_credentials(client):
    with patch('models.Benutzer.query') as mock_query:
        mock_query.filter_by.return_value.first.return_value = None

        response = client.post('/auth/signin', json={
            'email': 'invalid@example.com',
            'password': 'password'
        })
        assert response.status_code == 401
        assert response.get_json()['message'] == 'Ungültige Anmeldedaten!'