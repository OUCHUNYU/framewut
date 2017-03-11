# framewut
[![wut](misc/wut.png)](misc/wut.png)

**Python** web frameworks and their nearly infinite configurations are frankly kind of a morass. Like, we've all heard and take for truth that you should ditch the synchronous model for something async, based on libev -- you know like gevent, right?

But then you start to play around with things, and notice that you can run things various ways. Python imposes no restrictions (or guidance!) on this. E.g. you can run a Flask app as a gevent WSGI server. But you don't monkey patch, and so your `time.sleep` test performs no better than just running a plain WSGI server synchronously. Or perhaps you compare a CPU-intensive task, sync against async, and there is little difference (or maybe synchronous does a little better!).

Maybe you decide that for a really good test you should run under Gunicorn with 10 workers as you might in production, and you realize there are all these *worker classes* there, like *Meinheld* (which claims it's a better async server, and is based on something called picoev, blah). Then you also notice that you can run a server written for *gevent* with a *Meinheld* worker and you start to wonder, "can these just run together? does that even make sense?"

### Anyway ...
The above has more or less been my experience, and I finally got tired of wondering and getting confusing information from The Google and decided to just sort of *sort it out myself*.

Hence, this repository. Which is basically a set of simple servers oriented around a few test scenarios, which are then run in various ways by combining frameworks and engines (or whatever each is called; frankly I don't really care at this point):

* A basic *hello world* test, ran synchronously and asynchronously, as a vanilla WSGI server, Werkzeug, Flask.
* A *sleep* test, where we modify the *hello world* test to add a tiny `time.sleep` on the endpoint.
* A *request* test, a bit more realistic one which modifies the *hello world* test to make a request to a remote page, and return the results. We not only test with async/sync engines, but with sync and async *request* libraries.
* A CPU-intenstive test comparing async vs. sync.
* *TODO* Database test

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

*Fri Mar 10 08:32:54 CST 2017*

This was never intended to be a comprehensive benchmarking project. It is more a way to understand some characteristics of different configurations.

All the knowledge of `notes.sh` is encapsulated in [notes.txt](notes.txt), which is just a capture of its output. You should run it yourself to be sure what's here makes sense, and is replicable on your system.

That being said there are a couple things that became clear to me after getting this stuff sorted out.

### 1. Hello world
Running under a *gevent* server is considerably better.

```
# gevent
Requests/sec:  12157.01

# synchronous wsgi
Requests/sec:    823.07
```

More interestingly, running the plain WSGI code unmodified with a *Meinheld* worker is actually noticeably *better* than gevent:

```
# gevent
Requests/sec:  12157.01

# wsgi with meinheld workder
Requests/sec:  61283.44
```

However, it should be noted that *Meinheld* is also an event loop based server.

### 2. The real world
In our *sleep* tests, where we use `time.sleep` on an endpoint, gevent definitely makes a difference over the other configurations:

```
# gevent 
Requests/sec:   1947.02

# synchronous wsgi
Requests/sec:     98.46
```

However, when we do something that's more like what we'd actually do in real life, the results, are, well more interesting. In the following tests, the endpoint we hit makes a request of its own against a real, remote endpoint.

(There's a bit of a caveat I should mention regarding the below requests tests. In observing multiple runs, I've noticed that the results are a bit unpredictable. While I chose a remote endpoint -- a 404 on Google -- that I feel should be relatively stable/responsive, other factors like network come into play here.)

Basically, it appears that sync and async fare about the same.

```
# gevent
Requests/sec:     86.83

# synchronous wsgi
Requests/sec:    105.78
```

When you change to an async *requests* library (we're using the FuturesSession library), things look better:

```
# gevent
Requests/sec:    226.57

# synchronous wsgi
Requests/sec:    197.75

# wsgi with meinheld worker
Requests/sec:    211.04
```

But notice that things look better all around. I.e. the framework in this case doesn't seem to make much difference. Switching to an async requests library *does* seem to matter though.

### 3. CPU
If you add in a CPU intenstive task, things will get blocked, especially in an event loop. Another case where sync and async have essentially attained parity.

```
# gevent
Requests/sec:    208.45

# synchronous wsgi
Requests/sec:    229.23
```
