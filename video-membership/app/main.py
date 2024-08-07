from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from . import config, db, utils
from cassandra.cqlengine.management import sync_table
from .users.models import User
from .users.schema import UserSignUpSchema, UserLoginSchema
from .shortcut import render_template

session = None

app = FastAPI()
settings = config.get_settings()


@app.on_event("startup")
def startup_event():
    print("Sync Table")
    global session
    session = db.get_session()
    sync_table(User)


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    context = {
        "request": request,
        "abc": 1234
    }

    return render_template(request, "home.html", context)


@app.get("/login", response_class=HTMLResponse)
def login_get_view(request: Request):
    session_id = request.cookies.get("session_id")
    return render_template(request, "auth/login.html", {"logged_in": session_id is not None})


@app.post("/login", response_class=HTMLResponse)
def login_post_view(request: Request,
                    # key should be same as name field in form in login.html
                    email: str = Form(...),
                    password: str = Form(...)):  # (...) means required field
    data, errors = utils.valid_schema_data_or_error(
        {"email": email, "password": password}, UserLoginSchema)
    print(data)
    context = {
        "errors": errors,
        "data": data,
    }
    # print(context)
    if len(errors) > 0:
        return render_template(request, "auth/login.html", context, status_code=400)
    return render_template(request, "auth/login.html", {"logged_in": True}, cookies=data)


@app.get("/signup", response_class=HTMLResponse)
def signup_get_view(request: Request):
    return render_template(request, "auth/signup.html", {})


@app.post("/signup", response_class=HTMLResponse)
def signup_post_view(request: Request,
                     # key should be same as name field in form in login.html
                     email: str = Form(...),
                     password: str = Form(...),
                     password_confirm: str = Form(...)):  # (...) means required field
    data, errors = utils.valid_schema_data_or_error(
        {"email": email, "password": password, "password_confirm": password_confirm}, UserSignUpSchema)
    context = {
        "errors": errors,
        "data": data,
    }
    if len(errors) > 0:
        return render_template(request, "auth/signup.html", context, status_code=400)
    User.create_user(email=email, password=password)
    return render_template(request, "auth/signup.html", context)


@ app.get("/users")
def user_list_view():
    users = User.objects().all()
    # User.objects.create(email="lp@gmail.com", password="abc")
    return list(users)
