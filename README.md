[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org)

# Cosmic Data Stories
Cosmic Data Stories are online interactive resources for teaching the public data science skills. They are built on research-grade visualization tools like [glue](https://glueviz.org) and [WorldWide Telescope](https://worldwidetelescope.org/home).

This is the base repo for all python-based Data Stories, such as [HubbleDS](https://github.com/cosmicds/hubbleds).

### Requirements
- Python-based Cosmic Data Stories now run on [solara](https://solara.dev).

### Installation
- Optional but recommended, set up a new python environment.
- Install `pip` if you don't already have it.
- If you haven't already installed it,
```
    $ pip install solara
```
- Pull down the cosmicds repo.
- Inside the cosmicds folder in your terminal,
```
    $ pip install -e .
```

# Legacy Code
As of 4/30/2024, the voila-based code has been moved to the [legacy](https://github.com/cosmicds/cosmicds/tree/legacy) branch.

To run the legacy code:

- Pull down both the legacy branch and set up a new python environment.
- In the cosmicds directory with the legacy code:
```
    $ pip install -e .
```
- You may need to pip install any missing dependencies.
- If you have trouble installing voila, you may need to downgrade your version of `node.js` to a Long Term Support (LTS) version (14.x or 16.x).


## Note
This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
