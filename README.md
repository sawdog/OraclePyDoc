OraclePyDoc
===========

README
------

A package to generate rst formated documentation of a schema in oracle.  This includes the ability to generate minimal erd diagrams, and includes all objects within the schema.  After generating the rst documentaiton, running that as a sphinx doc project makes a sweet set of operational/development documentation.

See README_oraschemadoc for the old readme on the project this was forked from.

TODO
----

This is just a generic list of todo items....

- Abstract the formatting and writing from one another, so it's not so tightly
  coupled.  Right now it's just handled serially in a very functional way.  I'd
  like to see this broken out so that it's more generic - and any kind of
  formatting/formatters will be possible easily.
