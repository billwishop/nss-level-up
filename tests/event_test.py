import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import Event, Game, GameType

class EventTests(APITestCase):
    def setUp(self):
        """
        Create a new account and set up a game
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@steve.com",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those eventz!!"
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Seed database with one game type
        gametype = GameType()
        gametype.label = "Board game"
        gametype.save()

        # Seed database with one game
        game = Game()
        game.title = "Checkers"
        game.gametype_id = 1
        game.number_of_players = 2
        game.gamer_id = 1
        game.description = "Great game"
        game.save()

    def test_create_event(self):
        """
        Ensure we can create a new event.
        """
        # Define event properties
        url = "/events"
        data = {
            "time": "2020-08-29T13:24:27.172Z",
            "gameId": 1,
            "location": "Nashville, TN",
            "scheduler": 1
        }

        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Inititiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["event_time"], "2020-08-29T13:24:27.172Z")
        self.assertEqual(json_response["game"]["id"], 1)
        self.assertEqual(json_response["location"], "Nashville, TN")
        self.assertEqual(json_response["scheduler"]["user"]["id"], 1)

    def test_get_event(self):
        """
        Ensure we can get an existing event.
        """

        # Seed the database with an event
        event = Event()
        event.event_time = "2020-08-29T13:24:27.172Z"
        event.game_id = 1
        event.location = "Nashville, TN"
        event.scheduler_id = 1
        event.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/events/{event.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the event was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["event_time"], "2020-08-29T13:24:27.172000Z")
        self.assertEqual(json_response["game"]["id"], 1)
        self.assertEqual(json_response["location"], "Nashville, TN")
        self.assertEqual(json_response["scheduler"]["user"]["id"], 1)

    def test_change_event(self):
        """
        Ensure we can change an existing event
        """
        event = Event()
        event.event_time = "2020-08-29T13:24:27.172Z"
        event.game_id = 1
        event.location = "Nashville, TN"
        event.scheduler_id = 1
        event.save()

        # Define new properties for game
        data = {
            "time": "2020-08-29T13:24:27.172000Z",
            "gameId": 1,
            "location": "Columbus, GA",
            "scheduler": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/events/{event.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET Event again to verify changes
        response = self.client.get(f"/events/{event.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["event_time"], "2020-08-29T13:24:27.172000Z")
        self.assertEqual(json_response["game"]["id"], 1)
        self.assertEqual(json_response["location"], "Columbus, GA")
        self.assertEqual(json_response["scheduler"]["user"]["id"], 1)

    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """
        event = Event()
        event.event_time = "2020-08-29T13:24:27.172Z"
        event.game_id = 1
        event.location = "Nashville, TN"
        event.scheduler_id = 1
        event.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET again to verify 404
        response = self.client.get(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

