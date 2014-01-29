.. contents::

Introduction
============

This package provides an integration layer for Plone for the `Australian
Access Federation <http://aaf.edu.au>`_ (AAF), a Shibboleth-powered
authentication federation.

Features
========

Generic
-------

The following features could and probably should be refactored into a 
general ``collective.shibboleth`` package.  For the inclined, please contact
us and we'll work through it together.

* Embedded WAYF portlet (suitable for SWTICH-compatible Shibboleth Discovery
  Services (such as SWITCHaai, Australian Access Federation (AAF), and possibly
  more).
* Modifies login link to prevent login form appearing in an overlay, because
  the portlet requires JavaScript.
* Adds a ``Shibboleth Authenticated`` role into Plone.
* Assigns the ``Shibboleth Authenticated`` role to all users logging in
  using this method.


AAF-Specific
------------

* Configures the underlying authentication plugin to load user data from
  the relevant AAF attributes.
* Portlet value defaults are those from the AAF.

Installation
============

At the time of writing, this package relies upon one unreleased dependency:

* Products.AutoUserMakerPASPlugin

A new version of this package will be released and available on PyPI
as soon as possible.  In the meantime, installation from GitHub via a tool
such as `mr.developer <https://pypi.python.org/pypi/mr.developer>`_ is
recommended.

Techinical details
==================

Configuring Shibboleth (Shibd)
------------------------------

There are two ways you can authenticate users to your site using
Shibboleth, either actively, by forcing a session for certain resources,
or passively, by only passing through authentication information if a
session exists.  More information about this in terms of Shibboleth
can be found at https://wiki.shibboleth.net/confluence/display/SHIB2/NativeSPProtectContent.

In a Plone context, using ``collective.aaf``, you thus have two choices:

#. Configure Shibboleth and your front-end webserver to be **passively**
   aware of your application. After an authentication session has been 
   created, session details will automatically be added to incoming requests
   for Plone to accept; or
#. Configure Shibboleth and your front-end webserver to **require** a session
   for all or part of your site's URLs.  When a user visits the relevant URL
   or path, authentication will be requested and the user redirected to the
   relevant Discovery Service.

The first option is able to be more seamless as you can utilise a
login portlet inside Plone, rather than having a jarring jump to a WAYF or IdP
page. It also means you can provide an Identity Provider listing
*embedded* within your site, making the login process as clean as possible.

How Plone handles authentication
--------------------------------

By default, the underlying PAS plugin (``Products.AutoUserMakerPASPlugin``)
that listens for Shibboleth headers is configured to accept these on *any* site
URL.  For a default Plone install, a ``plone.session`` PAS plugin is configured
(the one that normally handles authentication), and this will create a session
and take over authentication from here on out whilst a user is logged in. 

To most efficiently manage this, the suggestion is to configure Shibboleth to
protect just the ``logged_in`` view for Plone, and configure this URL as the
return point (either via the WAYF portlet, or via a URL parameter). The
built-in default for the WAYF portlet will do this for you automatically.
This way, you can be sure that Shibboleth attributes will only be passed
at this specific path (only used during login, typically),
thus reducing the load time and processing required for the rest of the site.

.. note::

   This configuration may or may not suit your exact requirements depending on
   your configuration, federation (if not AAF), or other aspects. For example,
   if you require that your user's authentication in Plone is directly tied to
   their Shibboleth session, then you may wish to disable the Plone session
   plugin's ability to ``authenticateCredentials`` and to configure the
   Shibboleth SP such that the entire Plone URL/path is protected.  This will
   result in the upstream Shibboleth instance passing along authentication
   headers for every request.  Note that this is arguably ineffecient since
   both the Shibboleth SP and Plone's user setup machinery are being invoked
   for each and every request.


Embedded WAYF portlet
---------------------

This package uses the Shibboleth Embedded WAYF as provided by:

https://ds.aaf.edu.au/discovery/DS/embedded-wayf.js/snippet.html
or 
https://wayf.switch.ch/SWITCHaai/WAYF/embedded-wayf.js/snippet.html

and is configurable in the Shibboleth portlet.  

This could probably be refactored out into its own portlet later on. However,
the Shibboleth project also has an `Embedded Discovery Service
<https://wiki.shibboleth.net/confluence/display/EDS10/Embedded+Discovery+Service>`_
that exists and can be self-hosted.  The portlet provided by this package
will likely become modified to use this at some point in the near future.

