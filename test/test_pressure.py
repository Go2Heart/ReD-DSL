from threading import Thread
import unittest
import json
from server.app import app

class TestPressure(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.config['TESTING'] = True
        self.client = app.test_client()
        
    def pressure(self, index):
        """Simulate a user tops up his/her balance and withdraw afterwards for 100 times"""
        response = self.client.get('/register', query_string={"username": "test" + str(index), "password": "test"})
        self.assertEqual(response.status_code, 200)
        token = json.loads(response.data)['token']
        response = self.client.get('/send', query_string={"msg": "<on_enter>", "state": "<mono_begin>", "token": token})
        current_state = json.loads(response.data)['next_state']
        
        for i in range(100):
            response = self.client.get('/send', query_string={"msg": "topup", "state": current_state, "token": token})
            self.assertEqual(response.status_code, 200)
            current_state = json.loads(response.data)['next_state']
            
            response = self.client.get('send', query_string={"msg": "101", "state": current_state, "token": token})
            self.assertEqual(response.status_code, 200)
            current_state = json.loads(response.data)['next_state']
            
            response = self.client.get('/send', query_string={"msg": "withdraw", "state": current_state, "token": token})
            self.assertEqual(response.status_code, 200)
            current_state = json.loads(response.data)['next_state']
            
            response = self.client.get('/send', query_string={"msg": "100", "state": current_state, "token": token})
            self.assertEqual(response.status_code, 200)
            current_state = json.loads(response.data)['next_state']
        
        response = self.client.get('/send', query_string={"msg": "balance", "state": current_state, "token": token})
        self.assertEqual(response.status_code, 200)
        balance = json.loads(response.data)['msg'].split("\n")[0]
        self.assertEqual(balance, "Your balance is 200.0")
            
    def test_pressure(self):
        """Simulate 100 users tops up his/her balance and withdraw afterwards for 100 times"""
        threads = []
        for i in range(100):
            t = Thread(target=self.pressure, args=(i,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
          


if __name__ == '__main__':
    unittest.main()
            
        
        
        