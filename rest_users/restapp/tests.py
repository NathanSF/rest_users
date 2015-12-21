from rest_framework import status
from rest_framework.test import APITestCase


class TestUser(APITestCase):
    def test_user(self):
        """
        Ensure we can create a user, get users, update a user and delete user.
        Test for proper status codes.
        """
        # Add first user
        response = self.client.post('/users/',
            {'username': 't1', 'first_name':'t1', 'last_name':'last',
            'email': 't1@test.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get users
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

        # Get this particular user
        response = self.client.get('/users/1/')
        self.assertEqual(response.data['first_name'], 't1')
        self.assertEqual(response.data['email'], 't1@test.com')

        # Get user doesn't exist
        response = self.client.get('/users/2/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Don't allow post to existing user
        response = self.client.post('/users/1/',
            {'username': 't2', 'first_name':'t2', 'last_name':'last',
            'email': 't2@test.com1'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Add second user
        response = self.client.post('/users/',
            {'username': 't2', 'first_name':'t2', 'last_name':'last',
            'email': 't2@test.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get users should now have count 2
        response = self.client.get('/users/')
        self.assertEqual(response.data["count"], 2)

        # Add user with same username should fail
        response = self.client.post('/users/',
            {'username': 't2', 'first_name':'t2', 'last_name':'last',
            'email': 't2@test.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Attempt to get user that does not exist should return 404
        response = self.client.get('/users/5/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Delete returns 404 if doesn't exist
        response = self.client.delete('/users/5/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Delete an existing user, user count should now be 1
        response = self.client.delete('/users/2/')
        response = self.client.get('/users/')
        self.assertEqual(response.data["count"], 1)

        '''TODO Missing Unit Tests'''
        # Add user missing username/email should fail
        # Update user with PUT
        # PUT bad data should fail
        # PUT returns 404 if doesn't exist
