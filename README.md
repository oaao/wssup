# wssup

head over to [django/channels](https://github.com/django/channels) and use my promo code :rotating_light: :tickets: :hotsprings: `3HTTP5ME` :hotsprings: :tickets: :rotating_light:

## setup

Requirements:

* python >= `3.5`
* django >= `1.11`
* docker `used to install and run Redis`

Run migrations required by Django's session framework:

```./manage.py migrate```

Configure `ALLOWED_HOSTS` in `wssup.wssup.settings` (e.g. `*`, or `localhost` + `127.0.0.1`, or a specific domain name and/or external IP) as preferred.
