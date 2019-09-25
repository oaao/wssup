# wssup

head over to [django/channels](https://github.com/django/channels) and use my promo code :rotating_light: :tickets: :hotsprings: `3HTTP5ME` :hotsprings: :tickets: :rotating_light:

## setup

Requirements:

* python >= `3.5`
* django >= `1.11`
* docker `used to install and run Redis`


Run migrations (needed for Django's session framework):

```bash
# wssup/
$ ./manage.py migrate
```

Configure allowed hosts as needed:

```python
# wssup/wssup/settings.py
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'www.domain.com', '.domain.com']
```

### optional - testing via selenium

Install [Google Chrome](https://www.google.com/chrome/) web browser.

Obtain [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/getting-started) and place it in your `$PATH`. *This is used by Selenium to control Chrome; make sure you choose the appropriate release for you Chrome version.*

Install Selenium.

```bash
$ pip3 install selenium
```


## usage

Start a Redis server on a local `{port}` via Docker.

```bash
$ docker run -p {port}:6379 -d redis:2.8
```

Run the django ASGI server.

```bash
# wssup/
$ ./manage.py runserver # 0:{port} for external access
```

Clients access `{host}/chat/` and input a chatroom name to join. All messages from all clients should appear in that room.

## troubleshooting

+ [test that a channel layer can communicate with Redis](#channel_talks_redis)


**test that a channel layer can communicate with Redis**<a name="channel_talks_redis"></a>

```bash
# wssup/
$ ./manage.py shell
```
```python
>>> import channels.layers
>>> cl = channels.layers.get_channel_layer()
>>>
>>> from asgiref.sync import async_to_sync as a2s
>>> a2s(cl.send)('test', {'type': 'hi'})
>>>
>>> a2s(cl.receive)('test')
{'type': 'hi'}
```
