# fail2ban-map 

[![build](https://github.com/strangelookingnerd/fail2ban-map/actions/workflows/build.yml/badge.svg)](https://github.com/strangelookingnerd/fail2ban-map/actions/workflows/build.yml)

```
 _______  _______  ___  ___      _______  _______  _______  __    _        __   __  _______  _______ 
|       ||   _   ||   ||   |    |       ||  _    ||   _   ||  |  | |      |  |_|  ||   _   ||       |
|    ___||  |_|  ||   ||   |    |____   || |_|   ||  |_|  ||   |_| | ____ |       ||  |_|  ||    _  |
|   |___ |       ||   ||   |     ____|  ||       ||       ||       ||____||       ||       ||   |_| |
|    ___||       ||   ||   |___ | ______||  _   | |       ||  _    |      |       ||       ||    ___|
|   |    |   _   ||   ||       || |_____ | |_|   ||   _   || | |   |      | ||_|| ||   _   ||   |    
|___|    |__| |__||___||_______||_______||_______||__| |__||_|  |__|      |_|   |_||__| |__||___|    
```

## What is this?

![public/favicon.ico](public/favicon.ico)

fail2ban-map is a map generator for [fail2ban](http://www.fail2ban.org).
It displays banned IP on a world map. Adding IP is done through a fail2ban *action* included in this repository.

Check out the [demo](https://strangelookingnerd.github.io/fail2ban-map/).

fail2ban-map is a re-write of [fail2map](https://github.com/tachtler/fail2map) by Manuel Vonthron and Klaus Tachtler.

## Installation

* Clone fail2ban-map to the desired location

    ```bash
    git clone https://github.com/strangelookingnerd/fail2ban-map /home/pi
    ```
* Install dependencies

    ```bash
    cd /home/pi/fail2ban-map
    npm install
    pip install -r requirements.txt
    ```

* Edit `script/fail2ban-map-action.conf` with the correct path to fail2ban_map.py

    ```bash
    nano /home/pi/fail2ban-map/script/fail2ban-map-action.conf
    
    ```

    ```bash
    fail2ban-map = cd /home/pi/fail2ban-map/script && python fail2ban_map.py
    ```

*  Create a symlink to `script/fail2ban-map-action.conf` in the fail2ban actions folder 

    ```bash
    ln -s /home/pi/fail2ban-map/script/fail2ban-map-action.conf /etc/fail2ban/action.d/fail2ban-map-action.conf
    ```
    
* Add the action to your `jail.conf` or `jail.local`

    ```bash
    # The simplest action to take: ban only
    action_ = %(banaction)s[name=%(__name__)s, port="%(port)s", protocol="%(protocol)s", chain="%(chain)s"]
              fail2ban-map-action
    ```

* (Optional) Change the tile provider in `public/fail2ban-map.js`

    ```javascript
    // list of tile providers can be seen here: https://leaflet-extras.github.io/leaflet-providers/preview/
    L.tileLayer.provider("CartoDB.DarkMatterNoLabels").addTo(map);
    ```
