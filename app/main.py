from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routers import meals, customers, orders, auth

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Restaurant Information System API",
    description="""
##  Restaurant Information System - Secure REST API

A production-grade API demonstrating real-world cybersecurity practices.

##  Security Features Implemented
* **OAuth 2.0** : GitHub authentication with CSRF state verification
* **JWT Tokens** : Short-lived, timezone-aware secure session management
* **Rate Limiting** : Prevents brute force and DoS attacks on all endpoints
* **Parameterized Queries** : SQL injection prevention via SQLAlchemy ORM
* **Input Validation** : All inputs strictly validated via Pydantic schemas
* **RBAC** : Role Based Access Control (admin vs customer)
* **BOLA Prevention** : Users can only access their own data
* **Security Headers** : XSS, clickjacking and MIME sniffing protection
* **CORS Protection** :Controlled cross-origin access
* **Mass Assignment Prevention** : Explicit field mapping on all write operations

## Author
**Ashley Ntabiso Mondela** - Information Technologies Student, Cyprus International University
ISC2 Certified in Cybersecurity (CC)

## Note
Hosted on Render free tier - please allow 30-60 seconds for initial server spin-up.
    """,
    version="1.0.0",
    contact={
        "name": "Ashley Ntabiso Mondela",
        "url": "https://github.com/mavuso27",
        "email": "ashleymondelantabiso@gmail.com"
    }
)


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


ALLOWED_ORIGINS = [
    "http://localhost:3000",      
    "http://127.0.0.1:3000",
    "https://your-frontend-domain.vercel.app" # Replace with your live frontend domain when deployed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' cdn.jsdelivr.net; "
        "img-src 'self' data: fastapi.tiangolo.com;"
    )
    return response


app.include_router(auth.router)
app.include_router(meals.router)
app.include_router(customers.router)
app.include_router(orders.router)



@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Restaurant Information System API",
        "version": "1.0.0",
        "docs": "/docs",
        "author": "Ashley Ntabiso Mondela",
        "github": "https://github.com/mavuso27",
        "linkedin": "https://www.linkedin.com/in/ashley-mondela-b2a5a4218/",
        "note": "Hosted on Render free tier — please allow 30-60 seconds for initial server spin-up."
    }


@app.get("/health", tags=["Root"])
def health_check():
    return {"status": "healthy"}