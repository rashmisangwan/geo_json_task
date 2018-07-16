import unittest
import requests
import json

from app import app
from database_helpers import delete_record

class TestPostLocation(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_post_location_no_data(self):
        response = self.tester.post('/post_location')
        response = json.loads(response.data)
        self.assertEqual(response['status']['code'], 'INCORRECT_DATA')

    def test_post_location_invalid_data(self):
        response = self.tester.post('/post_location', data={"lat": 28.7, "long": 's76.s7', "pincode": '10114'})
        response = json.loads(response.data)
        self.assertEqual(response['status']['code'], 'INCORRECT_DATA')

    def test_post_location_insufficient_data(self):
        response = self.tester.post('/post_location', data={"lat": 28.7, "long": 76.7})
        response = json.loads(response.data)
        self.assertEqual(response['status']['code'], 'VALIDATION_ERROR :: pincode, latitude and longitude are compulsary')

    def test_post_location_correct_data(self):
        response = self.tester.post('/post_location', data={"lat": 51.16, "long": 10.45, "pincode": "new_pincode"})
        response = json.loads(response.data)
        self.assertEqual(response['status']['code'], 'SUCCESS')

    def test_post_location_duplicate_data(self):
        response = self.tester.post('/post_location', data={"lat": 51.16, "long": 10.45, "pincode": "new_pincode"})
        response = json.loads(response.data)
        self.assertEqual(response['status']['code'], 'ALREADY_EXISTS')
        # Deleting the test entry created in this test
        delete_record("new_pincode")

class TestGetUsingPostgres(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_get_using_postgres_no_data(self):
        response = self.tester.get('/get_using_postgres')
        response = json.loads(response.data)
        self.assertEqual(response['status']['code'], 'INCORRECT_DATA')

    def test_get_using_postgres_invalid_data(self):
        response = self.tester.get('/get_using_postgres?lat=28.9&long=s76.s7&distance=10114')
        response = json.loads(response.data)
        self.assertEqual(response['status']['code'], 'INCORRECT_DATA')

    def test_get_using_postgres_insufficient_data(self):
        response = self.tester.get('/get_using_postgres?lat=28.9&long=76.5667')
        response = json.loads(response.data)
        self.assertEqual(response['status']['code'], 'INCORRECT_DATA')

    def test_get_using_postgres_correct_data(self):
        response = self.tester.get('/get_using_postgres?lat=28.9&long=76.5667&distance=11')
        response = json.loads(response.data)
        self.assertEqual(response['status']['code'], 'SUCCESS')
        self.assertEqual(len(response['payload']), 7)

    def tearDown(self):
        pass

class TestGetUsingSelf(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_get_using_self_no_data(self):
        response = self.tester.get('/get_using_self')
        response = json.loads(response.data)
        self.assertEqual(response['status']['code'], 'INCORRECT_DATA')

    def test_get_using_self_invalid_data(self):
        response = self.tester.get('/get_using_self?lat=28.9&long=s76.s7&distance=10114')
        response = json.loads(response.data)
        self.assertEqual(response['status']['code'], 'INCORRECT_DATA')

    def test_get_using_self_insufficient_data(self):
        response = self.tester.get('/get_using_self?lat=28.9&long=76.5667')
        response = json.loads(response.data)
        self.assertEqual(response['status']['code'], 'INCORRECT_DATA')

    def test_get_using_self_correct_data(self):
        response = self.tester.get('/get_using_self?lat=28.9&long=76.5667&distance=11')
        response = json.loads(response.data)
        self.assertEqual(response['status']['code'], 'SUCCESS')
        self.assertEqual(len(response['payload']), 7)

    def tearDown(self):
        pass

class TestGetContainingArea(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_get_containing_area_no_data(self):
        response = self.tester.get('/get_containing_area')
        response = json.loads(response.data)
        self.assertEqual(response['status']['code'], 'INCORRECT_DATA')

    def test_get_containing_area_invalid_data(self):
        response = self.tester.get('/get_containing_area?lat=28.9&long=s76.s7')
        response = json.loads(response.data)
        self.assertEqual(response['status']['code'], 'INCORRECT_DATA')

    def test_get_containing_area_correct_data(self):
        response = self.tester.get('/get_containing_area?lat=77.0202548599243&long=28.5146691862972')
        response = json.loads(response.data)
        self.assertEqual(response['status']['code'], 'SUCCESS')
        self.assertEqual(len(response['payload']), 1)
        self.assertEqual(response['payload'][0]["place_name"], "Gurgaon")

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()