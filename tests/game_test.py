import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType, Game

class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@steve.com",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
        # Initiate reqest adn capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # SEED DATABASE WITH ONE GAME TYPE
        # This is needed because the API does not expose a /gametypes
        # endpoint for creating game types
        gametype = GameType()
        gametype.label = "Board game"
        gametype.save()

    def test_create_game(self):
        """
        Ensure we can create a new game.
        """
        # DEFINE GAME PROPERTIES
        url = "/games"
        data = {
            "title": "Checkers",
            "gameTypeId": 1,
            "numberOfPlayers": 2,
            "gamer": 1,
            "description": "Swell boardgame"
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)
        
        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["title"], "Checkers")
        self.assertEqual(json_response["gametype"]["id"], 1)
        self.assertEqual(json_response["number_of_players"], 2)
        self.assertEqual(json_response["gamer"]["id"], 1)
        self.assertEqual(json_response["description"], "Swell boardgame")

    def test_get_game(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the database with a game
        game = Game()
        game.title = "Checkers"
        game.gametype_id = 1
        game.number_of_players = 2
        game.gamer_id = 1
        game.description = "Great game"
        game.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/games/{game.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["title"], "Checkers")
        self.assertEqual(json_response["description"], "Great game")

    def test_change_game(self):
        """
        Ensure we can change an existing game
        """
        game = Game()
        game.title = "Checkers"
        game.gametype_id = 1
        game.number_of_players = 2
        game.gamer_id = 1
        game.description = "Great game"
        game.save()

        # Define new properties for game
        data = {
            "title": "Checkers!",
            "gameTypeId": 1,
            "numberOfPlayers": 2,
            "gamer": 1,
            "description": "Swell boardgame"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/games/{game.id}", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET game again to verify changes
        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["title"], "Checkers!")
        self.assertEqual(json_response["gametype"]["id"], 1)
        self.assertEqual(json_response["number_of_players"], 2)
        self.assertEqual(json_response["gamer"]["id"], 1)
        self.assertEqual(json_response["description"], "Swell boardgame")

    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """
        game = Game()
        game.title = "Checkers"
        game.gametype_id = 1
        game.number_of_players = 2
        game.gamer_id = 1
        game.description = "Great game"
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET game again to verify 404 response
        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
