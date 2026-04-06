from fastapi import APIRouter, Request, Form
from db.database import async_session
from fastapi.responses import HTMLResponse, RedirectResponse
from repository.user_repository import UserRepository
from utils.util import verify_password
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")


# Создаем роутер для группировки endpoints связанных с операциями
router = APIRouter(
    # Присваиваем тэг и префикс для нашей документации API
    prefix="/login",
    tags=["Авторизация"]
)

async def get_db():
    async with async_session() as session:
        yield session

@router.get("", response_class=HTMLResponse)
async def get_login_form(request: Request):
    """GET /login — открывает HTML-форму"""
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )

# Создаем ручку для генерации юзера и password_hash
@router.post("")
async def login(
        request : Request,
        username : str = Form(...),
        password : str = Form(...),
):
    user = await UserRepository.find_by_user(username)

    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "login.html",
            {
                "request" : request,
                "error" : "Неверный логин или пароль"
            }
        )
    return RedirectResponse(url="/docs", status_code=303)