# Red Hat Partner Certification Checker

This repository contains a reusable GitHub Actions [workflow](.github/workflows/certification.yml) to check whether an Ansible collection is ready for certification on Red Hat Ansible Automation Hub.

The workflow helps Red Hat partners catch common certification issues before uploading a collection to Automation Hub. Furthermore, the workflow file calls a [reusable workflow](.github/workflows/certification-reusable.yml) that the Ansible Community and Partner Engineering team at Red Hat maintain.

## What it checks

The certification checker runs the same types of checks used during the Automation Hub import process, including:

- [Galaxy importer](https://github.com/ansible/galaxy-importer) checks
- [Ansible Lint](https://docs.ansible.com/projects/lint/) checks
- [Ansible sanity](https://docs.ansible.com/projects/ansible/latest/dev_guide/testing/sanity/index.html) tests

These checks help reduce failed imports and repeat release cycles.

> [!IMPORTANT]
> This checker runs the types of checks used during the Automation Hub import process.
> The Ansible collection certification process has other [requirements](https://docs.ansible.com/projects/partner-certification-requirements/)
> which this checker does not cover.

> [!IMPORTANT]
> This checker is not a replacement for a complete test strategy.
> Use it alongside unit and integration tests for your modules, plugins, and roles.

## Quick start

Add the certification workflow to your collection repository.

1. Clone this repository.

1. Copy the certification workflow into your collection repository:

   ```bash
   cp partner-certification-checker/.github/workflows/certification.yml <PATH>/<TO>/<COLLECTION>.github/workflows/certification.yml
   ```

1. Commit and push the workflow:

   ```bash
   cd <PATH>/<TO>/<COLLECTION>
   git add .github/workflows/certification.yml
   git commit -m "Add certification workflow"
   git push
   ```

1. Open the `Actions` tab in your collection repository and verify that the workflow is enabled.

## Add Ansible Lint configuration

Add an [.ansible-lint](https://raw.githubusercontent.com/ansible-collections/partner-certification-requirements/refs/heads/main/docs/.ansible-lint) file to the root of your collection repository.
This prevents unrelated files from causing Ansible Lint failures.

## Keep the workflow updated

Optionally, add a [.github/dependabot.yml](https://github.com/ansible-collections/partner-certification-checker/blob/main/.github/dependabot.yml) configuration file so your repository receives pull requests when the certification workflow is updated.

Create `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

For more information, see the [Dependabot documentation](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/dependabot-quickstart-guide).

## Ignoring sanity failures

Some sanity test failures cannot be fixed and may need to be ignored.

To ignore an allowed sanity failure:

1. Review the list of [currently allowed ignores](https://docs.ansible.com/projects/lint/rules/sanity/).
1. Create a [sanity ignore file](https://docs.ansible.com/projects/ansible/devel/dev_guide/testing/sanity/ignores.html#ignore-file-location) for each affected ansible-core version, for example `tests/sanity/ignore-2.18.txt`.
1. Add the required ignore entries.
1. Commit and push the changes.

## Tested ansible-core branches and Python versions

| Component                                             | Version                                     |
| ----------------------------------------------------- | ------------------------------------------- |
| ansible-core sanity branches                          | `stable-2.16`, `stable-2.18`, `stable-2.20` |
| Python for `ansible-lint` and `galaxy-importer`       | `3.12`                                      |
| Default ansible-core for build, import, and lint jobs | `2.16.0`                                    |

The tested ansible-core branches are aligned with downstream Execution Environments.

If your collection declares a `requires_ansible` minimum in `meta/runtime.yml`
that is higher than the lowest sanity branch, the workflow automatically
detects it and skips unsupported versions from the sanity matrix.

To override auto-detection, use the `skip-sanity-versions` input:

```yaml
    with:
      skip-sanity-versions: 'stable-2.16'
```
