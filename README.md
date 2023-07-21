# Selectel balance Exporter

This repo contains prometheus Selectel balance exporter which can be used to get metrics
related to specified account.

## Installation

There are several ways to get this exporter. Let's look at all of them.

### Standalone

Selectel balance exporter is written on Python, so one first needs to have to install all
the requirements to run.

```
pip install -r requirements.txt
cd whois-exporter
uvicorn main:app
```

## FAQ

Q: I'm getting an error while installing `requirements.txt` on macos:

```
ERROR: Failed building wheel for maturin
```

A: You have to update your pip: `pip install -U pip` and try again
