import random

import requests
from django.core.exceptions import ObjectDoesNotExist

from conf import number_of_users, LOGIN_URL, SIGNUP_URL, max_posts_per_user, POSTS_URL, max_likes_per_user, LIKES_URL
from faker import Faker

fake = Faker()


class Bot:
    def __init__(self):
        self.users = []
        self.posts = []

    def register(self):
        for _ in range(number_of_users):
            username = fake.unique.email()
            password = username
            api = API(username, password)
            user = api.send_request(SIGNUP_URL, data={'username': username, 'password': password})
            if user:
                user['password'] = password
                self.users.append(user)

    def create_posts(self):
        for user in self.users:
            quantity_to_create = random.randint(1, max_posts_per_user)
            api = API(user['username'], user['password'])
            headers = api.get_headers()
            for _ in range(quantity_to_create):
                post_data = {'title': fake.text(max_nb_chars=20), 'content': fake.sentences(nb=5)}
                post = api.send_request(POSTS_URL, data=post_data, headers=headers)
                if post:
                    self.posts.append(post)

    def set_likes(self):
        for user in self.users:
            api = API(user['username'], user['password'])
            headers = api.get_headers()
            for post in random.choices(self.posts, k=max_likes_per_user):
                data = {'post_id': post['id']}
                api.send_request(LIKES_URL, data=data, headers=headers)


class API:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def send_request(self, url, data, headers=None):
        try:
            response = requests.post(url=url, data=data, headers=headers)
            return response.json()

        except ValueError as err:
            print(f"Wrong data input!. Exception: {err}")
        except ObjectDoesNotExist as err:
            print(f'User with that credentials does not exists. Exception: {err}')
        except Exception as err:
            print(f'Error while creating new user with username {self.username}. Exception: {err}')

        return {}

    def get_headers(self):
        data = {'username': self.username, 'password': self.password}
        response = requests.post(LOGIN_URL, data).json()
        token = response['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        return headers


if __name__ == '__main__':
    bot = Bot()
    bot.register()
    bot.create_posts()
    bot.set_likes()
