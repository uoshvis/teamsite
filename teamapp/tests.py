from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class TeamTest(TestCase):

    link = '/api/teams/'
    data = {
        'team_name': 'SuperTeam',
        'members': [
            {
                "id": 1,
                "username": "Akita",
                "email": "akita@one.lt",
                "firstname": "Ana",
                "lastname": "Aliba",
                "role": "defender",
            },

            {
                "id": 2,
                "username": "Bakia",
                "email": "bakita@one.lt",
                "firstname": "Bana",
                "lastname": "Mago",
                "role": "important"
            },
        ]
    }

    wrong_data = {
        'team_name': {'SuperTeam': 'ball'},
        'members': [
            {'firstname': 'Avava'},
            {'firstname': 'Bavava'}
        ]
    }

    def test_new_team(self):
        '''
        Test new team creation
        '''
        client = APIClient()
        response = client.post(self.link, self.data, format='json')
        self.assertEqual(response.data.get('team_name'), self.data['team_name'])
        self.assertTrue(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_wrong_field(self):
        '''
        Test wrong field entry
        '''
        client = APIClient()
        response = client.post(self.link, self.wrong_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_team(self):
        '''
        Test post and delete
        '''
        client = APIClient()
        response = client.post(self.link, self.data, format='json')
        self.assertEqual(response.data.get('team_name'), self.data['team_name'])
        delete_response = client.delete(self.link + str(response.data.get('id')) + '/')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        response_after = client.get(self.link + str(response.data.get('id')) + '/')
        self.assertEqual(response_after.status_code, status.HTTP_404_NOT_FOUND)

    def test_update(self):
        '''
        Test delete old and update.
        '''
        client = APIClient()
        response = client.post(self.link, self.data, format='json')
        members = response.data.get('members')
        member_ids = [member.get('id') for member in members]
        update_data = {
            'id': response.data.get('id'),
            'team_name': 'The Best',
            'members': [
                {
                    "id": min(member_ids),
                    "username": "Akita-new",
                    "email": "akita@one.lt",
                    "firstname": "Ana",
                    "lastname": "Aliba",
                    "role": "defender",
                },
            ]
        }

        response = client.put(self.link + str(response.data.get('id')) + '/',
                              update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_data['members'], response.data['members'])
        self.assertEqual((update_data), dict(response.data))

    def test_delete_on_update(self):
        '''
        Test delete old and create new on update
        '''
        client = APIClient()
        response = client.post(self.link, self.data, format='json')
        members = response.data.get('members')
        member_ids = [member.get('id') for member in members]
        update_data = {
            'id': response.data.get('id'),
            'team_name': 'The Best',
            'members': [
                {
                    "id": min(member_ids),
                    "username": "Akita-new",
                    "email": "akita@one.lt",
                    "firstname": "Ana",
                    "lastname": "Aliba",
                    "role": "defender",
                },

                {
                    "id": max(member_ids) + 1,
                    "username": "User",
                    "email": "user@one.lt",
                    "firstname": "user",
                    "lastname": "userlast",
                    "role": "user_defender",
                },
            ]
        }
        response = client.put(self.link + str(response.data.get('id')) + '/',
                              update_data, format='json')
        [member.pop('id') for member in update_data['members']]
        [member.pop('id') for member in response.data.get('members')]
        for mem_dict in update_data['members']:
            self.assertIn(mem_dict, response.data.get('members'))

    def test_unique_username(self):
        '''
        Test delete old and create new on update
        '''
        client = APIClient()
        response = client.post(self.link, self.data, format='json')
        members = response.data.get('members')
        member_ids = [member.get('id') for member in members]
        update_data = {
            'id': response.data.get('id'),
            'team_name': 'The Best',
            'members': [
                {
                    "id": min(member_ids),
                    "username": "Akita",
                    "email": "akita@one.lt",
                    "firstname": "Ana",
                    "lastname": "Aliba",
                    "role": "defender",
                },

                {
                    "id": max(member_ids) + 1,
                    "username": "Akita",
                    "email": "user@one.lt",
                    "firstname": "user",
                    "lastname": "userlast",
                    "role": "user_defender",
                },
            ]
        }
        response = client.put(self.link + str(response.data.get('id')) + '/',
                              update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unique_email(self):
        '''
        Test delete old and create new on update
        '''
        client = APIClient()
        response = client.post(self.link, self.data, format='json')
        members = response.data.get('members')
        member_ids = [member.get('id') for member in members]
        update_data = {
            'id': response.data.get('id'),
            'team_name': 'The Best',
            'members': [
                {
                    "id": min(member_ids),
                    "username": "Akita",
                    "email": "akita@one.lt",
                    "firstname": "Ana",
                    "lastname": "Aliba",
                    "role": "defender",
                },

                {
                    "id": max(member_ids) + 1,
                    "username": "User",
                    "email": "akita@one.lt",
                    "firstname": "user",
                    "lastname": "userlast",
                    "role": "user_defender",
                },
            ]
        }
        response = client.put(self.link + str(response.data.get('id')) + '/',
                              update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


'''

{
    "id": 5,
    "team_name": "TeamTwo" ,
    "members": [
        {
            "id": 1,
            "username": "Akita",
            "email": "Akita@one.lt",
            "firstname": "Ana",
            "lastname": "Aliba",
            "role": "defenderr"
        },
        {
            "id": 2,
            "username": "Bakia",
            "email":"bakita@one.lt",
            "firstname": "Bana",
            "lastname": "Mago",
            "role": "important"
        },
                {
            "id": 3,
            "username": "Cakita",
            "email": "Cakita@one.lt",
            "firstname": "Caba",
            "lastname": "Vago",
            "role": "manager"
        }

    ]
}

'''
