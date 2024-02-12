from fastapi import FastAPI
from db import Base, engine
from routers import auth, users, costumers
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="FastAPI app by Akmaljon",
    responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
               401: {'desription': 'Unauthorized'}}
)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return {"message": "Welcome"}


app.include_router(
    auth.login_router,
    prefix='/auth',
    tags=['User auth section'],

)


app.include_router(
    users.router_user,
    prefix='/user',
    tags=['User section'],
)

app.include_router(
    costumers.router_costumer,
    prefix='/costumers',
    tags=['Costumers section'],
)
