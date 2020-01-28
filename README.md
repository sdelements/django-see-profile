# django-see-profile
A simple middleware to capture useful profiling information in Django.

## Requirements

* Django 1.10+
* django-security 0.9.0+

## Description

This is intended to be a simple method for capturing useful profiling
information from Django for specific requests without interrupting the normal
program flow or requiring any database tables etc. It makes use of the builtin
python logging facilities to dump individual requests as a single log message
and leaving your log configuration to figure out what to do with it.

## Usage

Install as usual for a middleware:

```
MIDDLEWARES = (
    ...
    see_profile.ProfilingMiddleware
    ...
)
```

If you're interested in profiling what's being done in the other middlewares
you can put it higher in the middleware listing, but if you're just interested
in view-specific profiling it is recommended to have it fairly close to the
end of the middlewares list.

To activate the middleware, set `ENABLE_PROFILING` to True, otherwise set it
to false to deactivate.

The middleware by default does not log every request as it is a performance hit
and would be fairly noisy when trying to profile in a busy environment, so for
requests that you desire profiled you are expected to set an `X-Profile` HTTP
header for the request. The value is immaterial at this time.

All logged requests are sent to the `profiling` logger at the `DEBUG` level,
so you will need to configure a relevant logger & handler for that.
