# Releasing re-usable workflows

## Changelog

To track changes in this repository made between versions and to generate a changelog, we use [changelog fragments](https://docs.ansible.com/ansible/latest/community/development_process.html#creating-a-changelog-fragment).

### When updating tools versions in the reusable workflow

When updating versions of tools in the reusable workflow, ensure that the changelog, and any notifications to partners:
1. Include porting guides for related breaking changes
2. Make sure that the information in the [Tested ansible-core branches and Python versions](README.md#tested-ansible-core-branches-and-python-versions) is updated to reflect any changes

For example, when bumping the `ansible-core` version from `2.16` to `2.17`, create a corresponding changelog fragment. It should note that, because workflow version N runs the `ansible-test sanity` command from ansible-core 2.17, if a partner has a `tests/sanity/ignore-2.16.txt` file, they need to copy it to `tests/sanity/ignore-2.17.txt` to prevent errors.

## Immutable releases

This repository uses [GitHub Immutable Releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases) to protect supply chain integrity.
When a release is published, that release tag cannot be moved or deleted.
This also means that we do not use floating tags (v2, v3, etc.) that always point to the latest minor or patch release since v2.0.0. Tag v1 is kept for backwards compatibility reasons and is also immutable.

Enable **Immutable releases** in the repository settings under **Settings > Code security > Immutable releases**. You need to do this one time only.

## Release process

1. Based on the [Semantic Versioning](https://semver.org/) conventions and [changelog/fragments](changelog/fragments), determine a proper release version number.

   - When we change any versions of tools, their arguments or anything else that might result in failures on partners' side, we release a major version.
   - If this is the case, make sure there's a corresponding changelog entry containing a porting guide as explained in the [Changelog](#changelog) section.
2. Follow the [Releasing guidelines](https://docs.ansible.com/ansible/devel/community/collection_contributors/collection_release_without_branches.html) where applicable (for example, we don't publish this collection on Galaxy).
3. Create an annotated tag and push it.
   ```bash
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   git push origin vX.Y.Z
   ```
4. Create a **GitHub Release** from that tag. The release is immutable when published.
5. Update the version reference in the [calling workflow](.github/workflows/certification.yml) to `@vX.Y.Z` and open a PR.

## Post-release actions

- If there are any breaking changes in a particular release, notify partners to update the workflow version in their repository, including a description of changes and a link to a porting guide (i.e. the related changelog entry) as explained in the [Changelog](#changelog) section.
- Announce the release on the Ansible forum by creating a topic under the `News & Announcements` category with the `red-hat-partner` and `certification` tags. See the [first announcement](https://forum.ansible.com/t/release-announcement-partner-certification-checker-github-workflow-v2-0-0-has-been-released/45850) as an example.
