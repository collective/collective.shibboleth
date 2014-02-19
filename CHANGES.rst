Changelog
=========

1.2 (2014-02-19)
----------------

- Made the embedded WAYF JavaScript URL depend on the portlet's
  configured URL rather than being hardcoded.
  [davidjb]


1.1 (2014-01-30)
----------------

- Noted that latest collective.pluggablelogin released. Package now
  depends on this latest version or later.
  [davidjb]


1.0 (2014-01-29)
----------------

- If logging in again from a logged_out view, then strip the view from
  the ``came_from`` query string parameter. 
  [davidjb]
- Notify users of their temporary passwords being generated on first login.
  [davidjb]
- Monkey patch the password generation function AutoUserMakerPASPlugin
  to allow stronger passwords.
  [davidjb]
- Ensure users logging in get the Shibboleth Authenticated role via
  AuthZ mapping.
  [davidjb]
- Add Shibboleth Authenticated role.
  [davidjb]
- Package created using templer
  [davidjb]
