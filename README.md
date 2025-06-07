"# fitness_booking" 
# 🧘‍♀️ Fitness Booking API (Django + DRF + Celery)

## 🚀 Setup Instructions

1. **Clone the repo & install dependencies:**

```bash
git clone https://github.com/yourusername/fitness-booking.git
cd fitness-booking
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate (Windows)
pip install -r requirements.txt

2. **Apply migrations and seed data:**

```bash
python manage.py migrate
python manage.py seed_data

3. **Start the server and Celery:**

```bash
# In one terminal
redis-server  # Make sure Redis is running

# In another
python manage.py runserver

# In another
celery -A fitness_booking worker --loglevel=info

# In another (for periodic reminder tasks)
celery -A fitness_booking beat --loglevel=info

##  API Endpoints
1. **List All Classes:**
Gets all the classes
```http
GET /classes/

2. **Book a Class:**
```http
POST /book/
**JSON Body:**
{
  "fitness_class": 20,
  "client_name": "Aravind",
  "client_email": "dummy@example.com",
  "user_timezone": "Asia/Kolkata"
}
**Note: In fitness_class Enter fitness class id from the list of the fitness classes insted of 20 and also correct the mail**
3. **Get Bookings by Email:**
```http
GET /bookings/?email=dummy@example.com&timezone=Asia/Kolkata

## Timezone Support
All bookings and class times are shown based on the user_timezone passed in the API request (e.g., Asia/Kolkata, America/New_York).
