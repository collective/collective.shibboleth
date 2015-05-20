.. contents::

Introduction
============

This package provides the ability for Plone users to log into a site via
Shibboleth, making use of the Shibboleth `Embedded Discovery Service`_ (EDS).
This allows Plone to be a Shibboleth Service Provider (SP) and self-host a
discovery service on the Plone login page.  A running Shibboleth responder,
configured to provide a JSON Discovery Feed (``DiscoFeed`` handler) is
required to populate the EDS listing.

.. _Embedded Discovery Service: https://wiki.shibboleth.net/confluence/display/EDS10/

In Action
=========

.. image:: https://github.com/collective/collective.shibboleth/blob/master/docs/screenshot.png?raw=true
   :scale: 75%
   :alt: EDS login portlet within Plone.

``collective.shibboleth``'s EDS portlet in action, being used with the
Australian and New Zealand Access Federations.  The icons shown will
automatically display an organisation's logo if provided within SAML metadata.
At present, neither of these example federations support the relevant
`metadata extensions
<https://wiki.shibboleth.net/confluence/display/EDS10/4.+Metadata+Considerations>`_
and default to showing no logo.


Features
========

* Provides fully-configurable Shibboleth EDS login portlet
* Hosts Shibboleth EDS resources from within Plone
* Integrates Shibboleth EDS styles with Plone's default Sunburst theme
* Changes Plone's login page to be pluggable via
  ``collective.pluggablelogin``.
* Assigns a default Shibboleth EDS login portlet to the pluggable login page.
* Modifies login link to prevent login form appearing in an overlay, because
  the portlet requires JavaScript.
* Adds a ``Shibboleth Authenticated`` role into Plone.
* Assigns the ``Shibboleth Authenticated`` role to all users logging in
  using this method.
* Alerts the user on first login as to their local account's password.
  Plone's PAS requires users have a password, and this allows Shibboleth users
  to access Plone via WebDAV, FTP and other non-federation methods.

Installation
============

Installation with Plone follows the standard practice of modifying your
Buildout configuration like so, adding this package to your list of eggs::

    [instance]
    recipe = plone.recipe.zope2instance
    ...
    eggs +=
        collective.shibboleth

Re-run Buildout, restart Plone and activate the add-on.  This will configure a
default Shibboleth portlet on your login page.  You now need to ensure your
Shibboleth responder is configured accordingly, see `Technical details`_.

.. note::

   The default Shibboleth EDS currently switches language based upon the
   user's settings in their browser.  The default language setting in the
   Shibboleth portlet within Plone configures the the current site settings as
   default when the user's language isn't available. Note that language
   support for the EDS is currently limited so you may need to adjust the
   portlet's setting to pick a suitable fallback.

You may use Plone's GenericSetup infrastructure within another package or site
policy product to either reconfigure this default portlet or to create your
own.


Technical details
=================

Your webserver and Shibboleth Service Provider (SP) must be configured in two ways:

* With a Discovery Feed for the EDS. See `Configuring Shibboleth for the
  EDS`_; and
* To handle the login process and feed user attributes to Plone. See
  `Shibboleth authentication configuration`_


Configuring Shibboleth for the EDS
----------------------------------

Follow the instructions on the Shibboleth Wiki at
https://wiki.shibboleth.net/confluence/display/EDS10/3.+Configuration under
*Configuing the Service Provider*.  Your configuration may need to differ
from the instructions given.  The one mandatory configuration step is setting
up the ``DiscoveryFeed`` handler.

Your EDS configuration options (set in ``idpselect_config.js``) are
configured within Plone when you create the Shibboleth EDS portlet.


Shibboleth authentication configuration
---------------------------------------

There are two ways you can authenticate users to your site using Shibboleth:
either actively, by forcing a session for certain resources, or passively, by
only passing through authentication information if a session exists.  More
information about this in terms of Shibboleth can be found at
https://wiki.shibboleth.net/confluence/display/SHIB2/NativeSPProtectContent.

In a Plone context, using ``collective.shibboleth``, you thus have two choices:

#. Configure Shibboleth and your front-end webserver to be **passively** aware
   of your application. After an authentication session has been created,
   session details will automatically be added to incoming requests for Plone
   to accept; or

#. Configure Shibboleth and your front-end webserver to **require** a session
   for all or part of your site's URLs.  When a user visits the relevant URL
   or path, authentication will be requested and the user redirected to the
   relevant Discovery Service.


How Plone handles this authentication
-------------------------------------

The first option above is able to be more seamless as you can utilise a EDS
login portlet inside Plone, rather than having a jarring jump to a Discovery
Service or WAYF page.

By default, the underlying PAS plugin (``Products.AutoUserMakerPASPlugin``)
that listens for Shibboleth headers is configured to accept these on *any* site
URL.  For a default Plone install, a ``plone.session`` PAS plugin is configured
(the one that normally handles authentication), and this will create a session
and take over authentication from here on out whilst a user is logged in. 

To most efficiently manage this, the suggestion is to configure Shibboleth to
protect just the ``logged_in`` view for Plone, and configure this URL as the
return point (either via the EDS portlet, or via a URL parameter). The EDS
portlet will default to this automatically (but can be customised).  This way,
you can be sure that Shibboleth attributes will only be passed into Plone when the user
accesses this specific path.  As this path is typically only used during login,
you'll be reducing the load time and processing required for the rest of the
user's session.

The suggested flow is thus:

#. Configure Shibd Discovery Handler and protect ``/logged_in`` path with
   Shibboleth.
#. Install this package in Plone and configure the Shibboleth EDS portlet on
   the pluggable login page.

Now, when the user comes along:

#. User clicks ``Login`` in Plone
#. User is shown the EDS portlet, consisting of a list of Identity Providers
   (IdPs)
#. User selects an IdP and is taken to the IdP login page, or redirected
   transparently if the user is already authenticated with their IdP.
#. User is redirected back to Plone and logged in automatically. Behind the
   scenes, Shibboleth has injected the attributes into the user's request to
   ``logged_in`` and ``Products.AutoUserMakerPASPlugin`` has created that user
   an account.

The user's session has now been created and they're ready to use Plone without
relying on Shibboleth attributes.

.. note::

   This configuration may or may not suit your requirements depending on your
   site, security needs or federation.  This packages endeavours to fit all
   requirements so please raise an issue about your specific situation.

   For example, if you require that your user's authentication in Plone is
   *directly* tied to their Shibboleth session, then you'll need to disable
   the Plone session plugin's ability to ``authenticateCredentials`` and to
   configure the Shibboleth SP such that the entire Plone URL/path is
   protected.

   This will result in the upstream Shibboleth instance passing along
   authentication headers for every request.  Note that this is arguably
   ineffecient since both the Shibboleth SP and Plone's user setup machinery
   are being invoked or consulting for each and every request.


About the included Embedded Discovery Service (EDS)
---------------------------------------------------

This package uses the Shibboleth EDS as provided by the main Shibboleth
project.  Distributions of the EDS are available at
http://download.opensuse.org/repositories/security:/shibboleth/ and the source
is available from http://svn.shibboleth.net/view/js-embedded-discovery/.

The EDS is configurable as the Shibboleth login portlet.  This portlet can be
added to any page, though is most useful on the pluggable login page that is
configured by this package.

The included EDS distribution has been customised using the included patch
file (``src/collective/shibboleth/browser/shibboleth-ds-plone.patch``) in the
following ways:

* Allow configuration of the EDS using a ``data-options`` attribute on the
  DOM element.  Typically, the configuration function had to edited by hand.
* Adjust or remove some styles that conflict with Plone's defaults.

The patch is primarily required because the ``idpselect_config.js`` file
hard-codes a large structure of language information.  We are working with the
Shibboleth project on improving their JavaScript and incorporating the patch
back upstream.

For now, to reapply the patch to a new version of the EDS, do::

    cd src/collective/shibboleth/browser/
    patch -p5 < shibboleth-ds-plone.patch
    # Commit the result once patch is checked

