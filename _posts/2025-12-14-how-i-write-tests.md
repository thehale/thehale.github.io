---
layout: post
title: How I Write Tests
tags:
 - Testing
 - Test Driven Development
 - Unit Testing
 - Code Review
 - Teaching
---

I tend to like writing tests more than the average Joe. For me, there's something really satisfying about using a test to figure out how I want an API surface to feel, iterating on the failing test until the error message is exactly what I want to see in the test log if the feature breaks, then implementing the feature and seeing the test pass as expected, followed by refining both the implementation and test code to a state that I'd be happy to revisit/reread in 2 years.

I tend to use mocks sparingly. e.g. I consider the persistence layer of a service part of its private internal implementation that shouldn't be tested/mocked directly. That means full DB transactions and file system access. I will however stub out external network access and return hand crafted responses for third party APIs (great for testing handling of error cases like rate limits)

But I don't write tests first for everything, especially when I'm working with a brand new tool/language. There's a space for exploration to figure out what's possible before I pivot to testing to nail down/refine a durable approach.

The two videos below are probably favorites about software testing. Each provides nice mental frameworks that make testing feel more strategic/expressive.

[Sandi Metz: The Magic Tricks of Testing](https://www.youtube.com/watch?v=URSWYvyc42M)

<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/URSWYvyc42M?si=m1ZlGqeKeLAjBNOB" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

[Kevlin Henry: Structure and Interpretation of Test Cases](https://www.youtube.com/watch?v=MWsk1h8pv2Q)

<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/MWsk1h8pv2Q?si=S87hrVIqqQFfTDoo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>