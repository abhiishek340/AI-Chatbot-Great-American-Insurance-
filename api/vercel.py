from mangum import Mangum
from app import app

# Handler for Vercel
handler = Mangum(app) 