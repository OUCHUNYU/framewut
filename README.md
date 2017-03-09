# framewut
[![wut](misc/wut.png)](misc/wut.png)

**Python** web frameworks and their nearly infinite configurations are frankly kind of a morass. Like, we've all heard and take for truth that you should ditch the synchronous model for something async, based on libev -- you know like gevent, right?

But then you start to play around with things, and notice that you can run things various ways. Python imposes no restrictions (or guidance!) on this. E.g. you can run a Flask app as a gevent WSGI server. But you don't monkey patch, and so your `time.sleep` test performs no better than just running a plain WSGI server synchronously. Or perhaps you compare a CPU-intensive task, sync against async, and there is little difference (or maybe synchronous does a little better!).

Maybe you decide that for a really good test you should run under Gunicorn with 10 workers as you might in production, and then you realize there are all these _worker classes_ there, like _Meinheld_ (which claims it's a better async server, and is based on something called picoev, blah). Then you also notice that you can run a server written for _gevent_ with a _Meinheld_ worker and you start to wonder, "can these just run together? does that even make sense?"

### Anyway ...
The above has more or less been my experience, and I finally got tired of wondering and getting confusing information from The Google and decided to just sort of _sort it out myself_.

Hence, this repository. Which is basically a set of simple servers oriented around a few test scenarios, which are then run in various ways by combining frameworks and engines (or whatever each is called; frankly I don't really care at this point):

* A basic *hello world* test, ran synchronously and asynchronously, as a vanilla WSGI server, Werkzeug, Flask.
* A *sleep* test, where we modify the *hello world* test to add a tiny `time.sleep` on the endpoint.
* A *request* test, a bit more realistic test, which modifies the *hello world* test to make a request to a remote page, and return the results. We not only test with async/sync engines, but with sync and async *request* libraries.
* A CPU-intenstive test comparing async vs. sync.

## Getting started
If you want to try this out, clone this repository and do

```
pip install -r requirements.txt
```

You'll need a Bash environment with some standard *nix utilities, along with `curl` and the `wrk` benchmarking tool.

If you have those, then you can run all the tests by doing

```
./notes.sh
```

To understand how the tests are run, I recommend looking at that script. (Everything is run under Gunicorn with 10 workers, btw.)

## Interesting things

*Wed Mar  8 09:03:03 MST 2017*

This was never intended to be a comprehensive benchmarking project. It is more a way to understand some characteristics of different configurations.

All the knowledge of `notes.sh` is encapsulated in [notes.txt](notes.txt), which is just a capture of its output. You should run it yourself to be sure what's here makes sense, and is replicable on your system.

That being said there are a couple things that became clear to me after getting this stuff sorted out.

### 1. Hello world
Running under a *gevent* server is noticeably better.

```
# gevent
Requests/sec:  10902.24

# synchronous wsgi
Requests/sec:    823.50
```

More interestingly, running the plain WSGI code unmodified with a *Meinheld* worker is actually much *better* than gevent:

```
# gevent
Requests/sec:  10902.24

# wsgi with meinheld workder
Requests/sec:  50032.02
```

However, it should be noted that *Meinheld* is also an event loop based server.

### 2. The real world
In our *sleep* tests, where we use `time.sleep` on an endpoint, gevent definitely makes a difference over the other configurations:

```
# gevent 
Requests/sec:   1940.47

# synchronous wsgi
Requests/sec:     97.92
```

However, when we do something that's more like what we'd actually do in real life, the results, are, well more interesting. In the following tests, the endpoint we request makes a request of its own against a real, remote endpoint.

First, async beats sync here:

```
# gevent
Requests/sec:    207.24

# synchronous wsgi
Requests/sec:     86.37
```

However, there's a caveat. The gevent test in the above is using an *async requests* library, whereas the synchronous test is just using regular old [requests](http://docs.python-requests.org/).

So what happens when we use a synchronous server, but use an asynchronous requests library? The same one we use for the gevent one in the test above, in fact.

```
# synchronous wsgi
Requests/sec:    249.46

# plain wsgi with meinheld worker
Requests/sec:    256.39
```
No monkey patching or anything, and the synchronous server beats gevent (!?). Running with *Meinheld* is even more of an improvement, if a slight one (but I honestly don't know what hacks it might be running here, either).