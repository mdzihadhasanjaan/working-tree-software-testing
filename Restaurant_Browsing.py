"""
Module for restaurant browsing and database simulation.
"""

import unittest  # Module-level imports must be at the top


class RestaurantBrowsing:
    """
    A class for browsing restaurants in a database based on various
    criteria like cuisine type, location, and rating.

    Attributes:
        database (RestaurantDatabase): An instance that holds restaurant data.
    """

    def __init__(self, database):
        """
        Initialize with a reference to a restaurant database.

        Args:
            database (RestaurantDatabase): The database with restaurant info.
        """
        self.database = database

    def search_by_cuisine(self, cuisine_type):
        """
        Search for restaurants by cuisine type.

        Args:
            cuisine_type (str): The type of cuisine (e.g., "Italian").

        Returns:
            list: Restaurants that match the cuisine type.
        """
        return [
            restaurant
            for restaurant in self.database.get_restaurants()
            if restaurant["cuisine"].lower() == cuisine_type.lower()
        ]

    def search_by_location(self, location):
        """
        Search for restaurants by location.

        Args:
            location (str): The location (e.g., "Downtown").

        Returns:
            list: Restaurants in the specified location.
        """
        return [
            restaurant
            for restaurant in self.database.get_restaurants()
            if restaurant["location"].lower() == location.lower()
        ]

    def search_by_rating(self, min_rating):
        """
        Search for restaurants by minimum rating.

        Args:
            min_rating (float): The minimum rating (e.g., 4.0).

        Returns:
            list: Restaurants with rating >= min_rating.
        """
        return [
            restaurant
            for restaurant in self.database.get_restaurants()
            if restaurant["rating"] >= min_rating
        ]

    def search_by_filters(self, cuisine_type=None, location=None,
                          min_rating=None):
        """
        Search for restaurants using multiple filters.

        Args:
            cuisine_type (str, optional): The type of cuisine.
            location (str, optional): The location.
            min_rating (float, optional): The minimum rating.

        Returns:
            list: Restaurants matching all filters.
        """
        results = self.database.get_restaurants()
        if cuisine_type:
            results = [
                restaurant
                for restaurant in results
                if restaurant["cuisine"].lower() == cuisine_type.lower()
            ]
        if location:
            results = [
                restaurant
                for restaurant in results
                if restaurant["location"].lower() == location.lower()
            ]
        if min_rating:
            results = [
                restaurant
                for restaurant in results
                if restaurant["rating"] >= min_rating
            ]
        return results


class RestaurantDatabase:
    """
    A simulated in-memory database for restaurant information.

    Attributes:
        restaurants (list): A list of dictionaries, each representing a restaurant.
    """

    def __init__(self):
        """
        Initialize with a predefined set of restaurant data.
        """
        self.restaurants = [
            {
                "name": "Italian Bistro",
                "cuisine": "Italian",
                "location": "Downtown",
                "rating": 4.5,
                "price_range": "$$",
                "delivery": True,
            },
            {
                "name": "Sushi House",
                "cuisine": "Japanese",
                "location": "Midtown",
                "rating": 4.8,
                "price_range": "$$$",
                "delivery": False,
            },
            {
                "name": "Burger King",
                "cuisine": "Fast Food",
                "location": "Uptown",
                "rating": 4.0,
                "price_range": "$",
                "delivery": True,
            },
            {
                "name": "Taco Town",
                "cuisine": "Mexican",
                "location": "Downtown",
                "rating": 4.2,
                "price_range": "$",
                "delivery": True,
            },
            {
                "name": "Pizza Palace",
                "cuisine": "Italian",
                "location": "Uptown",
                "rating": 3.9,
                "price_range": "$$",
                "delivery": True,
            },
        ]

    def get_restaurants(self):
        """
        Retrieve the list of restaurants.

        Returns:
            list: List of restaurant dictionaries.
        """
        return self.restaurants


class RestaurantSearch:
    """
    Interfaces with RestaurantBrowsing to perform searches.

    Attributes:
        browsing (RestaurantBrowsing): The browsing instance.
    """

    def __init__(self, browsing):
        """
        Initialize with a RestaurantBrowsing instance.

        Args:
            browsing (RestaurantBrowsing): The browsing instance.
        """
        self.browsing = browsing

    def search_restaurants(self, cuisine=None, location=None, rating=None):
        """
        Search for restaurants using filters.

        Args:
            cuisine (str, optional): The type of cuisine.
            location (str, optional): The location.
            rating (float, optional): The minimum rating.

        Returns:
            list: Restaurants matching the criteria.
        """
        results = self.browsing.search_by_filters(
            cuisine_type=cuisine, location=location, min_rating=rating
        )
        return results


class TestRestaurantBrowsing(unittest.TestCase):
    """
    Unit tests for RestaurantBrowsing.
    """

    def setUp(self):
        """
        Set up by initializing RestaurantDatabase and RestaurantBrowsing.
        """
        self.database = RestaurantDatabase()
        self.browsing = RestaurantBrowsing(self.database)

    def test_search_by_cuisine(self):
        """
        Test searching by cuisine.
        """
        results = self.browsing.search_by_cuisine("Italian")
        self.assertEqual(len(results), 2)
        self.assertTrue(
            all(
                restaurant["cuisine"] == "Italian"
                for restaurant in results
            )
        )

    def test_search_by_location(self):
        """
        Test searching by location.
        """
        results = self.browsing.search_by_location("Downtown")
        self.assertEqual(len(results), 2)
        self.assertTrue(
            all(
                restaurant["location"] == "Downtown"
                for restaurant in results
            )
        )

    def test_search_by_rating(self):
        """
        Test searching by minimum rating.
        """
        results = self.browsing.search_by_rating(4.0)
        self.assertEqual(len(results), 4)
        self.assertTrue(
            all(
                restaurant["rating"] >= 4.0
                for restaurant in results
            )
        )

    def test_search_by_filters(self):
        """
        Test searching by multiple filters.
        """
        results = self.browsing.search_by_filters(
            cuisine_type="Italian", location="Downtown", min_rating=4.0
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Italian Bistro")


if __name__ == '__main__':
    unittest.main()
