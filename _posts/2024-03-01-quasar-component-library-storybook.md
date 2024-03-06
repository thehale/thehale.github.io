---
layout: post
title: How to use Quasar in a custom Vue Component Library with Storybook
tags:
 - Software Engineering
 - Test Driven Development
 - Quasar
 - Vue
 - Storybook
---

[Quasar](https://quasar.dev/) is a popular Vue framework with a large component library and best-in-class support for building apps for web/mobile/browser extension/electron/etc. from the same codebase. Yet, despite significant community interest, it has been difficult to find solid, versatile answers for how to create custom component libraries based on Quasar. This tutorial provides those answers, demonstrating how to create a standalone Quasar component library which can be used in any Vue application, whether or not that app runs via the Quasar CLI, the Vue CLI, or another tool.



<details markdown="1">
  <summary>History of community interest in custom Quasar component libraries (2019-2023)</summary>

23 August 2019 - [Quasar Issue #4956](https://github.com/quasarframework/quasar/issues/4956)
> *OP:* Is there any way to build a quasar project as a standalone component (SFC (?)) to be used in another project, using the quasar cli preferably, or if it is not possible with it, any other way?
>
> *Maintainer:* The purpose of a project folder is not to build a component, but a website/app.

10 September 2019 - [Quasar Issue #5063](https://github.com/quasarframework/quasar/issues/5063) 
> *OP:* I built the following scenario without full success:
>   - Project A: A vue-cli + quasar (as plugin)
>   - Project B: A plain Vue-cli project that includes Project A as JS dependency
>
> *Maintainer*: Quasar CLI's purpose (and even Vue CLI's purpose) is not to build a component library, but to build a website/app.

 1 March 2020 - [Quasar Issue #5063](https://github.com/quasarframework/quasar/issues/5063#issuecomment-593114114)
> Here is a basic use case : we have multiple Vue apps, and are creating a centralized component library imported by all the apps. These components have dependencies on multiple Quasar components. . After adding Quasar as a plugin, ... and importing it in other apps, it results in conflicts

 12 March 2020 - [Quasar Issue #6604](https://github.com/quasarframework/quasar/issues/6604)
> *OP:* When having more than one Vue application, a good practice is to put common components in an external component library. But it seems that putting Quasar components in an external library and using it in a Quasar app is not possible currently (or at least is not documented)
>
> *Quasar Collaborator:* Your components are either `.js` files or `.vue` files. You can copy them in any new project. I think you mean something and I don't get it. Can you explain why the copy/paste of the files with components is not good?
>
> *OP:* Just to be sure : you are suggesting me that, every time we make an update on a component, we should copy / paste it manually on our 15 others apps ?
> 
> We are a team of 8, sometimes working on the same components at the same time, it will result in versioning nightmare. Refactoring components in a single, versionable, external lib is a key feature of Vue
> We were thinking about migrating, but we cannot use Quasar with such a constraint

20 February 2023 - [StackOverflow](https://stackoverflow.com/q/75510418/14765128)
> I am creating a library that contains some company standard components. It is built upon Quasar components. When I try to use the library it gives the following error: [Vue warn]: Failed to resolve component: q-input.

</details>

## Why build a custom Quasar component library?

For sharing components between multiple Quasar projects, the official recommendation is to create a [Quasar App Extension](https://quasar.dev/app-extensions/introduction/). App Extensions *require* the Quasar CLI, which beneficially removes tons of pain from creating a web app/mobile app/browser extension/electron app/etc., but unfortunately brings multiple downsides:

 - *Framework Lock-In*: Using the Quasar CLI for your project [tightly couples your code to the Quasar framework](https://blog.cleancoder.com/uncle-bob/2014/05/11/FrameworkBound.html).
 - *Reduced Testability:* Quasar supports [Cypress as an App Extension](https://testing.quasar.dev/packages/e2e-cypress/), but other common testing tools still have significant limitations: [Jest has an unsupported beta package](https://testing.quasar.dev/packages/unit-jest/) , [Vitest support is still in Alpha](https://testing.quasar.dev/packages/unit-vitest/), and the main testing page is full of [deprecation notices with no replacements](https://testing.quasar.dev/). Community efforts to support popular sandboxed component development tools like [Storybook](https://github.com/quasarframework/quasar/issues/11654#issuecomment-1618295838) or [Histoire](https://github.com/histoire-dev/histoire/issues/105) have been blocked by the difficulty of replicating Quasar CLI's  [significant boot complexity](https://quasar.dev/quasar-cli-webpack/boot-files/#quasar-app-flow) within the sandboxed environment.
 - *Reduced Ecosystem Interoperability:* The Quasar CLI requirement prevents Quasar App Extensions from being used in vanilla Vue projects, further limiting their reach.
 - *Delayed Access to Ecosystem Improvements*: When using the Quasar CLI, access to many ecosystem-wide innovations must wait until the Quasar CLI adds official support. Sometimes that support takes years to arrive. For example, it took until February 2024 for Vite >1.0 support to [reach a usable beta stage](https://github.com/quasarframework/quasar/releases/tag/%40quasar%2Fapp-vite-v2.0.0-beta.1), nearly [two full years after the community raised the need](https://github.com/quasarframework/quasar/issues/14077#issuecomment-1353213893) and began developing solutions.

For projects which do not have a strong need to share a nearly identical experience across Web, Mobile, Browser Extension, and/or Electron (probably rare given the dramatically different use cases for each environment), these downsides of the Quasar CLI are significant, even prohibitive.

This tutorial for creating a custom, standalone Quasar component library mitigates those downsides by answering the following questions:
 - How can one use Quasar components (including custom derivatives) in a vanilla Vue project?
 - How can one improve the testability of a project managed by the Quasar CLI?

## How to create a custom Quasar component library

### Create a vanilla Vue Component Library.

A custom Quasar component library is just a vanilla Vue Component Library with Quasar added on top. 

This tutorial assumes you already have an existing Vue Component Library. If not, I strongly recommend following my tutorial [How to create a custom Vue Component Library with robust testing via Storybook and Vitest]({% link _posts/2024-02-29-vue-component-library-storybook-vitest.md %}). You can also reference the excellent tutorials by [FreeCodeCamp](https://www.freecodecamp.org/news/how-to-create-and-publish-a-vue-component-library-update/) and [LogRocket](https://blog.logrocket.com/building-vue-3-component-library/).

### Install Quasar as a Vue CLI plugin

> Quasar's official docs for their [Vue CLI Quasar Plugin](https://quasar.dev/start/vue-cli-plugin/) start with a scary-looking warning banner. The concerns expressed in that warning refer to building Quasar **applications** with the Vue CLI, and thus do not apply to our **component library**.
{: .prompt-info }

Using the Vue CLI to manage your component library avoids all the limitations of the Quasar CLI. Additionally, if you use your Vue CLI-managed component library within a larger Quasar CLI managed application, you can still retain the cross-platform benefits of the Quasar CLI.

While Quasar's docs include instructions for configuring the [Vue CLI Quasar Plugin](https://quasar.dev/start/vue-cli-plugin/), the installer assumes you are modifying a full Vue application, so it takes many steps which are unnecessary for a component library. As such, this section will detail a manual installation (which is ultimately simpler). If you prefer to install Quasar via the Vue CLI (e.g. to compare the official installation with these manual instructions) feel free to expand the following details note:

<details markdown="1">
  <summary>How to install Quasar via the Vue CLI (reference-only)</summary>

Verify that you have Vue CLI v4.5.11+ installed
```bash
$ vue --version
@vue/cli 5.0.8
```

If you get a lower version or an error like `command 'vue' not found` then globally install the latest version of the Vue CLI.
```bash
npm uninstall --global vue-cli  // Vue CLI 2.x.x only

npm install --global @vue/cli
```

Now you can add install Quasar into your component library with the command `vue add quasar`. When the setup wizard asks **Allow Quasar to replace App.vue, ...** answer **No** since those changes don't apply to a component library. Otherwise, answer the questions according to your preference.
```bash
$ vue add quasar

📦  Installing vue-cli-plugin-quasar...

added 6 packages, and audited 1379 packages in 4s

218 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
✔  Successfully installed plugin: vue-cli-plugin-quasar

? Allow Quasar to replace App.vue, About.vue, Home.vue and (if available) router.js? No
? Pick your favorite CSS preprocessor: Sass
? Choose Quasar Icon Set Material
? Default Quasar language pack - one from 
https://github.com/quasarframework/quasar/tree/dev/ui/lang en-US
? Use RTL support? No
? Select features: Roboto font, Material, Material Outlined, Material Round, Material 
Sharp, Fontawesome, Ionicons, MDI, Eva

🚀  Invoking generator for vue-cli-plugin-quasar...
📦  Installing additional dependencies...

added 5 packages, and audited 1384 packages in 6s

221 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
⚓  Running completion hooks...

✔  Successfully invoked generator for plugin: vue-cli-plugin-quasar               
```

Note that this installation adds several files only applicable to web applications (icons to the public folder, overwriting favicons, adding Quasar to the runtime `dependencies`, `vue.config.ts`, etc.) In my experience, the installed Sass styles are also frequently broken.

</details>

#### Manual installation of Quasar as a Vue CLI plugin

Add Quasar and its Vue CLI plugin as a dev dependency
```bash
npm install --save-dev quasar @quasar/extras vue-cli-plugin-quasar sass sass-loader
```

Add Quasar to your library's `peerDependencies`
```diff
{
  "peerDependencies": {
      "vue": "^3.4.19",
+     "@quasar/extras": "^1.0.0",  // NOTE: Match the versions in your devDependencies
+     "quasar": "^2.0.0" 
  },
}
```
{: file='package.json' }

Create a stylesheet for your custom Quasar variables (e.g. color themes)
```sass
// It's highly recommended to change the default colors
// to match your app's branding.

$primary   : #027BE3
$secondary : #26A69A
$accent    : #9C27B0

$dark      : #1D1D1D

$positive  : #21BA45
$negative  : #C10015
$info      : #31CCEC
$warning   : #F2C037
```
{: file='lib/styles/quasar.variables.sass' }

Create a stylesheet importing Quasar's global styles
```sass
// The built-in Quasar styles. Defined separately to avoid conflicts
// with custom Quasar styles defined in downstream projects.
@import 'quasar/src/css/index.sass'
@import 'quasar/src/css/variables.sass'
```
{: file='lib/styles/quasar.global.sass' }

Create the `quasar-user-options.js` for the Quasar Vue CLI plugin's configuration settings
```javascript
import './styles/quasar.variables.sass'

// NOTE: Omit any fonts/icon packs you do not use.
import '@quasar/extras/roboto-font/roboto-font.css'
import '@quasar/extras/material-icons/material-icons.css'
import '@quasar/extras/material-icons-outlined/material-icons-outlined.css'
import '@quasar/extras/material-icons-round/material-icons-round.css'
import '@quasar/extras/material-icons-sharp/material-icons-sharp.css'
import '@quasar/extras/fontawesome-v5/fontawesome-v5.css'
import '@quasar/extras/ionicons-v4/ionicons-v4.css'
import '@quasar/extras/mdi-v4/mdi-v4.css'
import '@quasar/extras/eva-icons/eva-icons.css'

// To be used on app.use(Quasar, { ... })
export default {
  config: {},
  plugins: {
  }
}
```
{: file='lib/styles/quasar-user-options.js' }

Finally create a `setupQuasarApp.ts` script with a function to augment a given Vue `app` with Quasar functionality.
```typescript
import { type App } from 'vue'
import { Quasar } from 'quasar'
// @ts-expect-error - quasar-user-options is not yet typed
import quasarUserOptions from './quasar-user-options'

export function setupQuasarApp(app: App) {
  app.use(Quasar, quasarUserOptions)
}
```
{: file='lib/setupQuasarApp.ts' }

That's it for the library installation!

If your downstream project uses the Quasar CLI then you may be able to import and use components directly from your component library. Otherwise, (e.g. if your downstream project is vanilla Vue) you will have to import the Quasar stylesheets and the apply the Quasar setup function yourself. Your code might look something like this:

```diff
import { createApp } from 'vue'
import App from './App.vue'

+ import "my-component-library/styles/quasar.global.sass"
+ // ^⚠️ WARNING^: Applies global styles to base elements (e.g. h1, h2). You may
+ // have to list your custom styles later to override these Quasar styles.

+ import "my-component-library/styles/quasar.variables.sass"
+ import { setupQuasarApp } from "my-component-library/setupQuasarApp"

const app = createApp(App)
+ setupQuasarApp(app)
app.mount(#app)
```
{: file='your-vue-app/main.ts' }

### Add a custom component based on Quasar

For this tutorial let's create a custom DatePicker

Create a `DatePicker.vue`
```vue
<template>
	<QCard class="q-pa-md" style="max-width: min-content;" role="datepicker">
		<QDate mask="YYYY-MM-DD" :modelValue="modelValue" dense minimal @update:modelValue="onSelectDate"></QDate>
		<QBtn color="primary" @click="onSelectDate(dashedDate(new Date()))" label="Today" />
	</QCard>
</template>

<script lang="ts">
import { QBtn, QCard, QDate } from "quasar"

export function dashedDate(date: Date) {
	return date.toISOString().slice(0, 10)
}

export default {
	emits: ["update:modelValue"],
	components: {
		QBtn,
    QCard,
		QDate,
	},
	props: {
		modelValue: {
			type: String,
		},
	},
	methods: {
		dashedDate,
		onSelectDate(date: string) {
			this.$emit("update:modelValue", date)
		},
	},
}
</script>
```
{: file='lib/components/DatePicker.vue' }

Notice that we import all Quasar components used within the template. This differs slightly from a Quasar CLI managed project where all those components are available globally.

### Render and test Quasar components in Storybook.js

Create some stories for the DatePicker
```typescript
import type { Meta, StoryObj } from '@storybook/vue3';
import { userEvent, within } from '@storybook/testing-library';

import DatePicker from '../components/DatePicker.vue';

// CONFIGURATION
const meta = {
	title: "Date Picker",
	component: DatePicker,
  render(args, { argTypes }) {
    return {
      template: `<div>
        Selected Date (in parent): {{ args.modelValue }}
        <br/>
        <br/>
        <DatePicker v-bind="args" v-model="args.modelValue" />
      </div>`,
      props: Object.keys(argTypes),
      components: { DatePicker },
      data: () => ({ args }),
    }
  },
	tags: ["autodocs"],
} satisfies Meta<typeof DatePicker>;

export default meta;
type Story = StoryObj<typeof meta>;

// STORIES
export const Default: Story = {
	args: {},
  play: async ({ canvasElement }) => {
    const datePicker = within(canvasElement).getByRole('datepicker');
    await userEvent.click(within(datePicker).getByText("15"));
    await userEvent.click(within(datePicker).getByText("Today"));
  }
}

export const SpecificDate: Story = {
  args: {
    modelValue: "2022-05-23",
  },
}
```
{: file='lib/components/DatePicker.stories.ts' }

And update the Storybook Previewer to support our Quasar components
```diff
import type { Preview } from "@storybook/vue3";

+ import { setup } from '@storybook/vue3';
+ import { setupQuasarApp } from '../lib/setupQuasarApp';
+ import "../lib/styles/quasar.global.sass"

+ setup(setupQuasarApp)

const preview: Preview = {
  …
```
{: file='.storybook/preview.ts' }

### How to use Quasar's Sass variables in a custom component library

[Quasar has tons of Sass variables](https://quasar.dev/style/sass-scss-variables) which control much of the look and feel of a Quasar app. Officially these variables are only available to Quasar CLI managed apps, but supporting them in Vue CLI managed projects (like a component library) only requires configuring a single Vite plugin.

Install the Quasar Vite plugin
```bash
npm install --save-dev @quasar/vite-plugin
```

Add the Quasar Vite plugin to your `vite.config.ts`. Make sure to set the Quasar plugin's `sassVariables` option to the path to the file containing your overrides of Quasar's variables.
```diff
import vue from "@vitejs/plugin-vue";
+ import { quasar, transformAssetUrls } from "@quasar/vite-plugin";
…
export default defineConfig({
  plugins: [
-    vue(),
+    vue({ template: { transformAssetUrls } }),
+    quasar({ sassVariables: "lib/styles/quasar.variables.sass" }),
    
```
{: file='vite.config.ts' }


## Conclusion

Quasar is a fabulous tool for building Vue applications. Hopefully this tutorial has helped it become even more useful and testable!

Feel free to comment on your experience improving the testability of Quasar and/or using it in a custom component library!