===========
 proptools
===========

A module providing three useful property subtypes:

``LazyProperty``
  Permanently cache a read-only property's dynamically computed value.

``TypedProperty``
  Check the type on all property assignments, raising TypeError on failure.

``SetOnceProperty``
  Allow the property to be set once, raising AttributeError on subsequent writes.
