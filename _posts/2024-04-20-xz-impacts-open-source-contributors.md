---
layout: post
title: "Potential impacts of the `xz` attack on new open-source contributors"
excerpt: |
  In the wake of the trust-breaking `xz` attack, I want to encourage hopeful first-time open-source software contributors to
  (1) demonstrate increased empathy for maintainers and (2) exemplify patience and kindness throughout the contribution process.
tags:
 - Open Source
 - Software Engineering
 - Security
image:
  path: /assets/img/posts/xz-contribution-impact/maintainer_trust_dilemma_4x3.jpg
---

New developers often ask me how they can start contributing to open-source software. My typical recommendations are succinct: start small, contribute to what you use, follow the project's CONTRIBUTING guidelines. But, given this month's discovery of a [severe security vulnerability](https://www.cve.org/CVERecord?id=CVE-2024-3094) introduced via a [social engineering attack](https://research.swtch.com/xz-timeline), I want to give additional guidance. Specifically, I want to encourage hopeful first-time open-source software contributors to (1) demonstrate increased empathy for maintainers and (2) exemplify patience and kindness throughout the contribution process.

## What happened in the `xz` attack?

 This post comes in the wake of an attack on [`xz`](https://github.com/tukaani-project/xz), an open-source project that provides "lossless data compression", a service that makes it cheaper for computers to share data with each other. 
 
 > If you're unfamiliar with compression, imagine you have a friend in another country who needs a heavy math textbook that you own. Instead of paying lots of postage to mail the giant book, you instead take a few pages of notes and send them via a single, cheap envelope. When your friend receives your detailed notes, she's able to rewrite the entire textbook word for word.
{: .prompt-info }
 
 `xz` is widely used in servers run by individuals, companies, and governments around the globe, but for years was largely unknown and maintained by one person. A few years ago, a new developer started contributing bug fixes and, at the urging of other purported users of `xz`, was eventually trusted as a co-maintainer. But, earlier this month it was discovered that this new maintainer had been sneaking in security flaws that would have allowed someone to [secretly take over computers](https://gist.github.com/thesamesam/223949d5a074ebc3dce9ee78baad9e27) using `xz` in communications. Upon discovery, the malicious maintainer and his supporters quickly vanished.


## How has the `xz` attack impacted maintainers?

While the security impacts of the `xz` attack have been limited thanks to its quick discovery, this gross abuse of one maintainer's trust has caused some other maintainers to become more wary. 

For example, one maintainer of a reputable, open-source application used by many companies lamented, "[the `xz` attack] impacts my trust in all the software I use daily to organize my life and livelihood." Similarly, a lone developer currently maintaining a complex project he inherited from someone else shared, "I'm looking for more maintainers to 'my' project, but now I feel insecure about it." 

Maintainers are also receiving warnings from reputable groups like the [Open Source Security Foundation](https://openssf.org/blog/2024/04/15/open-source-security-openssf-and-openjs-foundations-issue-alert-for-social-engineering-takeovers-of-open-source-projects/) to beware of social engineering attacks beyond `xz`.

> These social engineering attacks are exploiting the sense of duty that maintainers have with their project and community in order to manipulate them. Pay attention to how interactions make you feel. Interactions that create self-doubt, feelings of inadequacy, of not doing enough for the project, etc. might be part of a social engineering attack.

These reactions -- increased fear of abuse, decreased trust towards newcomers -- are reasonable responses to a serious breach of trust. It is scary to see the malicious exploitation of a fellow maintainer since it prompts the question "Am I next?"

## How might the `xz` attack impact first-time contributors?

I'm already seeing some maintainers demonstrate increased caution towards new contributors. In one isolated case a maintainer considered rejecting innocent typo corrections from first-time contributors because he had a "gut feeling ... that these accounts are being setup and prepared for 'something' in the future". Another maintainer closed similar pull requests with no feedback, expecting that a real contributor would follow up on the closure.

One respected maintainer of ecosystem-wide tools shared the following insightful perspective on how the `xz` attack might affect the relationship between maintainers and prospective contributors

> I believe this event [-- the `xz` attack --] adds an extra layer of mistrust for new contributors, especially for solo maintainers who may not know them beforehand. Such an event doesn't facilitate building trust or finding new maintainers; instead, it may lead to increased isolation among maintainers.

Maintainers are adjusting to the evidence that they could be targeted by a malicious contributor. As a result, honest contributors may also experience additional scrutiny.

## What can hopeful first-time contributors do?

Keep sharing your contributions! The worst possible outcome of the `xz` attack would be a widespread loss of trust that breaks down the entire open-source ecosystem. Maintainers know that the vast majority of contributors are not malicious, and they welcome the interest in and support for their projects.

But, since trust has been broken, it is increasingly important for new and existing contributors to **contribute with empathy and kindness**.

When an issue is closed unceremoniously, or a pull request is rejected without an explanation, let your first reaction be "Thank you for your time. I really appreciate your work to maintain this project."

When you see an aggressive comment from another contributor, choose to de-escalate the situation (e.g. wait to respond until you are calm, focus on substance over personality, etc.). When appropriate, encourage the contributor to engage more constructively.

## Conclusion

Trust has always taken time to earn. Since the `xz` attack, trust may take longer to earn. Let's accept that possibility with kindness, empathy, and grace, and together we can build an open-source community even stronger than before.

---

## Additional tips that may help build trust

- On GitHub, [personalize your profile](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/personalizing-your-profile), including adding a [profile README](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme). This helps people see your broader interests and goals, increasing trust that you are a real person.
- Where available, engage constructively with the project's broader community (e.g. chat on Discord/Slack). Hearing from you in different spaces can increase confidence in your authenticity.
- Publish an open-source project of your own. This gives you valuable experience in the mechanics of open-source work and provides more evidence of your sincerity. You don't have to create anything fancy or novel. If you need inspiration, check out [`build-your-own-x`](https://github.com/codecrafters-io/build-your-own-x).
- Disclose any use of Generative AI in producing your contribution (e.g. ChatGPT). Maintainers are currently receiving too many "AI spam PRs" and may reject contributions they suspect of being secretly AI generated. Being forthcoming about your use of AI (which is usually welcome and encouraged) increases the credibility of your contributions. Disclosing usage of AI is also [required by the US Copyright Office](https://copyright.gov/ai/ai_policy_guidance.pdf).

---

*CREDITS:* 
 - *The anonymous quotes/stories from maintainers are from a private community governed by the [Chatham House Rule](https://www.chathamhouse.org/about-us/chatham-house-rule).*
 - *The cover image of guarding treasure from unknown gift givers is AI generated using Microsoft Copilot Designer powered by DALL-E 3.*
 - *Except where quoted, the text of the article is entirely original writing by Joseph Hale.*