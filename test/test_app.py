import unittest
import json
from server.app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.config['TESTING'] = True
        self.client = app.test_client()
        
    def test_connect(self):
        response = self.client.get('/login', query_string={'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 200)
        token = json.loads(response.data)['token']
        response = self.client.get('/send', query_string={"msg": "<on_enter>", "state": "<mono_begin>", "token": token})
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)['msg']
        next_state = json.loads(response.data)['next_state']
        timeout = json.loads(response.data)['timeout']
        exit = json.loads(response.data)['exit']
        with open('test/script/app_test/output1.txt', 'r') as f:
            expected_output = f.read()
        self.assertEqual(output, expected_output)
        self.assertEqual(next_state, 'welcome')
        self.assertEqual(timeout, 30)
        self.assertEqual(exit, False)
        
        response = self.client.get('/send', query_string={"msg": "<on_timeout>", "state": "welcome", "token": token})
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)['msg']
        next_state = json.loads(response.data)['next_state']
        timeout = json.loads(response.data)['timeout']
        exit = json.loads(response.data)['exit']
        with open('test/script/app_test/output2.txt', 'r') as f:
            expected_output = f.read()
        self.assertEqual(output, expected_output)
        self.assertEqual(next_state, 'welcome')
        self.assertEqual(timeout, 30)
        self.assertEqual(exit, False)
        
        response = self.client.get('/send', query_string={"msg": "exit", "state": "welcome", "token": token})
        self.assertEqual(response.status_code, 200)
        next_state = json.loads(response.data)['next_state']
        response = self.client.get('/send', query_string={"msg": "yes", "state": next_state, "token": token})
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)['msg']
        next_state = json.loads(response.data)['next_state']
        timeout = json.loads(response.data)['timeout']
        exit = json.loads(response.data)['exit']
        with open('test/script/app_test/output3.txt', 'r') as f:
            expected_output = f.read()
        print(next_state)
        self.assertEqual(output, expected_output)
        self.assertEqual(next_state, 'goodbye')
        self.assertEqual(timeout, 30)
        self.assertEqual(exit, True)
        
        response = self.client.get('/register', query_string={"username": "test", "password": "test"})
        self.assertEqual(response.status_code, 403)
        
        response = self.client.get('/register', query_string={"username": "test2", "password": "test"})
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/login', query_string={"username": "test2", "password": "test"})
        self.assertEqual(response.status_code, 200)
if __name__ == '__main__':
    unittest.main()
        
