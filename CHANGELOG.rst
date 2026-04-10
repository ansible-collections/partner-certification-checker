===========================================
Partner Certification Checker Release Notes
===========================================

.. contents:: Topics

v1.0.0
======

Release Summary
---------------

This is the first major release of the Red Hat partner certification checker.
This changelog contains all changes to the workflows in this project
that have been made after the previous release.

Minor Changes
-------------

- certification.yml, certification-reusable.yml - Add the ``ansible-core-version`` input to pass an ansible-core version to use for collections that support higher versions than the one that runs on Automation Hub.
- certification.yml, certification-reusable.yml - Add the ``collection-root`` input to use in collections which do not reside at the root of the repository.
- certification.yml, certification-reusable.yml - Add the ``python-versions`` input to pass a JSON list of Python versions to test against in the sanity matrix.

New Modules
-----------

- sample_module - A custom module plugin for Ansible.

v0.1.0
======

Release Summary
---------------

The first release of the certification-reusable workflow.

Minor Changes
-------------

- Added certification-reusable.yml: called by certification.yml
- Added certification-static.yml: experimental, uses latest versions of tools
- Added certification.yml: supposed to be copied to partners' repos
- Added test-reusable.yml: for testing certification-reusable.yml
