#############
Configuration
#############

There are two methods of configuring the system. The first method is forced upon you when starting a new installation. The second method is by virtue of Djangorifa's admin site.

********
Method 1
********

When install_djangorifa.sh has successfully been run, start the test server and navigate to the URL indicated (most likely http://127.0.0.1:8000). Alternatively, point your Apache or Nginx or whatever server to the wsgi.py script and head to the IP address / domain name specified by that setup.

As you will not be logged in, the forced installation will not work. Therefore, go to ``/accounts/login/`` and login with the information you provided when creating a Django superuser.

This should automatically redirect you to the URL ``/taarifa_config/setupforthefirstime/``. The first page will ask for a ``Domain name`` and ``Display name``. Djangorifa relies on Django's inbuilt sites framework to store configuration settings. This first form is configuring that. Set the domain name to whatever your site happens to be. If only running locally, set to your test server URL. This is important. The default setting is ``example.com`` and some parts of the site will therefore try to render URLs as pointing to ``example.com`` and this will cause errors. Set the display name to whatever you want.

Submit will bring you to a page with a drop-down list ``Site`` and a map ``Bounds``. The ``Site`` drop-down is populated with whatever you filled in on the previous form's display name. The ``Bounds`` map is to constrain where reports can be made. This is an editable map with polygons. Click the blue Edit button in the top right corner of the map. The default setting is edit mode. Click on the map and add points to bound. Double click to finish setting. If not happy, click anywhere to start again, or click the far-left button on that top-right menu to edit the polygon already drawn. Once happy with the regions of the map, click submit.

The site is now configured.

********
Method 2
********

Go to ``/admin/`` and on the right hand side there is a pane entitled ``Configuration``. Under the tab ``wizard`` there is a link to run the wizard again. Under ``Individual``, there is ``Configuration`` and ``Sites``. ``Configuration`` will show the map page and sites will enable you to edit the domain name.
