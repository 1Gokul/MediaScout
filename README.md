# MediaScout

A movie/tv-show web app.

![Heroku Badge](https://pyheroku-badge.herokuapp.com/?app=mediascout)
![Codacy Badge](https://app.codacy.com/project/badge/Grade/4d83f97a49834c6391d6464ffed47109)
![License](https://img.shields.io/github/license/1gokul/mediascout)

Made with Flask, HTML and CSS.

If you want to work on the code yourself:

## Installation

- Clone the repo
- Navigate to the downloaded folder
- Open Terminal/CMD in the folder
- Run `pip install -r requirements.txt`
- Once it is finished, run `python main.py`
- You're good to go!

## Important

This uses a Postgres DB to get information for the "home", "movie" and "tv" pages instead of sending requests every time to the [TMDB API](https://developers.themoviedb.org).

To keep the DB up to date with the required info,

1. [Set up Postgres locally if you haven't](https://www.prisma.io/dataguide/postgresql/setting-up-a-local-postgresql-database)
2. Create a new database and set the address to it in `data_storage.py` like so-

```python
os.environ["DATABASE_URL"] = "postgresql://postgres:<your_password>@localhost:5432/<your_db_name>"
```

3. Set an `UPDATE_VERIFICATION_CODE` environment variable in `data_storage.py` to a particular value.

```python
os.environ["UPDATE_VERIFICATION_CODE"] = "<my_secret_code>"
```

4. Run the app
5. Send a POST request to `localhost:5000/update-db/` with the request body:
    ```
    {
      "auth_code": "<my_secret_code>"
    }
    ```
6. The DB should be updated!
