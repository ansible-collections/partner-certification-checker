# Certifying Ansible collections

This repository helps Red Hat partners check their Ansible content against minimum requirements for certification on Ansible Automation Hub.

## Certification checks

This repository provides GitHub workflows to perform sanity and lint tests as part of the [Red Hat certification workflow guide](https://connect.redhat.com/sites/default/files/2025-06/Ansible-Certification-Workflow-Guide202506.pdf).
The purpose of these certification checks is to identify common errors in the Ansible Automation Hub import process.
You should run these checks before uploading Ansible collections to Automation Hub.

Certification checks are not a substitute for a comprehensive testing strategy.
You should add unit and integration tests for robust test coverage that validates the functionality and behavior of your modules, plugins, and roles.

## Preparing collections for certification

Before uploading your collection to Ansible Automation Hub, you should verify that it meets certification requirements.
Follow instructions in the [Red Hat certification workflow guide](https://connect.redhat.com/sites/default/files/2025-06/Ansible-Certification-Workflow-Guide202506.pdf) to ensure that your collection meets all requirements.

Some common reasons for certification rejections include:

- Missing or unclear sections in the project README.
Refer to the [Ansible Certified Collections README Template](https://access.redhat.com/articles/7068606) for all information that your README must contain.
- Missing changelog entries for each collection version.
We recommend using the [antsibull-changelog](https://docs.ansible.com/projects/antsibull-changelog/) tool for changelog generation.

Additionally, certified collections must follow guidelines for dependency management such as:

- Python dependencies must be declared in a `requirements.txt` file with either a lower bound constraint, `>=x.x.x`, or not fixed to a version.
- Python dependencies must not include `ansible` or `ansible-core`.
- Ansible collection dependencies can exist only if the dependency is also a certified collection.

## Adding certification checks to your repository

To run the certification checks against pull requests and on schedule:

1. Copy the [Ansible collection certification GitHub Actions workflow](https://github.com/ansible-collections/certification/blob/main/.github/workflows/certification.yml) to the `.github/workflows` directory of your collection repository.
1. Navigate to the `Actions` tab of the collection repository and then verify the workflow is enabled. 
1. If Ansible Lint checks fail on files unrelated to the collection's core functionality, add an [.ansible-lint](.ansible-lint) file to your collection's root directory and list all files and directories you want Ansible Lint to ignore.
1. If there are sanity test failures that cannot be fixed and are [allowed to ignore](https://docs.ansible.com/projects/lint/rules/sanity/), create a [sanity ignore file](https://docs.ansible.com/projects/ansible/devel/dev_guide/testing/sanity/ignores.html#ignore-file-location) for each affected version of ansible-core (for example, `tests/sanity/ignore-2.18.txt`) and add corresponding entries.

### Updating the test matrix

You must update the list of `ansible-core` versions in the `Sanity` job of the `.github/workflows/certification.yml` workflow when new versions of `ansible-core` are released.
Refer to default `ansible-core` versions in the `Ansible Automation Platform Installation Requirements` section of the [Red Hat Ansible Automation Platform Life Cycle](https://access.redhat.com/support/policy/updates/ansible-automation-platform#installation) document.
