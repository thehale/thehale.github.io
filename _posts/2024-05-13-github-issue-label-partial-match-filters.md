---
layout: post
title: "Search GitHub Issues by label prefix, suffix, and contains"
category:
 - How-To Guides
 - GitHub
tags:
 - Project Management
---

On the new [GitHub Project Boards](https://docs.github.com/en/issues/planning-and-tracking-with-projects), you can use wildcard characters to search issue labels.

```
label:"prefix*"  // i.e. Label starts with 
label:"*suffix"  // i.e. Label ends with
label:"*middle*" // i.e. Label contains
```

> NOTE: As of the publication of this article, partial label filtering is only available in GitHub's new project boards, not a repository's Issues tab.
{: .prompt-info }

## Examples

### Searching GitHub Issues by Label Prefix

[Filtering my Binary Clock issues by `label:"h*"`](https://github.com/users/thehale/projects/3/views/1?filterQuery=label%3A%22h*%22&sortedBy%5Bdirection%5D=asc&sortedBy%5BcolumnId%5D=Labels) finds all the issues which have a label that starts with the letter `h`, in this case `hacktoberfest` and `help wanted`.

![A GitHub project board filtered to show Issues with a label matching a specific prefix](/assets/img/posts/github_issue_label_filters/search_github_issue_label_prefix.png)

### Searching GitHub Issues by Label Suffix

[Filtering my Binary Clock issues by `label:"*ment"`](https://github.com/users/thehale/projects/3/views/1?filterQuery=label%3A%22*ment%22&sortedBy%5Bdirection%5D=asc&sortedBy%5BcolumnId%5D=Labels) finds all the issues which have a label that ends with the letters `ment`, in this case `document` and `enhancement`.

![A GitHub project board filtered to show Issues with a label matching a specific suffix](/assets/img/posts/github_issue_label_filters/search_github_issue_label_suffix.png)

### Searching GitHub Issues by Label Contains

[Filtering my Binary Clock issues by `label:"*first*"`](https://github.com/users/thehale/projects/3/views/1?filterQuery=label%3A%22*first*%22&sortedBy%5Bdirection%5D=asc&sortedBy%5BcolumnId%5D=Labels) finds all the issues which have a label that contains the letters `first`, in this case `good first issue` and `first timers only`.

![A GitHub project board filtered to show Issues with a label containing a specific term](/assets/img/posts/github_issue_label_filters/search_github_issue_label_contains.png)