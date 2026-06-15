# Red Hat partner certification checker

This repository provides Red Hat partners with GitHub workflows that check collections for minimum requirements for certification on Red Hat Ansible Automation Hub (Automation Hub).

## Purpose of certification checks

To upload Ansible collections to Automation Hub, Red Hat partners must satisfy certification requirements.
Those requirements include running sanity and lint tests against collections during the Automation Hub import process.

In cases where those tests fail or highlight breaking issues, the collection uploads are rejected.
This requires Red Hat partners to address the issues and resubmit their collections, which results in additional development and release cycles.

The certification checker provides Red Hat partners with the ability to assess the readiness of collections for certification.
It is a minimal tool intended to reduce the likelihood of rejection by identifying common errors that Red Hat partners can fix before uploading to Automation Hub.

> Certification checks are not a substitute for a comprehensive testing strategy.
> You should add unit and integration tests for robust test coverage that validates the functionality and behavior of your modules, plugins, and roles.

## Adding certification checks to your repository

To run the certification checks against pull requests and on schedule:

1. Copy the [Ansible collection certification GitHub Actions workflow](https://github.com/ansible-collections/partner-certification-checker/blob/main/.github/workflows/certification.yml) to the `.github/workflows` directory of your collection repository, for example:
    ```bash
    git clone git@github.com:ansible-collections/partner-certification-checker.git
    cp partner-certification-checker/.github/workflows/certification.yml path/to/repository/.github/workflows/
    ```
1. Add an [.ansible-lint](https://github.com/ansible-collections/partner-certification-checker/blob/main/.ansible-lint) configuration file to the root directory of your collection.
1. List any files and folders that are not related to the collection's core functionality, such as `.github/`, to the `exclude_paths` option.
This prevents Ansible Lint rule violations in those files and folders.
1. Commit and push the changes to your repository.
1. Navigate to the `Actions` tab of your repository and verify that the workflow is enabled.
1. (Optional but recommended) Add a [.github/dependabot.yml](https://github.com/ansible-collections/partner-certification-checker/blob/main/.github/dependabot.yml) configuration file to your repository. When a new version of the certification workflow is released, Dependabot automatically opens a pull request to update your repository. For more information about Dependabot, see the [official documentation](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/dependabot-quickstart-guide).

### Ignoring sanity failures

The certification checker might report sanity test failures that cannot be fixed and should be ignored.
In this case you should do the following:

1. Review the list of [currently allowed ignores](https://docs.ansible.com/projects/lint/rules/sanity/).
1. Create a [sanity ignore file](https://docs.ansible.com/projects/ansible/devel/dev_guide/testing/sanity/ignores.html#ignore-file-location) for each affected version of ansible-core (for example, `tests/sanity/ignore-2.18.txt`).
1. Add the corresponding entries to the sanity ignore files.
1. Commit and push the changes to your repository.

## Tested ansible-core branches and Python versions

The certification checker runs sanity tests against the following ansible-core branches, aligned with downstream Execution Environments:

- `stable-2.16`
- `stable-2.18`
- `stable-2.20`

The GitHub Actions `ansible-lint` and `galaxy-importer` jobs use Python 3.12, matching downstream Execution Environments.

The default ansible-core version for the build-import and lint jobs is `2.16.0`.

## Using the standalone workflow

The `.github/workflows/certification.yml` workflow file calls a reusable workflow that the Ansible Community and Partner Engineering team at Red Hat maintain.
If you want to modify and maintain the certification checker, you can use the `.github/workflows/certification-static.yml` workflow file instead.

You must update the list of `ansible-core` versions in the `sanity.strategy.matrix.ansible` section of the workflow when new versions of `ansible-core` are released.
Refer to default `ansible-core` versions in the `Ansible Automation Platform Installation Requirements` section of the [Red Hat Ansible Automation Platform Life Cycle](https://access.redhat.com/support/policy/updates/ansible-automation-platform#installation) document.
