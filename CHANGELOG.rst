Changelog
=========

v1.1.3 (2018-03-07)
-------------------
- CS-479 Add CloudPassageRateLimit Exception Class. [Jye Lee]


v1.1.2 (2018-02-26)
-------------------
- Adding tests for TimeSeries() for events, scans, and issues endpoints.
  [Ash Wilson]
- Adding docs for TimeSeries class. [Ash Wilson]
- CS-458 Python SDK: Move multiple servers into a target group. [Hana
  Lee]


v1.1 (2018-01-05)
-----------------
- V1.1. [Hana Lee]
- CS-426 add Agent Upgrades class. [Hana Lee]
- CS-428 Add CveDetails class. [Hana Lee]
- CS-428 Add CveDetails class. [Hana Lee]
- CS-429 add cve exceptions class. [Hana Lee]
- Conflict. [Hana Lee]
- CS-427 add processes endpoint to servers class. [Hana Lee]
- CS-427 add processes endpoint to servers class. [Hana Lee]
- Add Accept-Encoding 'gzip' [Jye Lee]
- Add Accept-Encoding 'gzip' [Jye Lee]
- CS-359 Added traffic discovery endpoint to Server and ServerGroup
  classes. [Hana Lee]
- Rev to v1.0.6.8. [Jye Lee]
- Rev to v1.0.6.7. [Jye Lee]
- CS-322 Fix naming from Server to Issue. [Jye Lee]
- V1.0.6.6. [Jye Lee]

  flake8: expected 2 blank lines, found 1
- This is it @2. [Hana Lee]
- This is it. [Hana Lee]
- Test: see travis. [Hana Lee]
- Test:add +x. [Hana Lee]
- Test: use travis.sh. [Hana Lee]
- Test: edit yml. [Hana Lee]
- Test: travis.sh. [Hana Lee]
- Test: script onlt. [Hana Lee]
- Test: added if statement. [Hana Lee]
- Test: took up typo. [Hana Lee]
- Added echo branch. [Hana Lee]
- Test: added travis after_success. [Hana Lee]
- Test: print env. [Hana Lee]
- Test: run py.test. [Hana Lee]
- Test: run test_wrapper.sh. [Hana Lee]
- Test: added ls. [Hana Lee]
- Test: remove --it. [Hana Lee]
- Test: show docker images. [Hana Lee]
- Test: added image id. [Hana Lee]
- Test: put docker run in before_install. [Hana Lee]
- Test: using docker exec to run test_wrapper.sh. [Hana Lee]
- Added test_wrapper.sh. [Hana Lee]
- Edited the changelog. [Hana Lee]
- Added converge version lock. [Hana Lee]
- Added email notification. [Hana Lee]
- Fix logic in api_key_manager class. [Hana Lee]
- Modified pagination for servers endpoint. [Hana Lee]
- Fixed logic in api key manager. [Hana Lee]

  rev init to 1.0.6.3
- Fixed logic in api key manager. [Hana Lee]
- Bug/CS-283 fix kwargs params if 500. [Jye Lee]

  remove unexpected spaces around =
- Rev to 1.0.6.2. [Jye Lee]
- Bug CS-269 edit doc server_id to issue_id. [Jye Lee]


v1.0.6 (2017-05-01)
-------------------
- Rev to v1.0.6. [Jye Lee]
- Fixed flake8. [Hana Lee]
- Added LocalUserGroup to __init__.py Fixed typo in server.py. [Hana
  Lee]
- Fixed status_code 500s. [Hana Lee]
- CS-267 add local user account endpoint to SDK. [Hana Lee]
- CS-269 add issues endpoint to the SDK. [Jye Lee]

  added list_all, describe, and resolve methods
- CS-259. [Jye Lee]

  Add delayed retry to http helper
- Added required openssl version and python version. [Hana Lee]


v1.0.5 (2017-02-18)
-------------------

Changes
~~~~~~~
- Improvents to list FIM baseline with detail information. [Hana Lee]

Other
~~~~~
- Fixed Flake8 styling issue. [Hana Lee]
- Changed the output FIM baseline to include more detail information.
  [Hana Lee]
- Change the child server group name to avoid "Name Peer groups cannot
  have the same name" [Hana Lee]


v1.0.4 (2017-01-31)
-------------------
- Rev to v1.0.4. [Jye Lee]
- Fixes firewall log paging. [Spencer Herzberg]


v1.0.3 (2017-01-24)
-------------------

Changes
~~~~~~~
- Improvements to server group creation, use grid-side input
  sanitization for post data. [Ash Wilson]

Other
~~~~~
- Rev setup.py version to 1.0.3. [Jye Lee]
- Rev to v1.0.3 to changelog. [Jye Lee]
- Scan history should use since and until. [Spencer Herzberg]


v1.0.1 (2016-12-02)
-------------------

Changes
~~~~~~~
- Docker image now builds with git inside, syntax fix in testing script.
  Set default value in ApiKeyManager for api_port to 443.  New testing
  procedure implemented and documented. [Ash Wilson]
- Re-ordering operations in test_wrapper.sh to better converge testing
  file for api_key_manager.py.  Altered unit tests to point to converged
  config file.  Installed package in editable mode within container in
  order to get coverage module working. [Ash Wilson]
- Changed values in portal.yaml file to facilitate testing automation
  with test_wrapper.sh. [Ash Wilson]
- Added test_wrapper.sh to replace bare command in Dockerfile.  This
  allows for dynamic testing behavior, depending on the environment
  variables passed into the container at runtime. [Ash Wilson]
- Consolidated testing procedure in official, built docs.  Links
  provided in README.rst and README.md to published docs containing
  testing procedure. [Ash Wilson]

Fix
~~~
- Fix: test: Corrected logic for running codeclimate (thanks @mong2)
  [Ash Wilson]

Other
~~~~~
- Remove -z from codeclimate if statement. [mong2]


v1.0 (2016-11-21)
-----------------
- Revert "remove whitelist and pagination for policies and events"
  [mong2]
- Updating CHANGELOG. [Ash Wilson]
- Changing version to 1.0, removing beta references. [Ash Wilson]
- Adding unit tests for useragent string composition. [Ash Wilson]
- Correcting ordering of user agent string composition. [Ash Wilson]
- Adding integration strings to integration tests. [Ash Wilson]
- Correcting UA string building logic. [Ash Wilson]
- Formatting user agent more like RFC 2616 says we should. [Ash Wilson]
- Fixed sanitizer. [Hana Lee]
- Fixed server.py to align with flake8. [Hana Lee]
- Added url sanitizer. [Hana Lee]
- Fixed expires and comments in fim_baseline create. [Hana Lee]
- Take out whitelist from event. [Hana Lee]
- Updating server.py. [Jye Lee]
- Remove supported_search_fields from servers. [Jye Lee]
- Revert "remove whitelist and pagination for policies and events" [Jye
  Lee]

  This reverts commit b78e40d52f08984623772417fea1660122584987.
- Revert "remove supported_search fields and get_paginated for scan,
  server, and server_group class/tests" [Jye Lee]

  This reverts commit 906b1e39e55b8155340cbae340d4e8e2c813f508.
- Remove supported_search fields and get_paginated for scan, server, and
  server_group class/tests. [Jye Lee]
- Remove whitelist and pagination for policies and events. [Hana Lee]
- Correcting installation document. [Ash Wilson]
- Documentation improvements.  Building changelog into docs, adding
  version indicator to index. [Ash Wilson]
- Adding links to built documentation. [Ash Wilson]
- Improve README.rst formatting. [Ash Wilson]
- Improving setup.py to include changelog in long description, which is
  published on PyPI. [Ash Wilson]


v0.101 (2016-10-18)
-------------------

New
~~~
- .gitchangelog.rc now takes latest version from
  cloudpassage/__init__.py. [Ash Wilson]

Fix
~~~
- Flake8 correction in __init__.py. [Ash Wilson]
- CS-66 Remove ImportError exception for unsupported Python version.
  [Ash Wilson]
- CS-66 implement soft failure for wrong Python version. [Ash Wilson]
- Correcting docs build isssues, change revision to v0.101. [Ash Wilson]

Other
~~~~~
- Add all supported search fields for servers endpoint. [Jye Lee]


v0.100 (2016-10-11)
-------------------

Fix
~~~
- Typo = should be == in requirements-testing.txt. [Jye Lee]

Other
~~~~~
- Adding CHANGELOG.md. [Ash Wilson]
- Adding .gitchangelog.rc. [Ash Wilson]
- Forget to && between commands. [Jye Lee]
- Add apt-get install git to Dockerfile. [Jye Lee]
- Add pytest-cov to requirements-testing and codeclimate pkg install to
  Dockerfile. [Jye Lee]
- Clean up pep8 error blank line at end of file. [Jye Lee]
- Add group_name to servers.list_all() supported fields Add parent_id to
  server groups create and update. [Jye Lee]
- CS-55 fix get sam target_id to get linux only. [Jye Lee]
- CS-53 swap the order of sdk_version_string and integration_string.
  [Jye Lee]
- CS-41-2 remove sam last_scan_results retrieve. [Jye Lee]
- Fixing testing deps. [Ash Wilson]
- CS-33 adding documentation for exception kwargs. [Ash Wilson]
- CS-37 Corrected bad path, which was breaking doc build. [Ash Wilson]
- Documentation improvements. [Ash Wilson]
- CS-40 Improve user_agent string composition. [Ash Wilson]
- CS-39 added get_sdk_version() to utility. [Ash Wilson]
- CS-2 missed import libraries. [Jye Lee]
- CS-2 fix alert_profile, does not have a self.policy_key. [Jye Lee]
- Pinning pyflakes to 1.2.3. [Ash Wilson]
- CS-25 fixing spelling and variable naming in __init__.py. [Ash Wilson]
- CS-25 correcting unnecessary import of sys module. [Ash Wilson]
- CS-25 re-structuring version comparator. [Ash Wilson]
- Adding travis-ci build badges for master and develop branches. [Ash
  Wilson]
- Fixing docs for API key manager. [Ash Wilson]
- CS-34 flake8 integration tests. [Ash Wilson]
- CS-35 Make unit tests flake8 compliant. [Ash Wilson]
- Sanitize exception error codes. [Ash Wilson]
- CS-32 Re-tooling to work with flake8 v3.0. [Ash Wilson]
- CS-23 pep8 event integration tests. [Ash Wilson]
- Pointed to file that would be in an environment not configured for
  integrationt testing. [Ash Wilson]
- Re-arranging tests for special events policy, getting rid of
  conflicting test for NotImplementedError exception. [Ash Wilson]
- Fixes to ease transition to flake8. [Ash Wilson]
- CS-31 moved from pep8 to flake8. [Ash Wilson]
- Requirements file for testing added, updated dockerfile for flakes
  testing. [Ash Wilson]
- Removing duplication detector- we will use pyflakes. [Ash Wilson]
- First stab at codeclimate. [Ash Wilson]
- Adding codeclimate badges to READMEs. [Ash Wilson]
- CS-18 Adding RST for pypi pretties. [Ash Wilson]
- Dockerfile-based travis config is now working. [Ash Wilson]
- Fixing WORKDIR in Dockerfile. [Ash Wilson]
- Add -y to apt-get install. [Ash Wilson]
- Travis to use docker for testing SDK. [Ash Wilson]
- Correcting grammar in LICENSE. [Ash Wilson]
- Restructuring test script. [Ash Wilson]
- First stab at .travis.yml. [Ash Wilson]
- Added pyflakes config. [Ash Wilson]
- CS-17 remove print and move bad_statuses into if. [Jye Lee]
- CS-7 adding python veresion check. [Hana Lee]
- CS-7 do not support less than python 2.7.10. [Jye Lee]
- Used systemError and added unit test for python version CS-7. [Hana
  Lee]
- All references to version number point back to __init__.py file. [Ash
  Wilson]
- LICENSE. [Ash Wilson]

  Adding license file

  CS-8 added issues endpoint to server.py

  Update test_integration_server.py

  CS-8 update agent_firewall_logs to have pagination
- DOC - Adding specific tested and supported minimum Python version.
  [Ash Wilson]
- Cleaning up bad commit, redefined methods, and pep8 issues. [Ash
  Wilson]
- Changed from repr to str method to prevent inclusion of superfluous
  quotes in string. [Ash Wilson]
- Fixing pep8. [Ash Wilson]
- Update gitignore. [Ash Wilson]
- CS-14 Add ability and instructions for building PDF docs. [Ash Wilson]
- CS-5 Change (true | false) to (bool) [Jye Lee]
- CS-5 Add Critical to support search field for events, Added to
  DocString. [Jye Lee]
- CS-2 CRUD for alert_profiles, Fixes squashed. [Jye Lee]
- CS-3 Remove sam from supported_historical_scans list. [Jye Lee]
- CS-3 Remove sam from supported_historical_scans list. [Jye Lee]
- CS-4 Add Describe to Special Events Policies. [Jye Lee]
- CS-6 update scan finding comment to include CSM and SVA. [Jye Lee]
- Add exception message feature/CS-13. [Hana Lee]
- Adding __str__ to exceptions. [mong2]

  such that error messages will be printed


v0.99 (2016-09-02)
------------------
- LICENSE. [Ash Wilson]

  Adding license file
- Improved parsing. [Ash Wilson]
- Enhanced README. [Ash Wilson]
- Changing to v0.99 for beta period. [Ash Wilson]
- Adding requests to requirements.txt. [Ash Wilson]
- Fixed pep8 issue with == vs is. [Ash Wilson]
- Coe-230 force key and secret to string. [Ash Wilson]
- Coe-229 fixed type issues with api key manager, rev setup to 1.0. [Ash
  Wilson]
- Remove unnecessary print statement. [Ash Wilson]
- Coe-191 coe-192 Tests use port number, soft fail-around for lack of
  key scope. [Ash Wilson]
- COE-117 Add cleanup routines for better smoking. [Ash Wilson]
- COE-158 fix get_sam_target. [Ash Wilson]
- COE-158 fix get_sam_target. [Ash Wilson]
- Adding test cases. [Ash Wilson]
- Coe-153 Bring test coverage to 95% [Ash Wilson]
- Coe-149 coe-150 pylint 10/10, deduplication of functionality. [Ash
  Wilson]
- Coe-148 Corrected cyclic import issue in cloudpassage.sanity. [Ash
  Wilson]
- Coe-152 Documentation update. [Ash Wilson]
- Coe-152 Documentation update. [Ash Wilson]
- Coe-151 Add instructions for new testing layout. [Ash Wilson]
- Coe-131 coe-143 coe-147 update documentation, separate tests by type,
  pylint http_helper. [Ash Wilson]
- Coe-144 coe-142 create test cases for new functions. [Ash Wilson]
- Coe-133, 132, 130, 129, 128, 127 pylint cleanup. [Ash Wilson]
- Coe-135, 136, 137, 138, 139 pylint cleanup. [Ash Wilson]
- Coe-140 pylint 10/10 utility.py. [Ash Wilson]
- Coe-141 Add docstrings to methods that will fail if run against an
  empty account. [Ash Wilson]
- Coe-126 10/10 pylint for event.py. [Ash Wilson]
- Coe-125 pylint 10/10 for congifiguration_policy.py. [Ash Wilson]
- Coe-122 Pylint 10/10, removed overrides.  Refactored
  api_key_manager.py. [Ash Wilson]
- Coe-124 pylint __init__.py. [Ash Wilson]
- Corrected docstrings for pylint. [Ash Wilson]
- COE-118 pylint cloudpassage/ [Dave Doolin]
- Completed testing docs. [Ash Wilson]
- COE-120 bring test coverage to 90%, make corrections in
  FirewallBaseline. [Ash Wilson]
- COE-85 Cleanup of test_halo.py, test coverage improvements. [Ash
  Wilson]
- COE-109 Cleaned up api_key_manager a bit, added since/until query for
  scans. [Ash Wilson]
- COE-111 COE-114 Added api key manager, refactored tests to be atomic,
  added docs. [Ash Wilson]
- COE-112 Adding input sanity checking for URLs constructed from method
  args. [Ash Wilson]
- Coe-65 Change fn to utility, refactor all the things. [Ash Wilson]
- Coe-108 - also advancing version to 0.9.9. [Ash Wilson]
- Coe-108 changed name to hostname. [Ash Wilson]
- Coe-58 Added CVE exceptions query, tests, and docs. [Ash Wilson]
- Added server group delete method. [Ash Wilson]
- Coe-99 coe-100 Docmentation update. [Ash Wilson]
- Coe-86 coe-102 Added Events, improved test coverage and documentation.
  [Ash Wilson]
- Coe-104 coe-103 coe-60 coe-84 coe-98 coe-97 coe-96 coe-94 coe-90
  coe-89 coe-88 coe-87. [Ash Wilson]
- Coe-82 coe-92 coe-103 Implement inheritance for policies, cleanup docs
  and tests.  Complete firewall module. [Ash Wilson]
- Coe-101 Adding exclusion for html docs. [Ash Wilson]
- Coe-81 adding coverage to test runner. [Ash Wilson]
- Coe-18 autogenerating docs from docstrings. [Ash Wilson]
- Coe-80 coe-48 clean out imp, old cpapi functions. [Ash Wilson]
- Coe-73 Adding basic firewall policy management functionality. [Ash
  Wilson]
- Coe-72 Wrapping up FIM module. [Ash Wilson]
- Coe-71 Rounding off LIDS policy-related functionality. [Ash Wilson]
- Coe-78 Corrected setup.py, .gitignore. [Ash Wilson]
- Coe-74 rounding out server.Server functionality. [Ash Wilson]
- Coe-75 Expanding scans module. [Ash Wilson]
- Coe-77 Adding basedir and config for docs. [Ash Wilson]
- Coe-70 Adding configuration policy CRUD. [Ash Wilson]
- Coe-69 Added server.Server.describe() method. [Ash Wilson]
- Coe-64 Added server command details method. [Ash Wilson]
- Coe-68 adding ServerGroup.list_members() and tests. [Ash Wilson]
- Coe-67 Improve scan initiator and test cases. [Ash Wilson]
- Coe-63 Added scan initiator module.  Some integration tests will be
  fulfilled by coe-66. [Ash Wilson]
- Coe-59 Add fn.determine_policy_metadata() with tests. [Ash Wilson]
- Coe-44 add Server.retire() [Ash Wilson]
- Coe-55 add tests for fn.verify_pages() [Ash Wilson]
- Coe-57 Adding tests for sanity.py. [Ash Wilson]
- Coe-61 Adding SpecialEventsPolicy.list_all() [Ash Wilson]
- Coe-56 Add server group update capabilities. [Ash Wilson]
- Coe-51 Added pep8 checking to all tests and SDK, from within tests.
  [Ash Wilson]
- Coe-54 Added get_paginated(), tests, and moved ServerGroup.list_all()
  to it. [Ash Wilson]
- Coe-53 pep-8 all the things, stub out things too. [Ash Wilson]
- Coe-52 Created SystemAnouncement class. [Ash Wilson]
- Coe-42 Create method and test for describing server group. [Ash
  Wilson]
- Coe-50 Corrected according to comments on merge request. [Ash Wilson]
- Coe-47 adding HTTP method-specific components. [Ash Wilson]
- COE-45 Added test cases pursuant to ticket details. [Ash Wilson]
- COE-43 adding getServerDetails method. [Ash Wilson]
- COE-20 Added updateServerGroup() w/ sanity checking. [Ash Wilson]
- COE-40 Get halo.py passing pep8. [Ash Wilson]
- COE-39 removing artifacted cpapi.py and cputils.py. [Ash Wilson]
- Changing layout and naming of project, incorporating tests. [Ash
  Wilson]
- Added initiateScan() COE-36. [Ash Wilson]
- Added ldevlin's getAnnouncements() COE-34. [Ash Wilson]
- Deleting foo. [Ash Wilson]
- Updated cpapi to add group delete feature. [Ash Wilson]
- Testing. [Ash Wilson]
- Adding requirements. [Ash Wilson]
- Better catching of auth faulure. [Ash Wilson]
- Merged diff from cpapi.py in cpapi examples repo with this one.  See
  COE-9. [Ash Wilson]
- Added authTokenScope for exposing key access level. [Ash Wilson]
- Added gitignore. [Ash Wilson]
- Create README.md. [Ash Wilson]
- First commit for the CloudPassage Halo Python SDK. [Apurva Singh]


