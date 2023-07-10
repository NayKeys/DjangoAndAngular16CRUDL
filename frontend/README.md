# This repo is no longer maintained. Consider using `npm init vite` and selecting the `svelte` option or — if you want a full-fledged app framework — use [SvelteKit](https://kit.svelte.dev), the official application framework for Svelte.

---

# svelte app

This is a project template for [Svelte](https://svelte.dev) apps. It lives at https://github.com/sveltejs/template.

To create a new project based on this template using [degit](https://github.com/Rich-Harris/degit):

```bash
npx degit sveltejs/template svelte-app
cd svelte-app
```

*Note that you will need to have [Node.js](https://nodejs.org) installed.*


## Get started

Install the dependencies...

```bash
cd svelte-app
npm install
```

...then start [Rollup](https://rollupjs.org):

```bash
npm run dev
```

Navigate to [localhost:8080](http://localhost:8080). You should see your app running. Edit a component file in `src`, save it, and reload the page to see your changes.

By default, the server will only respond to requests from localhost. To allow connections from other computers, edit the `sirv` commands in package.json to include the option `--host 0.0.0.0`.

If you're using [Visual Studio Code](https://code.visualstudio.com/) we recommend installing the official extension [Svelte for VS Code](https://marketplace.visualstudio.com/items?itemName=svelte.svelte-vscode). If you are using other editors you may need to install a plugin in order to get syntax highlighting and intellisense.

## Building and running in production mode

To create an optimised version of the app:

```bash
npm run build
```

You can run the newly built app with `npm run start`. This uses [sirv](https://github.com/lukeed/sirv), which is included in your package.json's `dependencies` so that the app will work when you deploy to platforms like [Heroku](https://heroku.com).


## Single-page app mode

By default, sirv will only respond to requests that match files in `public`. This is to maximise compatibility with static fileservers, allowing you to deploy your app anywhere.

If you're building a single-page app (SPA) with multiple routes, sirv needs to be able to respond to requests for *any* path. You can make it so by editing the `"start"` command in package.json:

```js
"start": "sirv public --single"
```

## Using TypeScript

This template comes with a script to set up a TypeScript development environment, you can run it immediately after cloning the template with:

```bash
node scripts/setupTypeScript.js
```

Or remove the script via:

```bash
rm scripts/setupTypeScript.js
```

If you want to use `baseUrl` or `path` aliases within your `tsconfig`, you need to set up `@rollup/plugin-alias` to tell Rollup to resolve the aliases. For more info, see [this StackOverflow question](https://stackoverflow.com/questions/63427935/setup-tsconfig-path-in-svelte).

## Deploying to the web

### With [Vercel](https://vercel.com)

Install `vercel` if you haven't already:

```bash
npm install -g vercel
```

Then, from within your project folder:

```bash
cd public
vercel deploy --name my-project
```

### With [surge](https://surge.sh/)

Install `surge` if you haven't already:

```bash
npm install -g surge
```

Then, from within your project folder:

```bash
npm run build
surge public my-project.surge.sh
```




# carbon-components-svelte

[![NPM][npm]][npm-url]
![GitHub](https://img.shields.io/github/license/ibm/carbon-components-svelte?color=262626&style=for-the-badge)
![npm downloads to date](https://img.shields.io/npm/dt/carbon-components-svelte?color=262626&style=for-the-badge)
<a href="https://discord.gg/J7JEUEkTRX">
<img src="https://img.shields.io/discord/689212587170201628?color=5865F2&style=for-the-badge" alt="Chat with us on Discord">
</a>

Carbon Components Svelte is a [Svelte](https://github.com/sveltejs/svelte) component library that implements the [Carbon Design System](https://github.com/carbon-design-system), an open source design system by IBM.

Design systems facilitate design and development through reuse, consistency, and extensibility.

The Carbon Svelte portfolio also includes:

- **[Carbon Icons Svelte](https://github.com/carbon-design-system/carbon-icons-svelte)**: 2,000+ Carbon icons as Svelte components
- **[Carbon Pictograms Svelte](https://github.com/carbon-design-system/carbon-pictograms-svelte)**: 900+ Carbon pictograms as Svelte components
- **[Carbon Charts Svelte](https://github.com/carbon-design-system/carbon-charts/tree/master/packages/svelte)**: 20+ charts, powered by d3
- **[Carbon Preprocess Svelte](https://github.com/carbon-design-system/carbon-preprocess-svelte)**: Collection of Svelte preprocessors for Carbon

## [Documentation](https://carbon-components-svelte.onrender.com)

Other forms of documentation are auto-generated:

- **[TypeScript definitions](types)**: Component TypeScript definitions
- **[Component Index](COMPONENT_INDEX.md)**: Component API in Markdown format
- **[Component API](docs/src/COMPONENT_API.json)**: Component API in JSON format

## Installation

Install `carbon-components-svelte` as a development dependency.

```sh
# Yarn
yarn add -D carbon-components-svelte

# npm
npm i -D carbon-components-svelte

# pnpm
pnpm i -D carbon-components-svelte
```

## Usage

### Styling

Before importing components, you will need to first apply Carbon component styles. The Carbon Design System supports five themes (2 light, 3 dark).

- **white.css**: Default Carbon theme (light)
- **g10.css**: Gray 10 theme (light)
- **g80.css**: Gray 80 theme (dark)
- **g90.css**: Gray 90 theme (dark)
- **g100.css**: Gray 100 theme (dark)
- **all.css**: All themes (White, Gray 10, Gray 90, Gray 100) using [CSS variables](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)

Each StyleSheet is [generated](scripts/build-css.js) from the flagship [carbon-components](https://github.com/carbon-design-system/carbon/tree/main/packages/carbon-components) library.

The compiled CSS is generated from the following `.scss` files:

- [css/white.scss](css/white.scss)
- [css/g10.scss](css/g10.scss)
- [css/g80.scss](css/g80.scss)
- [css/g90.scss](css/g90.scss)
- [css/g100.scss](css/g100.scss)
- [css/all.scss](css/all.scss)

#### CSS StyleSheet

```js
// White theme
import "carbon-components-svelte/css/white.css";

// Gray 10 theme
import "carbon-components-svelte/css/g10.css";

// Gray 80 theme
import "carbon-components-svelte/css/g80.css";

// Gray 90 theme
import "carbon-components-svelte/css/g90.css";

// Gray 100 theme
import "carbon-components-svelte/css/g100.css";

// All themes
import "carbon-components-svelte/css/all.css";
```

#### CDN

An alternative to loading styles is to link an external StyleSheet from a Content Delivery Network (CDN) like [unpkg.com](https://unpkg.com/).

This is best suited for rapid prototyping.

##### HTML

```html
<!DOCTYPE html>
<html>
  <head>
    <link
      rel="stylesheet"
      href="https://unpkg.com/carbon-components-svelte/css/white.css"
    />
  </head>
</html>
```

##### `svelte:head`

```html
<svelte:head>
  <link
    rel="stylesheet"
    href="https://unpkg.com/carbon-components-svelte/css/white.css"
  />
</svelte:head>
```

### SCSS

The most performant method to load styles is to import SCSS directly from carbon-components. Although it requires more set up, you can reduce the size of the bundle CSS by importing individual component styles instead of a pre-compiled CSS StyleSheet.

Refer to the [official Carbon guide on SASS](https://github.com/carbon-design-system/carbon/blob/v10/docs/guides/sass.md) for documentation.

### Dynamic theming

Use the "all.css" StyleSheet for dynamic, client-side theming.

```js
import "carbon-components-svelte/css/all.css";
```

Update the theme by setting the `theme` attribute on the `html` element. The default `theme` is `"white"`.

```html
<!DOCTYPE html>
<html lang="en" theme="g10">
  <body>
    ...
  </body>
</html>
```

Programmatically switch between each of the five Carbon themes by setting the "theme" attribute on the HTML element.

```html
<script>
  let theme = "white"; // "white" | "g10" | "g80" | "g90" | "g100"

  $: document.documentElement.setAttribute("theme", theme);
</script>
```

### Importing components

Import components from `carbon-components-svelte` in the `script` tag of your Svelte file. Visit the [documentation site](https://carbon-components-svelte.onrender.com) for examples.

```html
<!-- App.svelte -->
<script>
  import { Accordion, AccordionItem } from "carbon-components-svelte";
</script>

<Accordion>
  <AccordionItem title="Section 1" open> Content 1 </AccordionItem>
  <AccordionItem title="Section 2"> Content 2 </AccordionItem>
  <AccordionItem title="Section 3"> Content 3 </AccordionItem>
</Accordion>
```

**Refer to [COMPONENT_INDEX.md](COMPONENT_INDEX.md) for component API documentation.**

## Preprocessors

[carbon-preprocess-svelte](https://github.com/carbon-design-system/carbon-preprocess-svelte) is a collection of Svelte preprocessors for Carbon.

```sh
# Yarn
yarn add -D carbon-preprocess-svelte

# npm
npm i -D carbon-preprocess-svelte

# pnpm
pnpm i -D carbon-preprocess-svelte
```

### `optimizeImports`

`optimizeImports` is a script preprocessor that rewrites base imports from Carbon components/icons/pictograms packages to their source Svelte code paths. This can greatly speed up compile times during development while preserving typeahead and autocompletion hinting offered by integrated development environments (IDE) like VSCode.

The preprocessor optimizes imports from the following packages:

- [carbon-components-svelte](https://github.com/carbon-design-system/carbon-components-svelte)
- [carbon-icons-svelte](https://github.com/carbon-design-system/carbon-icons-svelte)
- [carbon-pictograms-svelte](https://github.com/carbon-design-system/carbon-pictograms-svelte)

**Before & After**

```diff
- import { Button } from "carbon-components-svelte";
- import { Add16 } from "carbon-icons-svelte";
- import { Airplane } from "carbon-pictograms-svelte";
+ import Button from "carbon-components-svelte/src/Button/Button.svelte";
+ import Add16 from "carbon-icons-svelte/lib/Add16.svelte";
+ import Airplane from "carbon-pictograms-svelte/lib/Airplane.svelte";
```

#### Usage

```js
// svelte.config.js
import { optimizeImports } from "carbon-preprocess-svelte";

export default {
  preprocess: [optimizeImports()],
};
```

`svelte-preprocess` should be invoked before any preprocessor from `carbon-preprocess-svelte`.

```diff
// svelte.config.js
+ import sveltePreprocess from "svelte-preprocess";
import { optimizeImports } from "carbon-preprocess-svelte";

export default {
  preprocess: [
+   sveltePreprocess(),
    optimizeImports()
  ],
};
```

## Examples

- [examples/rollup](examples/rollup/)
- [examples/sveltekit](examples/sveltekit/)
- [examples/vite](examples/vite/)
- [examples/webpack](examples/webpack/)

## TypeScript support

[TypeScript definitions](types) are generated by [sveld](https://github.com/carbon-design-system/sveld).

## Contributing

Refer to the [Contributing guidelines](CONTRIBUTING.md).

## [Changelog](CHANGELOG.md)

## License

[Apache 2.0](LICENSE)

[npm]: https://img.shields.io/npm/v/carbon-components-svelte.svg?color=262626&style=for-the-badge
[npm-url]: https://npmjs.com/package/carbon-components-svelte