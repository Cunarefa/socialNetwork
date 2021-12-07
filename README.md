# socialNetwork

DRF Social Network project and Bot

## Setting up DRF project

First build Dockerfile:

```
cd backend/
make build
```

Then run migrations:

```
make migrate
```

Optionally create superuser:

```
make user
```

Run project 

```
make run
```

## Running bot

First you need to install requirements.txt in the root directory:

```
pip install -r requirements.txt
```

Launching bot

```
cd bot/
python bot.py
```

You can change ```number_of_users```, ```max_posts_per_user``` and ```max_likes_per_user``` in ```conf.py``` file

