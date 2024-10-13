import unittest
import json
from app import app, init_db
import tempfile
import os

class KanbanAPITestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.client = app.test_client()
        with app.app_context():
            init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def register(self, username, password, organization):
        return self.client.post('/register', data=dict(
            username=username,
            password=password,
            organization=organization
        ), follow_redirects=True)

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_register_and_login(self):
        rv = self.register('testuser', 'testpass', 'testorg')
        assert b'Registration successful' in rv.data
        rv = self.login('testuser', 'testpass')
        assert b'Enhanced Digital Kanban System' in rv.data

    def test_add_card(self):
        self.register('testuser', 'testpass', 'testorg')
        self.login('testuser', 'testpass')
        rv = self.client.post('/api/cards', data=json.dumps(dict(
            item='Test Item',
            quantity=10,
            status='Full',
            location='Warehouse A',
            supplier='Supplier X'
        )), content_type='application/json')
        assert rv.status_code == 201
        assert b'Test Item' in rv.data

    def test_get_cards(self):
        self.register('testuser', 'testpass', 'testorg')
        self.login('testuser', 'testpass')
        self.client.post('/api/cards', data=json.dumps(dict(
            item='Test Item',
            quantity=10,
            status='Full',
            location='Warehouse A',
            supplier='Supplier X'
        )), content_type='application/json')
        rv = self.client.get('/api/cards')
        assert rv.status_code == 200
        assert b'Test Item' in rv.data

    def test_update_card(self):
        self.register('testuser', 'testpass', 'testorg')
        self.login('testuser', 'testpass')
        rv = self.client.post('/api/cards', data=json.dumps(dict(
            item='Test Item',
            quantity=10,
            status='Full',
            location='Warehouse A',
            supplier='Supplier X'
        )), content_type='application/json')
        card_id = json.loads(rv.data)['id']
        rv = self.client.put(f'/api/cards/{card_id}', data=json.dumps(dict(
            status='In Use'
        )), content_type='application/json')
        assert rv.status_code == 200
        assert b'Card updated successfully' in rv.data

    def test_delete_card(self):
        self.register('testuser', 'testpass', 'testorg')
        self.login('testuser', 'testpass')
        rv = self.client.post('/api/cards', data=json.dumps(dict(
            item='Test Item',
            quantity=10,
            status='Full',
            location='Warehouse A',
            supplier='Supplier X'
        )), content_type='application/json')
        card_id = json.loads(rv.data)['id']
        rv = self.client.delete(f'/api/cards/{card_id}')
        assert rv.status_code == 200
        assert b'Card deleted successfully' in rv.data

    def test_organization_separation(self):
        self.register('user1', 'pass1', 'org1')
        self.login('user1', 'pass1')
        self.client.post('/api/cards', data=json.dumps(dict(
            item='Org1 Item',
            quantity=10,
            status='Full',
            location='Warehouse A',
            supplier='Supplier X'
        )), content_type='application/json')
        self.logout()

        self.register('user2', 'pass2', 'org2')
        self.login('user2', 'pass2')
        self.client.post('/api/cards', data=json.dumps(dict(
            item='Org2 Item',
            quantity=20,
            status='In Use',
            location='Warehouse B',
            supplier='Supplier Y'
        )), content_type='application/json')

        rv = self.client.get('/api/cards')
        assert b'Org2 Item' in rv.data
        assert b'Org1 Item' not in rv.data

if __name__ == '__main__':
    unittest.main()