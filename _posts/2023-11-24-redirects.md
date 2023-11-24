---
title: "Configuring Redirects"
author: thehale
categories: [Blogging, Tutorial]
tags: [migration]
redirect_from:
 - /my/old/url
 - /my/other/old/url
---
<!-- The rest of the blog post content -->

## Motivation

When switching to Chirpy from a different Jekyll theme, the URLs of your blog posts might change, breaking backlinks and erasing your SEO gains.

You'll want to configure redirects so existing bookmarks/links continue working, and so that search engines can find your new URLs and credit them with your SEO history.

## Configuration

Simply add the key `redirect_from` to the front matter of your posts.

```markdown
---
# ... other front matter keys
redirect_from:
  - /my/old/url
  - /my/other/old/url
---
<!-- The rest of the blog post content -->
```
{: file='2023-11-24-redirects.md' }

Now the urls [/my/old/url](/my/old/url) and [/my/other/old/url](/my/other/old/url) will forward traffic to the post's new URL with Chirpy. Try them! You'll land back on this article.

## How it works

Chirpy includes the plugin [`jekyll-redirect-from`](https://github.com/jekyll/jekyll-redirect-from) which creates a special HTML file at each path listed in the `redirect_from` key in your front matter. That HTML file tells browsers to redirect to the latest link, and it instructs search engines to forward SEO history to the new link.
