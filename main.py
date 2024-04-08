from fastapi import FastAPI
from db import Base, engine
from routers import auth, users, costumers, branches, orders, transport, xizmatlar, washing, qadoqlash, tokcha, \
    operator, sozlamalar, millat, davomat, buxgalteriya
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

app.include_router(
    branches.router_branch,
    prefix='/branches',
    tags=['Branches section'],
)

app.include_router(
    orders.router_order,
    prefix='/orders',
    tags=['Orders section'],
)

app.include_router(
    transport.router_transport,
    prefix='/transport',
    tags=['Transport section'],
)

app.include_router(
    xizmatlar.router_xizmat,
    prefix='/xizmatlar',
    tags=['Xizmatlar section'],
)

app.include_router(
    washing.router_washing,
    prefix='/washing',
    tags=['Washing section'],
)

app.include_router(
    qadoqlash.router_qadoqlash,
    prefix='/qadoqlash',
    tags=['Qadoqlash section'],
)

app.include_router(
    tokcha.router_tokcha,
    prefix='/tokcha',
    tags=['Tokcha section'],
)

app.include_router(
    operator.router_operator,
    prefix='/operator',
    tags=['Operator section'],
)

app.include_router(
    sozlamalar.router_sozlamalar,
    prefix='/sozlamalar',
    tags=['Sozlamalar section'],
)

app.include_router(
    millat.router_millat,
    prefix='/millat',
    tags=['Millat section'],
)

app.include_router(
    davomat.router_davomat,
    prefix='/davomat',
    tags=['Davomat section'],
)

app.include_router(
    buxgalteriya.router_buxgalteriya,
    prefix='/buxgalteriya',
    tags=['Buxgalteriya section'],
)