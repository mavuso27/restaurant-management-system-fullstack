import secrets
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from httpx import AsyncClient
from app.database import get_db
from app.models.models import Customer
from app.security.security import create_access_token
from app.config import settings
from app.security.security import verify_token, oauth2_scheme

router = APIRouter(prefix="/auth", tags=["Authentication"])

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"


@router.get("/login")
def github_login(request: Request, response: Response):
    state = secrets.token_urlsafe(32)
    
    auth_url = f"{GITHUB_AUTH_URL}?client_id={settings.GITHUB_CLIENT_ID}&scope=user:email&state={state}"
    
    response = RedirectResponse(url=auth_url)
    response.set_cookie(
        key="oauth_state", 
        value=state, 
        httponly=True, 
        secure=request.url.scheme == "https",  
        samesite="lax", 
        max_age=300            
    )
    return response


@router.get("/callback")
async def github_callback(
    request: Request, 
    response: Response, 
    code: str, 
    state: str, 
    db: Session = Depends(get_db)
):
    
    cookie_state = request.cookies.get("oauth_state")
    if not cookie_state or cookie_state != state:
        raise HTTPException(status_code=400, detail="State verification failed. CSRF detected.")
    

    response.delete_cookie("oauth_state")

    async with AsyncClient() as client:
    
        token_response = await client.post(
            GITHUB_TOKEN_URL,
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
            },
            headers={"Accept": "application/json"},
        )
        token_data = token_response.json()
        github_access_token = token_data.get("access_token")

        if not github_access_token:
            raise HTTPException(status_code=400, detail="GitHub authentication failed")

    
        user_response = await client.get(
            GITHUB_USER_URL,
            headers={"Authorization": f"Bearer {github_access_token}"},
        )
        github_user = user_response.json()

    github_id = str(github_user.get("id"))
    github_name = github_user.get("name") or github_user.get("login")
    

    github_email = github_user.get("email") or f"{github_user.get('login')}@users.noreply.github.com"

    
    customer = db.query(Customer).filter(Customer.github_id == github_id).first()

    if not customer:
    
        customer = Customer(
            name=github_name,
            phone="N/A",
            address="N/A",
            email=github_email,
            country="Unknown",
            github_id=github_id
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)

    
    access_token = create_access_token(data={"sub": github_id})

    return {"access_token": access_token, "token_type": "bearer", "user": github_name}

#-------I will start debugging from here.
@router.get("/me", tags=["Authentication"])
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Extracts and verifies the JWT token via Bearer authentication, 
    linking it to the authenticated customer in Supabase.
    """
    github_id = verify_token(token)
    if not github_id:
        raise HTTPException(
            status_code=401, 
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    customer = db.query(Customer).filter(Customer.github_id == github_id).first()
    if not customer:
        raise HTTPException(status_code=401, detail="User not found")
        
    return customer