from app import app
from mangum import Mangum

# Handler for Vercel
handler = Mangum(app) 