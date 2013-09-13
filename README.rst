.. contents::

Introduction
============

Authentication integration layer for the Australian Access Federation (AAF) and Plone

Embedded WAYF portlet
---------------------

Uses the Shibboleth Embedded WAYF as provided by:
https://ds.aaf.edu.au/discovery/DS/embedded-wayf.js/snippet.html
or 
https://wayf.switch.ch/SWITCHaai/WAYF/embedded-wayf.js/snippet.html

-- configurable in the Shibboleth portlet.  This should probably be
refactored out into its own portlet later on.

The Shibboleth project also has an `Embedded Discovery Service <https://wiki.shibboleth.net/confluence/display/EDS10/Embedded+Discovery+Service>`_ that exists
and can be self-hosted.  This portlet will likely be migrated to that at
some point in the near future.

