

# Stripe Card payment with Django.

Stripe Card payment System is a web application that allows to create payments/refund, perform CRUD on Card along with that set/get default card & payment envent handling.


This project contains the Django back-end with Django REST framework and back-end code required to make it all work.





## Django setup instructions.



1. Create a python virtual environment using below command.

   `python3 -m venv virtual-env`

2. Activate the environment.

   `source virtual-env/bin/activate`

3. Install dependencies.

   `pip install -r requirements.txt`

4. You can change the database settings if you wish in `settings.py`


5. You can set the Stripe Configuration settings in `settings.py` by providing STRIPE_PUBLIC_KEY,STRIPE_SECRET_KEY,STRIPE_WEBHOOK_SECRET


6. If you are using a fresh database in local execute this commands.

   `python manage.py makemigrations `

   `python manage.py migrate`

7. Run this command and your django app should be running on port `8000`

   `python manage.py runserver`
