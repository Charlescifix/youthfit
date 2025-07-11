from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import models
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

# Landing page (home)
@router.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

# Show the booking form
@router.get("/book", response_class=HTMLResponse)
async def show_booking_form(request: Request):
    return templates.TemplateResponse("booking_form.html", {"request": request})

# Handle booking form submission
@router.post("/book", response_class=HTMLResponse)
async def submit_booking(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    service: str = Form(...),
    consent_text: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # Create user
    new_user = models.User(
        full_name=full_name,
        email=email,
        phone=phone
    )
    db.add(new_user)
    await db.flush()

    # Create booking
    booking = models.Booking(
        service=service,
        user_id=new_user.id
    )
    db.add(booking)

    # Create consent
    consent = models.Consent(
        content=consent_text.strip(),
        user_id=new_user.id
    )
    db.add(consent)

    # Commit all
    await db.commit()

    return templates.TemplateResponse("booking_confirmation.html", {
        "request": request,
        "full_name": full_name,
        "service": service
    })






@router.get("/admin/bookings", response_class=HTMLResponse)
async def list_bookings(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        models.Booking.__table__.join(models.User).select()
    )
    rows = result.fetchall()

    return templates.TemplateResponse("admin_bookings.html", {
        "request": request,
        "bookings": rows
    })


@router.get("/consent", response_class=HTMLResponse)
async def consent_form(request: Request):
    return templates.TemplateResponse("consent_form.html", {"request": request})

@router.post("/consent", response_class=HTMLResponse)
async def submit_consent(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    consent_text: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # Find or create user
    result = await db.execute(
        models.User.__table__.select().where(models.User.email == email)
    )
    user = result.fetchone()
    if not user:
        new_user = models.User(full_name=full_name, email=email)
        db.add(new_user)
        await db.flush()
        user_id = new_user.id
    else:
        user_id = user.id

    # Save consent
    consent = models.Consent(
        content=consent_text,
        user_id=user_id
    )
    db.add(consent)
    await db.commit()

    return templates.TemplateResponse("consent_confirmation.html", {
        "request": request,
        "full_name": full_name
    })
