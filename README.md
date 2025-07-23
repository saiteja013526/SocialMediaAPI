# 📸 Hey there! Welcome to FastAPI Framework

This is a cool little backend for a social media app, built with Python and FastAPI. It's got all the basic stuff you'd need to get a modern app up and running!

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.9.0-05998b?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql)

---

## What's Inside?

This project shows off some key backend skills and has everything you need to get going:

- **Log in safely!** We've got secure user sign-ups and logins using JWT tokens.
- **Share your thoughts!** You can create, read, update, and delete posts. All the good stuff.
- **No messy data here.** We use Pydantic to make sure all the data coming in and out is squeaky clean, and SQLAlchemy makes talking to the database a breeze.
- **It's all organized!** The project is set up in a clean way that keeps everything neat and tidy.

---

## What's Under the Hood?

Here's the tech we're using:

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT & Passlib
- **Server:** Uvicorn

---

## Get it Running in a Min

1. **First, clone the project.**

    ```bash
    git clone https://github.com/saiteja013526/SocialMediaAPI.git
    ```

2. **Install all the things it needs.**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your database info.** Create a `.env` file in the main folder, and must have a PostgreSQL as database..
4. **Fire it up!**

    ```bash
    uvicorn app.main:app --reload
    ```

---

## Play with the API

Ready to see it in action? Once the server's running, you can mess around with all the API endpoints right in your browser. It's super easy!

- **Check it out here:** `http://127.0.0.1:8000/docs`
