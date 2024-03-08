---
layout: post
title: How to create a custom Vue Component Library with robust testing via Storybook and Vitest
categories:
 - How-To Guides
 - Vue
tags:
 - Software Engineering
 - Test Driven Development
 - Continuous Integration
 - Vue
 - Vitest
 - Storybook
 - GitHub Actions
---

Many developers are familiar with using a component library (e.g. Vuetify, Quasar, PrimeVue, etc.), but there comes a time when it's useful to create your own.
- Multiple projects which should share custom components.
- A large project which is hard to test.

This comprehensive, step-by-step guide will take you from a new, empty folder all the way to a fully-functional component library with robust automated testing tools which follow software engineering best practices. The techniques described here are neither theoretical nor a mere "proof-of-concept" -- they have been used successfully in critical production applications.

Let's get started!

*Steps 1, 3, and 4 of this guide are heavily inspired by [Andreas Riedmüller](https://dev.to/receter)'s excellent [tutorial for creating a React Component Library](https://dev.to/receter/how-to-create-a-react-component-library-using-vites-library-mode-4lma)*
## 1. Scaffold an empty Vite project

Vite is a fabulous build tool that works especially well with Vue projects like a Vue Component Library.

Run `npm create vite@latest` to scaffold a new project. You'll be asked for a project name, then choose the Vue framework and the TypeScript variant to complete the setup.

```bash
$ npm create vite@latest

Need to install the following packages:
create-vite@5.2.1
Ok to proceed? (y) y
✔ Project name: … my-component-library
✔ Select a framework: › Vue
✔ Select a variant: › TypeScript

Scaffolding project in /my-component-library...

Done. Now run:

  cd my-component-library
  npm install
  npm run dev

```

Run the recommended commands to verify that installs and works correctly.
```shell
$ npm install

added 46 packages, and audited 47 packages in 9s

5 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
```

```bash
$ npm run dev

  VITE v5.1.4  ready in 329 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

Open your browser to the `Local` URL shown in your console to see the your new webpage powered by Vite!

To wrap up scaffolding, let's do a few tiny polishing steps...

### Install TypeScript types for NodeJS APIs
Currently, newly scaffolded Vite projects do not include the TypeScript type declarations for built-in NodeJS APIs. We'll need these later in the guide.

```bash
npm install --save-dev @types/node
```

### Create an `.nvmrc` file (optional)
Many developers (and CI tools) use [`nvm` (Node Version Manager)](https://github.com/nvm-sh/nvm) to easily configure the correct NodeJS version for each project. Creating an `.nvmrc` file clearly communicates your project's preferred version of `node`.

```bash
node --version > .nvmrc
```

### Make a `git` commit (optional)
At this point, I like to make a commit to snapshot my progress

```bash
git add .
git commit --message "chore: Scaffold new Vite project"
```

Committing immediately after scaffolding gives two major benefits: first, I can easily revert back to the scaffolded version if I mess up a later step; and second, a `git blame` can distinguish default configurations from custom configurations.

## 2. Create some sample library code

Let's add some placeholder code to our library! The goal at this point is have just enough library code to meaningfully evaluate the build tooling we will add in later steps. As such, I strongly recommend starting with only trivial library code so you can focus any debugging efforts on the build tooling.

For this tutorial, we'll use a simple `Greeting` component which calls a utility function to generate its greeting.

Create a custom utility function
```typescript
export function createGreeting(name?: string): string {
  return name === undefined ? "Hello!" : `Hello ${name}!`
}
```
{: file='lib/utils/createGreeting.ts' }

And create a custom component
{% raw %}
```vue
<script setup lang="ts">
import { createGreeting } from '../utils/createGreeting.ts'

defineProps<{ name: string }>()
</script>

<template>
  <h1>{{ createGreeting(name) }}</h1>
</template>
```
{: file='lib/components/Greeting.vue' }

{% endraw %}

> For now, ignore the TypeScript error on the import line. We'll fix that in a later step.
{: .prompt-info }

Finally, export your component from your library
```typescript
export * as Greeting from "./components/Greeting.vue"
```
{: file='lib/main.ts' }

At this point, if you run `npm run build` you'll notice that the generated `dist` directory contains none of the library code you just wrote. We'll fix the build in the next step.

<!-- In TDD terms, the "test" we just wrote for our build has failed successfully! -->

## 3. Convert Vite to library mode

A newly scaffolded Vite project always starts in *project* mode (i.e. building a complete web application), but, with a little more configuration, Vite also supports building JavaScript libraries.

<details markdown="1">
  <summary> <b>How does Vite's <i>project</i> mode work?</b> </summary>

Understanding the "magic" behind Vite's project mode isn't required for building a component library. But that knowledge does make it easier to understand the changes made to support library mode in Vite.

When you run `npm run dev`, here's what happens behind the scenes:
  1. `npm` parses your `package.json`, looks in the `scripts` section to find the configured `dev` command.
  2. `npm` runs the `dev` command (in this case `vite`) in the context of your currently installed `node_modules`.
  3. Vite loads its config file `vite.config.ts` and [starts an http server rooted at `index.html`](https://vitejs.dev/guide/#index-html-and-project-root), the default entrypoint for the new Vite project.
    - Notice the `vue` plugin which enables Vite to transpile `.vue` files to plain JS. 

Opening a web browser loads the `index.html` like a normal webpage, opening your web application.
  - The `index.html` defines an empty `<div id="app"></div>` (where the web application will mount). 
  - The `<script type="module" src="/src/main.ts"></script>`  loads the `src/main.ts` script (dynamically transpiled to JS by Vite) which creates the Vue app and mounts it at the previously defined `div`.

</details>

You'll notice that if you run `npm run build`, Vite will create a `dist` directory containing [`index.html` (the default entrypoint)](https://vitejs.dev/guide/#index-html-and-project-root) and the optimized code from your `src` directory. The key difference for *library* mode is telling Vite to build a different entrypoint to your code.

### Create a library entrypoint
In Step 2, we created a separate `lib` folder for our library code. We left the `index.html` file and `src` directory alone since they are a helpful playground to use while building components. 

Now we need to add the library entrypoint to `vite.config.ts`

```diff
import { defineConfig } from 'vite'
+ import { resolve } from 'path'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
+  build: {
+    copyPublicDir: false,
+    lib: {
+      entry: resolve(__dirname, 'lib/main.ts'),
+      formats: ['es']
+    }
+  }
})
```
{: file='vite.config.ts' }

> Setting `build.copyPublicDir` to `false` [excludes files in the `public` folder from the build](https://vitejs.dev/config/build-options.html#build-copypublicdir). For libraries, that's typically the preferred option since [`public` is intended to hold static assets for a webpage](https://vitejs.dev/guide/assets.html#the-public-directory).
{: .prompt-info }

> The [default value for `build.lib.formats` is `['es', 'umd']`](https://vitejs.dev/config/build-options.html#build-lib) . The `'umd'` format is mostly used for [standalone JS files distributed via a CDN](https://stackoverflow.com/a/77284527/14765128), so it isn't necessary for a component library. Omitting `'umd'` also has the benefit of allowing us to [omit the `build.lib.name` key](https://vitejs.dev/config/build-options.html#build-lib).
{: .prompt-info }

Now, running `npm run build` will generate a bundle in the `dist` folder containing your `lib`rary code instead of the `src` code!

### TypeScript Support in the IDE

Right now, TypeScript doesn't work in our `lib`rary code because the default configuration only looks at the `src` code. Let's fix that!

Copy Vite's types to your library
```bash
cp src/vite-env.d.ts lib/vite-env.d.ts
```

Enable TypeScript in your IDE for the `lib` directory
```diff
-   "include": ["src/**/*.ts", "src/**/*.tsx", "src/**/*.vue"],
+   "include": ["src", "lib"],
```
{: file='tsconfig.json' }

TypeScript should now be working in your IDE!

### Add TypeScript declarations to the built library

We also want to include TypeScript type declarations in the built library so that library users also benefit from the IDE autocompletion and quality checks. However, we want to omit type declarations for `src` files (our dev playground) since the `src` code won't be there either.

Start by creating a separate TypeScript config for building the library
```json
{
  "extends": "./tsconfig.json",
  "include": ["lib"]
}
```
{: file='tsconfig-build.json' }

And update your `package.json`'s `build` script to use the new TypeScript config. Now your build will only run type checks for code in your `lib` directory.
```diff
  "scripts": {
    …
-   "build": "vue-tsc && vite build",
+   "build": "vue-tsc --p ./tsconfig-build.json && vite build",
```
{: file='package.json' }

To distribute TypeScript type declarations with your library, install the Vite plugin called [`vite-plugin-dts`](https://github.com/qmhc/vite-plugin-dts) and point it to the `tsconfig-build.json` you just created.

```bash
npm add --save-dev vite-plugin-dts
```

```diff
+import dts from 'vite-plugin-dts'
…
  plugins: [
    vue(),
+   dts({ tsconfigPath: "tsconfig-build.json" }),
  ],
…
```
{: file='vite.config.ts' }

Now, `npm run build` should include several `.d.ts` files in your `dist` folder containing the TypeScript declarations for your library code!

## 4. Optimize the build

At this point, the built library bundle is nearly **50kb**, a huge amount of code for such a simple component library. The reason for the excessive size is that our build is packaging in a copy of Vue. Since our component library will be used within projects which already have Vue installed, this additional bundling is entirely unnecessary.

### Remove Vue from the bundle

Let's update our Vite config to exclude Vue from the built library bundle
```diff
  build: {
    …
+   rollupOptions: {
+     external: ['vue'],
+   }
  }
```
{: file='vite.config.ts' }

We'll also want to mark Vue as a [peer dependency](https://docs.npmjs.com/cli/v10/configuring-npm/package-json#peerdependencies) so that our library users are reminded that they need to install Vue themselves.

```diff
-   "dependencies": {
+   "peerDependencies": {
    "vue": "^3.4.19"
  },
```
{: file='package.json' }

You'll also want to add Vue as a development dependency so it continues to be installed while you develop the library.

```
npm install --save-dev vue
```

Now `npm run build` produces a much more reasonably sized bundle of only **~0.5kb**, a 100x size reduction!

<!-- TODO, add instructions about tree shaking, particularly for CSS. Start here: https://dev.to/receter/how-to-create-a-react-component-library-using-vites-library-mode-4lma#4-add-some-styles -->

<!-- TODO add instructions for publishing the package. Start here: https://dev.to/receter/how-to-create-a-react-component-library-using-vites-library-mode-4lma#4-a-few-last-steps-before-you-can-publish-the-package -->

## 5. Add testing tools to verify software quality

### Add Storybook.js for Component Driven Development

As we add more components to our library, it is helpful to have a dedicated tool to preview and test our components. The most powerful of these tools is [Storybook.js](https://storybook.js.org/).

#### Install Storybook
You can install Storybook using their [installation guide for Vue projects](https://storybook.js.org/docs/get-started/install), but I'll repeat the key steps here for completeness.

> NOTE: At the time of writing, there is a [shortcoming with the current Storybook install script](https://github.com/storybookjs/storybook/issues/22431#issuecomment-1630086092). You may have to force `npm` to resolve the package `jackspeak` (one of Storybook's transitive dependencies) to a specific version.
>
> ```diff
>    "dependencies": { … d}
>+   "resolutions": {
>+      "jackspeak": "2.1.1"
>+   }
> ```
{: file='package.json' }
{: .prompt-info }

Install Storybook.js
```
npx storybook@latest init
```

Storybook should automatically configure itself and launch in your browser at https://localhost:6006. Explore the tool to get a feel for what it does and how it works.

#### Add a Story for a library component

Stories are written in files named `*.stories.ts` and, by convention, are placed next to the component they test.

Create a Story file for the `Greeting.vue` component we created at the beginning of the tutorial.
```typescript
import type { Meta, StoryObj } from '@storybook/vue3';

import Greeting from './Greeting.vue';

// CONFIGURATION
const meta = {
  title: 'components/Greeting',
  component: Greeting,
  tags: ['autodocs'],
} satisfies Meta<typeof Greeting>;

export default meta;
type Story = StoryObj<typeof meta>;

// STORIES
export const Default: Story = {
  args: {},
};

export const HelloWorld: Story = {
  args: {
    name: 'World',
  },
};
```
{: file='lib/components/Greeting.stories.ts' }

To show this story within Storybook in your browser, you'll have to tell Storybook to look for stories in the `lib` folder. For this tutorial, we won't be writing stories for anything in the `src` folder so we'll have Storybook ignore `src` entirely.

```diff
const config: StorybookConfig = {
-   stories: ["../src/**/*.mdx", "../src/**/*.stories.@(js|jsx|mjs|ts|tsx)"],
+   stories: ["../lib/**/*.mdx", "../lib/**/*.stories.@(js|jsx|mjs|ts|tsx)"],
  …
```
{: file='.storybook/main.ts' }

Restart Storybook for this config change to take effect.

```
npm run storybook
```

Your `Greeting` story should now available in your Storybook!

#### Add testing addons to Storybook

Storybook supports a rich ecosystem of addons for testing your components.

##### Install the Accessibility Addon

I like starting with the [Accessibility addon](https://storybook.js.org/addons/@storybook/addon-a11y) since it provides a solid foundation for later testing plugins (particularly interaction testing).

```bash
npm install --save-dev @storybook/addon-a11y
```

```diff
const config: StorybookConfig = {
  …
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "@storybook/addon-interactions",
+     "@storybook/addon-a11y",
  ],
```
{: file='.storybook/main.ts' }

Now your stories will have an **Accessibility** tab which automatically checks your component for Accessibility issues and recommends fixes.
##### Install the Storybook Test Runner

The [Storybook Test Runner](https://storybook.js.org/docs/writing-tests/test-runner) turns all of your stories into automated unit, smoke, and interaction tests, no extra effort required!

Install the test runner
```bash
npm install --save-dev @storybook/test-runner @storybook/testing-library
```

Install [`playwright`](https://playwright.dev/) (used by the test runner for smoke and interaction tests)
```
npx playwright install
```

Start Storybook in one terminal
```bash
npm run storybook
```

And run the tests against that Storybook instance in another terminal
```bash
npm run test-storybook
```

##### Add Storybook Test Coverage

Measuring your test coverage -- which lines of production code get executed while running the test suite -- can help you find gaps in your testing.

To have Storybook collect test coverage during its test runs, install the [Storybook Test Coverage Addon](https://storybook.js.org/docs/writing-tests/test-coverage)
```bash
npm install --save-dev @storybook/addon-coverage
```

You'll also need to include the coverage addon in your Storybook configuration
```diff
const config: StorybookConfig = {
  …
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "@storybook/addon-interactions",
    "@storybook/addon-a11y",
+     "@storybook/addon-coverage",
  ],
```
{: file='.storybook/main.ts' }

To measure test coverage in your `.vue` files, you'll also need to a `.nycrc.json` config file instructing the test runner to instrument `.vue` files.
```
touch .nycrc.json
```

```json
{ "extension": [".vue",".js","jsx",".ts","tsx"] }
```
{: file='.nycrc.json' }

Restart your Storybook instance if necessary, then rerun the test suite, this time with the `--coverage` flag.
```bash
npm run test-storybook -- --coverage
```

The coverage metrics will be saved to `coverage/storybook/coverage-storybook.json`. You can generate a coverage report using [`nyc`](https://github.com/istanbuljs/nyc).
```bash
$ npx nyc report --reporter=text --temp-dir coverage/storybook
--------------------|---------|----------|---------|---------|-------------------
File                | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s 
--------------------|---------|----------|---------|---------|-------------------
All files           |     100 |      100 |     100 |     100 |                   
 components         |     100 |      100 |     100 |     100 |                   
  Greeting.vue      |     100 |      100 |     100 |     100 |                   
 utils              |     100 |      100 |     100 |     100 |                   
  createGreeting.ts |     100 |      100 |     100 |     100 |                   
--------------------|---------|----------|---------|---------|-------------------

$ npx nyc report --reporter=text-summary --temp-dir coverage/storybook
=============================== Coverage summary ===============================
Statements   : 100% ( 4/4 )
Branches     : 100% ( 2/2 )
Functions    : 100% ( 1/1 )
Lines        : 100% ( 4/4 )
================================================================================
```

### Add Vitest for unit testing for utility functions

Your library may include utility functions in addition to UI components. To test these utility functions directly, you can add a unit testing framework like [Vitest](https://vitest.dev/).

#### Install `vitest`

```bash
npm install --save-dev vitest 
```

Add a `test` script to your `package.json`
```diff
scripts: {
…
+     "test:unit": "vitest"
}
```
{: file='package.json' }

Add a test file for the `createGreeting.ts` utility function we created at the start of the tutorial
```typescript
import { describe, expect, it } from "vitest"
import { createGreeting } from "../createGreeting"

describe("createGreeting", () => {
  it("creates a generic greeting when no name is provided", () => {
    expect(createGreeting()).toBe("Hello!")
  })
  it("creates a specific greeting when a name is provided", () => {
    expect(createGreeting("World")).toBe("Hello World!")
  })
})
```
{: file='lib/utils/__tests__/createGreeting.test.ts' }

Now you can run the unit tests for your utility code
```bash
npm run test:unit
```

#### Setup Test Coverage Measurement for Vitest

Create a `vitest.config.ts` with the following contents
```typescript
import { defineConfig } from 'vitest/config'
import vue from "@vitejs/plugin-vue"
import tsconfigPaths from "vite-tsconfig-paths"

export default defineConfig({
  test: {
    coverage: {
      all: true,  // Include files with 0% coverage in the report.
      provider: 'istanbul', // or 'v8'
      include: ['lib/**/*'],
      // Omit test code from the report (both Storybook and Vitest)
      exclude: ['lib/**/*.stories.{ts,tsx}', 'lib/**/*.test.{ts,tsx}'],
      reporter: ["text", "text-summary", "json", "json-summary"],
      reportsDirectory: "coverage/unit",
    },
  },
  plugins: [
    vue(),
    tsconfigPaths(),
  ],
})
```
{: file='vitest.config.ts' }

Install [`vite-tsconfig-paths`](https://www.npmjs.com/package/vite-tsconfig-paths) so Vitest can better support TypeScript resolutions.
```bash
npm install --save-dev vite-tsconfig-paths
```

Run the unit tests with the `--coverage` flag to see the coverage results. If you are prompted to install `@vitest/coverage-istanbul`, accept it, then re-run the test command.
```bash
npm run test:unit -- --coverage
```

### Combine Test Coverage Results from Storybook and Vitest

Since we're running two different testing tools, we get two separate, and thus incomplete, test coverage reports. We want to merge those reports into one complete test coverage report.

Currently, the data backing the Storybook test coverage report is saved in the `coverage/storybook/` folder while Vitest's test coverage data is in `coverage/unit/`

The underlying CLI tool for test coverage, [`nyc`](https://github.com/istanbuljs/nyc), has a built-in `merge` command which will merge all test coverage reports found in a specified directory. As a result, we can use the following script to generate our combined report

```bash
mkdir --parents coverage/merged
cp coverage/storybook/coverage-storybook.json coverage/merged/coverage-storybook.json
cp coverage/unit/coverage-final.json coverage/merged/coverage-unit.json
npx nyc merge coverage/merged coverage/coverage-final.json
```

Now you can view a complete, combined test coverage report:

```bash
$ npx nyc report --reporter=text --temp-dir coverage/
--------------------|---------|----------|---------|---------|-------------------
File                | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s 
--------------------|---------|----------|---------|---------|-------------------
All files           |     100 |      100 |     100 |     100 |                   
 components         |     100 |      100 |     100 |     100 |                   
  Greeting.vue      |     100 |      100 |     100 |     100 |                   
 utils              |     100 |      100 |     100 |     100 |                   
  createGreeting.ts |     100 |      100 |     100 |     100 |                   
--------------------|---------|----------|---------|---------|-------------------

$ npx nyc report --reporter=text-summary --temp-dir coverage/

=============================== Coverage summary ===============================
Statements   : 100% ( 4/4 )
Branches     : 100% ( 2/2 )
Functions    : 100% ( 1/1 )
Lines        : 100% ( 4/4 )
================================================================================
```

### Running Tests in a Continuous Integration System

Running your tests regularly in an automated environment helps you find and fix errors in your code faster. 

To run our tests in a continuous integration system (e.g. GitHub Actions), we need to write scripts that:
 - Run the tests headlessly (i.e. with zero user interaction).
 - Specify all dependencies required for the production code and its tests.

#### Run headless tests locally
Let's start by updating the scripts in `package.json` to clearly specify whether they run interactively (for local development) or headlessly (for use in `ci`).

```diff
"scripts": {
+    "cdd": "storybook dev --port 6006",
+    "test:unit": "vitest",
+    "test:unit:ci": "vitest --coverage --run",
+    "test:cdd": "test-storybook --watch --browsers chromium,firefox,webkit",
+    "test:cdd:ci": "test-storybook --coverage --browsers chromium,firefox,webkit",
+    "build": "vue-tsc -p ./tsconfig-build.json && vite build --watch",
+    "build:ci": "vue-tsc -p ./tsconfig-build.json && vite build",
+    "build:cdd": "storybook build",
}
```
{: file='package.json' }

> I use the name `cdd` (shorthand for Component Driven Development) to refer to my Storybook scripts because I prefer to focus on engineering principles over the tool that enables them.
{: .prompt-info }

From there, we can write the scripts to use in CI. I like to use a `Makefile` for this purpose

```bash
.PHONY: build
build:
	npm run build	

.PHONY: build-ci
build-ci:
	npm run build:ci


.PHONY: test
test:
	npx --yes concurrently --kill-others --success first --names "CDD,UNIT" -c "magenta,blue" \
		"npx --yes npm run test:cdd" \
		"npx --yes npm run test:unit"

.PHONY: test-ci
test-ci:
	rm -rf coverage
# Run the unit tests
	npm run test:unit:ci
# Run the Storybook tests
# - Credits: https://storybook.js.org/docs/writing-tests/test-runner#run-against-non-deployed-storybooks
	npx --yes concurrently --kill-others --success first --names "SB,CDD" -c "magenta,blue" \
		"npx --yes npm run cdd -- --port 6006 --ci --quiet" \
		"npx --yes wait-on tcp:6006 && npm run test:cdd:ci"
# Merge the coverage reports
	mkdir --parents coverage/merged
	cp coverage/storybook/coverage-storybook.json coverage/merged/coverage-storybook.json
	cp coverage/unit/coverage-final.json coverage/merged/coverage-unit.json
	npx nyc merge coverage/merged coverage/coverage-final.json
# Generate the coverage report
	for reporter in text text-summary lcov json-summary ; do \
		npx nyc report --reporter=$$reporter -t coverage/ --report-dir coverage/ ; \
	done
```
{: file='Makefile' }

With this `Makefile` you now have four useful commands for local development and CI verification
```bash
$ make build  # Run the production build in *watch* mode (i.e. rebuild on file saves)
$ make build-ci  # One-off, headless production build
$ make test  # Run both unit/cdd tests in *watch* mode (i.e. rerun on file save)
$ make test-ci  # One-off, headless test run
```

The magic part of these scripts is the use of the [`concurrently` package](https://www.npmjs.com/package/concurrently) to boot a Storybook server headlessly for the Storybook testing library to run against (thanks [Storybook docs](https://storybook.js.org/docs/writing-tests/test-runner#run-against-non-deployed-storybooks)!).
#### Run tests in GitHub Actions

If you host your component library repository in GitHub, you can create a GitHub Actions workflow file which will run the tests for you on every commit you push up.

```yaml
name: "CI(branch): Test, Release"

on:
  push:
    branches: [master, qa, dev, "[0-9]+.[0-9]+.[0-9]+", "[0-9]+.[0-9]+.[0-9]+-[a-zA-Z]+"]
    tags:
      - "[0-9]+.[0-9]+.[0-9]+"
  pull_request:
    branches: [master, qa, dev, "[0-9]+.[0-9]+.[0-9]+"]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version-file: '.nvmrc'
      
      - name: Install dependencies
        run: yarn install --frozen-lockfile
    
      - name: Install Playwright
        run: npx playwright install --with-deps
      
      - name: Build the package
        run: make build-ci

      - name: Run the Unit Tests
        run: make test-ci

      - name: Publish internal package releases
        # Run only on `push` events to tags/branches other than `master`
        if: github.ref_name != 'master' && (github.event_name == 'push' || github.event_name == 'workflow_dispatch')
        run: |
          echo "NO-OP: Replace with your code for publishing an internal version"

      - name: Push the production package releases
        # Only run this job for the `master` branch
        if: github.ref_name == 'master'
        run: |
          echo "NO-OP: Replace with your code for publishing a production version"
```
{: file='.github/workflows/ci-test-release.yml' }

## 6. Other Notes

### Hot-reloading the Vue component library within a larger project

My original motivation for creating a component library was to improve the testability of a large Vue application, not to share components between multiple applications. In that situation, my team wanted to preserve the ability to edit the component library and see it hot-reload within the large Vue application.

Attempting to hot-reload code changes to an npm dependency is extraordinarily difficult. 
- The dependency code is usually an optimized, compiled form of the original source code, so a hot-reload requires rebuilding the original source code. [Vite's  `build --watch` mode](https://vitejs.dev/guide/build#rebuild-on-files-changes) impressively managed to effectively tree-shake the build process so that it only rebuilt the smallest number of JS chunks possible; however, even that optimized build still took 3-4 seconds for tiny code changes (e.g. changing a static text label).
- npm dependencies are loaded from `node_modules`, which is only updated by `npm install`. Any hot-reload process would also need to automatically re-install the component library.

For these reasons, we decided to import our component library code directly (i.e. *not* as an npm dependency) and let our larger Vue project's compiler handle the entire build process for both the library code and the main application code.

Include your component library within the larger project as a submodule
```bash
git submodule init
git submodule add COMPONENT_LIBRARY_URL lib/COMPONENT_LIBRARY
```

Within the larger project, configure resolution aliases for your component library's code.

Add a TypeScript alias
```diff
{
  "compilerOptions": {
    "baseUrl": ".",
        "paths": {
+            "my-component-lib/*": ["lib/my-component-lib/lib/*"]
        }
  }

}
```
{: file='tsconfig.json' }

Add a Vite alias
```diff
import { defineConfig } from "vite";
+  import path from "path"

export default defineConfig({
  resolve: {
    alias: {
+      "my-component-lib": path.join(__dirname, "./lib/my-component-lib/lib"),
    }
  }
})
```
{: file='vite.config.ts' }

Now your larger Vue project can directly import code from your component library and have the library code hot-reload/build just like the code of the larger application.
```vue
import Greeting from "my-component-lib/components/Greeting.vue"
```
{: file='your-vue-app/SomePage.vue' }

## Conclusion

Testing UI code is can be really hard, especially when attempting to improve the testability of a large, established project. Creating a custom component library can (1) provide a clean environment for developing and testing individual components and (2) open the door to sharing code with between projects for further productivity gains.

I hope this tutorial has helped you create a robustly testable component library which can provide a solid foundation for your development work for years to come.

Please share your experience, insights, and/or critiques in the comments below!
