from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.router_group import router_groups
from routes.router_members import router_members
from routes.router_solo_artists import router_solo_artists

app = FastAPI(title="KPOP-WIKI API")
app.include_router(router_groups)
app.include_router(router_members)
app.include_router(router_solo_artists)



origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)