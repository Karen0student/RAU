to make this project work, follow these steps:
1) move into "DB_Project/postgres" directory, then execute command: docker-compose up -d (it will create "postgres" named container and initialize "opera" DB)
2) move into "DB_Project/FastAPI" directory, then execute command: uvicorn main:app --reload
3) in browser type this: http://127.0.0.1:8000
4) in "DB_Project" directory execute command: alembic upgrade head (it will create tables in database)

DONE

If you're done, turn this off with the following steps:
1) stop uvicorn
2) in "DB_Project/postgres" directory execute command: docker-compose down -v

DONE