Changelog
=========

1.1.2 (2015-06-19)
------------------

- Fix issue with users not returning to ``came_from`` URL if they were
  prompted to login.  This fix will be incorporated upstream in the EDS
  shortly.
  [davidjb]


1.1.1 (2015-05-20)
------------------

- Minor changes to readme and package description.
  [davidjb]


1.1 (2015-05-20)
----------------

- Nothing changed yet.


1.0 (2015-05-20)
----------------

- Upgrade EDS to r157 for recent bug fixes.
  [davidjb]
- Assign a portlet onto the Pluggable Login page on installation.
  [davidjb]
- Change from a Embedded WAYF to Shibboleth's EDS.
  [davidjb]
- Remove old ``collective.aaf`` code from this package; that package now
  depends on this one.
  [davidjb]
- Refactor from ``collective.aaf``, and turn collective.aaf into an AAF-specific
  layer on top of this package.
  [davidjb]


