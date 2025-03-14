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

fail2ban-map is a re-write of on [fail2map](https://github.com/tachtler/fail2map) by Manuel Vonthron and Klaus Tachtler.

## Installation

* Place fail2ban-map in the desired path of your web server

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

    ```
    fail2ban-map = cd /home/pi/fail2ban-map/script && python fail2ban_map.py
    ```

*  Move `script/fail2ban-map-action.conf` to fail2ban actions folder 

    ```bash
    mv /home/pi/fail2ban-map/script/fail2ban-map-action.conf /etc/fail2ban/action.d/
    ```
    
* Add the action to your `jail.conf` or `jail.local`

    ```
    # The simplest action to take: ban only
    action_ = %(banaction)s[name=%(__name__)s, port="%(port)s", protocol="%(protocol)s", chain="%(chain)s"]
              fail2ban-map-action
    ```

* (Optional) Change the tile provider in `public/fail2ban-map.js`

    ```javascript
    // list of tile providers can be seen here: https://leaflet-extras.github.io/leaflet-providers/preview/
    L.tileLayer
      .provider("CartoDB.DarkMatterNoLabels", {
        noWrap: true, 
      })
      .addTo(map);
    ```
