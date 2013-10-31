Changelog
=========

0.1-dev (unreleased)
--------------------

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
