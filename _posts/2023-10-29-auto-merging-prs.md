---
layout: post
title: "How to automatically merge trusted Pull Requests on GitHub"
tags:
 - Open Source
 - Security
 - Software Engineering
 - Project Management
---

<figure>
    <img style="max-height: 50vh" src="/assets/img/auto_merging_prs/merged_prs.png" alt="A screenshot showing a large number of automatically merged pull requests.">
    <figcaption>
    Unblock your maintainers, reduce friction for regular contributors, and automatically apply updates/security fixes from GitHub's Dependabot -- without compromising your standards for security or quality!
    </figcaption>
</figure>


You can increase development velocity by automatically merging pull requests from individuals or bots you trust. Here's how

## Enable **Allow auto-merge** pull requests in repository settings

The default settings for GitHub repositories block auto-merging any Pull Requests. This is a beneficial security measure which makes it harder for untrusted actors to integrate malicious code into your repository. 

To allow trusted actors (e.g. maintainers and priviledged GitHub Actions workflows) to enable auto-merge for individual pull requests, you need to globally enable the feature in your repository settings.

1. Go to `https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/settings`
2. Choose the **General** settings group
3. Scroll down to the **Pull Requests** section
4. Enable **Allow auto-merge**

![A screenshot of the GitHub repository settings page, showing how to allow auto-merging pull requests](/assets/img/auto_merging_prs/allow_auto_merge.png)

Remember, this setting is a repository-level *feature toggle*. Individual pull requests still will not be auto-merged unless explicitly flagged otherwise (which we handle [later in this guide](#automatically-enable-auto-merge-for-individual-pull-requests)).

### GitHub Organizations: Allow GitHub Actions to create and approve pull requests

Repositories under the scope of a GitHub Organization also need organization-level permissions to enable auto-approval/merging of pull requests.

1. Go to `https://github.com/organizations/YOUR_ORGANIZATION/settings/actions`
2. Scroll down to the **Workflow permissions** section
3. Enable **Allow GitHub Actions to create and approve pull requests**

    ![A screenshot of the GitHub organization Actions settings page, showing how to allow automated creation and approval of pull requests](/assets/img/auto_merging_prs/org_actions_prs_permissions.png)

After enabling the setting at the organization level, double check that it is also enabled on the repository level.

1. Go to `https://github.com/YOUR_ORGANIZATION/YOUR_REPOSITORY/settings/actions`
2. Scroll down to the **Workflow permissions** section
3. Enable **Allow GitHub Actions to create and approve pull requests**

## Configure branch protection rules 

Without proper protections, automatically merging code can result in broken projects and/or security disasters. You can guard against these scenarios with [branch protection rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule).

> **Note**
>
> Branch protection rules are free for public GitHub repositories. While you can create a branch protection rule for private GitHub repositories, it will only be enforced if the user/organization owning the repository subscribes to a paid plan (e.g. Pro, Team, Enterprise).

Branch protection rule are configured in your repository settings

1. Go to `https://github.com/USERNAME/REPOSITORY/settings`
2. Choose the **Branches** settings group

    If branch protection rules have never been configured for this repository, you should see the option to **Add branch protection rule**

    ![A screenshot of the branch protection rules settings page in GitHub when no rules have been configured.](/assets/img/auto_merging_prs/branch_protection_rules_none.png)

    If branch protection rules already exist, you will instead see the options to **Edit** a rule, or **Add rule**

    ![A screenshot of the branch protection rules settings page in GitHub when one or more rules have been configured.](/assets/img/auto_merging_prs/branch_protection_rules_some.png)

3. Under **Branch name pattern**, enter the name of the branch to protect (e.g. `main` or `master`)
4. Under **Protect matching branches** enable all the rules you want to enforce before any merge can happen, automatic or not. I recommend the following:
    - Enable **Require a pull request before merging** and its subrule **Require approvals** with the number of required approvals set to `1`
    - Enable **Require status checks to pass before merging** and its subrule **Require branches to be up to date before merging**
       > **Warning**
       >
       > Use the search box to find and select the names of the jobs to enforce as required status checks. Otherwise, this rule will do nothing.

    ![A screenshot of creating a new branch protection rule in GitHub.](/assets/img/auto_merging_prs/branch_protection_rule_settings.png)
5. Scroll down to the bottom and press **Save changes**



### RECOMMENDED: Improve the maintainability of required status checks with the `alls-green` GitHub Action

The rule **Require status checks to pass before merging** suffers from two major flaws:
 - Required status checks that are "skipped" count as "passing"
 - The list of required status checks must be maintained manually -- especially difficult with [build matrices](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs)

These concerns can be largely mitigated by adding the [`alls-green` GitHub Action](https://github.com/marketplace/actions/alls-green) to the end of your CI's workflow file with your required jobs listed under the `needs` key of the `alls-green` job.

For example,
{% raw %}
```yaml
name: My Project's CI Checks
on:
  pull_request:
    branches: [main]
jobs:
  lint:
    # ... specifications for the `lint` job
  test:
    # ... specifications for the `test` job

  # Reduce the maintenance burden for required status checks.
  # https://github.com/marketplace/actions/alls-green#why
  alls-green:  
    # ^--- TODO: After the first run, set this job name as a 
    # required status check in your branch protection rules.
    if: always()
    needs:  # <--- TODO: List all required jobs here.
     - lint
     - test
    runs-on: ubuntu-latest
    steps:
      - name: Ensure all other jobs pass successfully.
        uses: re-actors/alls-green@release/v1
        with:
          jobs: ${{ toJSON(needs) }}
```
{% endraw %}

After your updated CI workflow is run for the first time, you can reopen the branch protection rules and search for `alls-green` to set it as a required status check.

With the `alls-green` job configured, you no longer have to manually sync your branch protection rules with your build matrix. Additionally, changes to required job names only have to be kept in sync within the same workflow file, instead of with the GitHub branch protection UI.

If you use status checks from third-party providers or multiple workflow files, you will still need to maintain those in your list of required status checks in the repository's branch protection rules.

## Automatically enable auto-merge for pull requests from trusted authors

Once the appropriate permissions and safeguards are in place, auto-merging pull requests from trusted authors can be enabled automatically with another GitHub Actions workflow. 

For example, the following workflow will automatically merge pull requests from [GitHub's Dependabot](https://docs.github.com/en/code-security/dependabot):

{% raw %}
```yaml
# .github/workflows/automerge-dependabot-prs.yml
name: Auto-merge Dependabot PRs

on: pull_request

permissions:
  contents: write
  pull-requests: write

jobs:
  dependabot:
    runs-on: ubuntu-latest
    if: ${{ github.actor == 'dependabot[bot]' }}
    steps:
      - name: Approve a PR
        run: gh pr review --approve "$PR_URL"
        env:
          PR_URL: ${{github.event.pull_request.html_url}}
          GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
      - name: Enable auto-merge for Dependabot PRs
        run: gh pr merge --auto --rebase "$PR_URL"
        env:
          PR_URL: ${{github.event.pull_request.html_url}}
          GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```
{% endraw %}
> **Note**
>
> The above workflow was adapted from the [GitHub Dependabot documentation](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/automating-dependabot-with-github-actions#enable-auto-merge-on-a-pull-request).

### How the auto-merging workflow works

#### Limiting when the workflow runs
The above workflow is triggered `on` the opening of any [`pull_request`](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#pull_request) into the repository.

The workflow's sole job, `dependabot`, only runs `if` the user who opened the request (i.e. `github.actor`) is `'dependabot[bot]'`. You can [customize this guard with any valid GitHub Action expression](https://docs.github.com/en/actions/learn-github-actions/expressions). For example, to auto-merge pull requests from one of multiple trusted authors (e.g. `dependabot[bot]`  and a trusted maintainer with the username `octocat`) you can [provide a list](https://stackoverflow.com/a/70142531/14765128) of trusted author names:

{% raw %}
```
if: ${{ contains(fromJson('["dependabot[bot]", "octocat"]'), github.actor) }}
```
{% endraw %}

#### Automatically approving and merging the pull request
The job's two `steps` will use the [GitHub CLI's `pr` command](https://cli.github.com/manual/gh_pr) to interact with the pull request.

The first step adds an automatic approval to satisfy the **Require approvals** branch protection rule we [configured earlier](#configure-branch-protection-rules). This approval will appear as coming from `github-actions[bot]`.

The second step directs GitHub to `--auto`matically merge the pull request once all required status checks pass, per the **Require status checks to pass before merging** branch protection rule [configured earlier](#configure-branch-protection-rules). As written, the merge will use the `--rebase` strategy, but you can change it to [`--merge` or `--squash`](https://cli.github.com/manual/gh_pr_merge) at your preference.

#### Security notes
These steps authenticate with the GitHub CLI using the [default `GITHUB_TOKEN`](https://docs.github.com/en/actions/security-guides/automatic-token-authentication) which is granted additional priviledges for `write`-ing updates to a pull request by the [`permissions`](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#permissions-for-the-github_token) block at the top of the workflow.

## Examples

I actively use this auto-merging strategy for Dependabot PRs in many of my open source projects. While the repository settings are not publicly viewable, the GitHub Actions workflow files are.

 - **Multicounter:** [A Python package for easily counting multiple things at once.](https://github.com/thehale/multicounter)
 - **Signatures**: [Run-time type checking for function signatures in Python.](https://github.com/thehale/signatures)

If you successfully used this guide in your project, please let me know! I am happy to list your project here too.