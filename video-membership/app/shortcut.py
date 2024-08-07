from app import config
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

settings = config.get_settings()

templates = Jinja2Templates(directory=str(settings.template_dir))


def render_template(request, template_name, context={}, status_code: int = 200, cookies: dict = {}):
    ctx = context.copy()
    ctx.update({
        "request": request
    })
    t = templates.get_template(template_name)
    html_str = t.render(ctx)
    # print(request.cookies)
    response = HTMLResponse(html_str, status_code=status_code)
    if len(cookies.keys()) > 0:
        for k, v in cookies.items():
            response.set_cookie(k, v, httponly=True)
    return response
    # return templates.TemplateResponse(template_name, ctx, status_code=status_code)
