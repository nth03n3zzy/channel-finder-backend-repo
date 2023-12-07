# UPDATING SECURITY KEYS

// (portfolio) $ python manage.py shell
Once there, you’ll be able to generate a new random secret key using Django’s built-in management utilities:

> > > from django.core.management.utils import get_random_secret_key
> > > print(get_random_secret_key())
> > > 6aj9il2xu2vqwvnitsg@!+4-8t3%zwr@$agm7x%o%yb2t9ivt%
> > > Grab that key and use it to set the SECRET_KEY variable in your .env file:

$ echo 'SECRET_KEY=6aj9il2xu2vqwvnitsg@!+4-8t3%zwr@$agm7x%o%yb2t9ivt%' > .env
The heroku local command picks up environment variables defined in your .env file automatically, so it should be working as expected now. Remember to comment out the SECRET_KEY variable again if you uncommented it!

The final step is specifying a Django secret key for the remote Heroku app:

$ heroku config:set SECRET_KEY='6aj9il2xu2vqwvnitsg@!+4-8t3%zwr@$agm7x%o%yb2t9ivt%'
Setting SECRET_KEY and restarting ⬢ polar-island-08305... done, v3
SECRET_KEY: 6aj9il2xu2vqwvnitsg@!+4-8t3%zwr@$agm7x%o%yb2t9ivt%
This will permanently set a new environment variable on the remote Heroku infrastructure, which will immediately become available to your Heroku app. You can reveal those environment variables in the Heroku dashboard or with the Heroku CLI:

$ heroku config
=== polar-island-08305 Config Vars
SECRET_KEY: 6aj9il2xu2vqwvnitsg@!+4-8t3%zwr@$agm7x%o%yb2t9ivt%

$ heroku config:get SECRET_KEY
6aj9il2xu2vqwvnitsg@!+4-8t3%zwr@$agm7x%o%yb2t9ivt% \*/
