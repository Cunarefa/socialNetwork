import ast
import random
import requests

from conf import SIGNUP_URL, number_of_users, LOGIN_URL, POSTS_URL, max_posts_per_user, LIKES_URL, \
    max_likes_per_user

from faker import Faker

fake = Faker()


class DataGenerator:
    def __init__(self):
        self.headers = {}
        self.users = []
        self.posts = []

    def registration(self):
        for _ in range(number_of_users):
            username = fake.unique.email()
            password = username
            requests.post(SIGNUP_URL, data={'username': username, 'password': password})
            self.login(username, password)

    def login(self, username, password):
        login_data = {'username': username, 'password': password}
        response = requests.post(LOGIN_URL, data=login_data)
        self.set_headers(response)
        self.create_random_posts()

    def set_headers(self, response):
        data_dict = ast.literal_eval(response.text)
        token = data_dict['access']
        self.headers = {'Authorization': f'Bearer {token}'}
        self.users.append(self.headers)

    def create_random_posts(self):
        quantity_to_create = random.randint(1, max_posts_per_user)
        for _ in range(quantity_to_create):
            post_data = {'title': fake.text(max_nb_chars=20), 'content': fake.sentences(nb=5)}
            post = requests.post(POSTS_URL, data=post_data, headers=self.headers)
            self.posts.append(post)

    def set_likes(self):
        for headers in self.users:
            for post in random.choices(self.posts, k=max_likes_per_user):
                response_to_dict = ast.literal_eval(post.text)
                post_id = response_to_dict['id']
                data = {'post_id': post_id}
                requests.post(LIKES_URL, headers=headers, data=data)


if __name__ == '__main__':
    generator = DataGenerator()
    generator.registration()
    generator.set_likes()
