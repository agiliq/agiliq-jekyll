---
layout: post
comments: true
title:  "Setting up reactjs development environment from scratch"
description: "Basic Tools needed to work with ReactJS are react, babel and webpack. Babel transcompiles JSX syntax into javascript syntax."
keywords: "reactjs from scratch, setting up reactjs, reactjs dev environment"
date:   2018-05-23
categories: [javascript, reactjs, dev-environment, from scratch]
author: Anjaneyulu
---
### What is ReactJS ?
ReactJS is a javascript library. It is used to build web user interfaces. It is mostly used to develop single page web applications. We can also develop mobile applications using library ReactJS. To develop mobile applications we use library ReactNative.

### Advantages of ReactJS
* ReactJS a opensource library
* ReactJS is used to build single page web applications.
* ReactJS is component based. A webpage can be devided into simple modules called a "component". We can build a complex component using basic components. Every component has it's own state to respond to the events. Because component logics are writtern in javascript.
* ReactJs uses a virtual DOM to speed up the rendering process.
* Code re-usability is a must in Software Development. In web development most of the functionality is repeated. So, we can reuse the components.
* ReactJS uses ES06 javasxript syntax called as JSX. It speeds up the ReactJS appliations development time. JSX is a advanced javascript syntax.


### Install NodeJS and NPM
Nodejs is a cross platform javascript runtime environment. It's capable of executing the javascript code server-side. It is used with ReactJS to run the react development server.
NPM(node package manager) is a manager of javascript packages. By using it we can install javascript packages required for our project. It's just like python pip.

To install NodeJS and NPM on ubuntu run the below commands on terminal

```bash
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install npm --global
```

Confirm installation of NodeJs and NPM

```bash
node -v
# v8.0.0
npm -v
# 6.0.0
```


### Basic Tools needed to work with ReactJS
1. **React**: To work with react we need to install it's dependencies like react, react-dom, etc.
2. **Babel**: ReactJS uses JSX syntax to speed up the development process. But the syntax is not understandable by browsers. So, we need a transcompiler (Babel) to convert JSX into a javascript code.
3. **Webpack**: It is a javascript code bundler. In ReactJS we deal with the components so, every component is written in a seperate file to quickly navigate to the component and make changes. It will be difficult to add all these files to webpage. So, we use webpack to to bundle all these components.

### setting up dev environment for a simple app

1. create  and navigate to the directory "react_app"
	```bash
	mkdir react_app && cd react_app
	```
2. create a react package using command `npm init`. It will ask some questions either answer or just press <Enter> key. It will create a file `package.json` file to manage the react app dependencies. `package.json` file looks similar to
	```bash
{
	"name": "react_app",
	"version": "1.0.0",
	"description": "",
	"main": "index.js",
	"scripts": {
		"test": "echo \"Error: no test specified\" && exit 1"
	},
	"author": "Agiliq",
	"license": "ISC"
}
	```
3. Now, install `webpack` and `webpack-dev-server`
	* **webpack**: to generate a single javascript files out of all components and host it on the dev server.
	* **webpack-dev-server**: it helps us to transcompile the jsx every time we make changes to any component and it loads the newly generated file onto the development server. Install it with the below command
	```bash
npm install webpack webpack-cli webpack-dev-server --save-dev
	```
4. install `react`, `react-dom`, `babel` and it's dependencies
	```bash
npm install --save react react-dom
npm install --save-dev babel-core babel-loader babel-preset-env babel-preset-react
npm install --save-dev style-loader css-loader
npm install --save-dev html-webpack-plugin
echo '{ "presets": ["react", "env"] }' > .babelrc
	```
	* **babel-core**: It transforms ES6 code into ES5
	* **babel-loader**: It is a webpack helper to transform the JavaScript dependencies with babel
	* **babel-preset-env**: It determines the plugins to use and provides modern functionality on older browsers that do not natively support it.
	* **babel-preset-react**: Babel preset for all React plugins, for example, turning JSX into javascript functions
	* **css-loader**: we import `css` files in JSX files, it helps to resolve them.
	* **style-loader**: it collects all the styles and makes it a single file and injects it into DOM.
	* **html-webpack-plugin**: It is needed to inject this into our DOM — adding a `<style>` tag into the `<head>` element of our HTML.
5. We will going to create a directory structure as below for our application
	```bash
	    react_app
	    ├── src
	    │   ├── components
	    │   │   └── HelloWorld
	    │   │       ├── HelloWorld.css
	    │   │       └── HelloWorld.js
	    │   ├── index.html
	    │   └── index.js
	    ├── .babelrc
	    ├── package.json
	    └── webpack.config.js
	```
	* **react_app**: Root of project directory.
	* **react_app/src**: It contains all our react app source code.
	* **react_app/src/components**: It contains the components of react app.
	* **react_app/src/index.html**: It it used by html webpack plugin to work with react. It contains the root element which react renderer will use. 
	* **react_app/src/index.js**: It is the entry point where react starts rendering the components.
	* **.babelrc**: It provide the options for babel-loader.
	* **package.json**: It contains the package dependency information and startup scripts to be used.
	* **webpack.config.js**: It contains the configuration information of webpack.

	Now, we know why we use above files. Let's configure all these files.

6. To configure webpack create `webpack.config.js` and add below code to it.
	```bash
	const HtmlWebPackPlugin = require("html-webpack-plugin");

	const htmlWebpackPlugin = new HtmlWebPackPlugin({
	  template: "./src/index.html",
	  filename: "./index.html"
	});

	module.exports = {
	  module: {
	    rules: [
	      {
	        test: /\.js$/,
	        exclude: /node_modules/,
	        use: {
	          loader: "babel-loader"
	        }
	      },
	      {
	        test: /\.css$/,
	        use: [
	          {
	            loader: "style-loader"
	          },
	          {
	            loader: "css-loader",
	            options: {
	              modules: true,
	              importLoaders: 1,
	              localIdentName: "[name]_[local]_[hash:base64]",
	              sourceMap: true,
	              minimize: true
	            }
	          }
	        ]
	      }
	    ]
	  },
	  plugins: [htmlWebpackPlugin]
	};
	```
	Note: we can also use other plugins like `scss-loader` to work with it.
7. Now, open `package.json` and add below start scripts to it.
	```json
	"scripts": {
	    "start": "webpack-dev-server --mode development --open --port 3000",
	    "build": "webpack --mode production"
	  }
	```
	These are aliases for lengthy commands. If run command `npm run start` then it will run command `webpack-dev-server --mode development --open --port 3000` which will opens a browser with dev host on port 3000 `http://localhost:3000`
	For production, use command `npm run build`. After running the command it will creates a new directory named `dist` with bundled javascript, css and images.

	After adding the above code `package.json` looks like below
	```bash
{
  "name": "react_app",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "webpack-dev-server --mode development --open --port 3000",
    "build": "webpack --mode production"
  },
  "keywords": ["react from scratch"],
  "author": "Agiliq",
  "license": "ISC",
  "devDependencies": {
    "babel-core": "^6.26.3",
    "babel-loader": "^7.1.4",
    "babel-preset-env": "^1.7.0",
    "babel-preset-react": "^6.24.1",
    "css-loader": "^0.28.11",
    "html-webpack-plugin": "^3.2.0",
    "style-loader": "^0.21.0",
    "webpack": "^4.8.3",
    "webpack-cli": "^2.1.3",
    "webpack-dev-server": "^3.1.4"
  },
  "dependencies": {
    "react": "^16.3.2",
    "react-dom": "^16.3.2"
  }
}

	```
8. Let's see how other files looks like<br/>
	**react_app/src/index.html**
	```html
	<html lang="en">
	<head>
	  <meta charset="UTF-8">
	  <meta name="viewport" content="width=device-width, initial-scale=1.0">
	  <meta http-equiv="X-UA-Compatible" content="ie=edge">
	  <title>React App</title>
	</head>
	<body>
	  <section id="main"></section>
	</body>
	</html>
	```
	**react_app/src/index.js**
	```javascript
	import React from "react";
	import ReactDOM from "react-dom";
	import Hello from "./components/HelloWorld/HelloWorld"

	ReactDOM.render(<Hello />, document.getElementById("main"));
	```
	**react_app/src/components/HelloWorld.js**
	```javascript
	import React from "react";
	import style from "./HelloWorld.css";

	const HelloWorld = () => {
	  return (<div className={style.Hello}>
	           HelloWorld
	         </div>)
	}

	module.exports = HelloWorld;
	```
	**react_app/src/components/HelloWorld.css**
	```css
	.Hello{
		font-size: 100px;
		color: green;
	}
	```

Now, open your terminal and change directory to `react_app` and run the command `npm run start`. It will open browser with url `http://localhost:3000`. You can find text `Hello world` with font size `100px` with green color.
When we run command `npm run start` or `webpack-dev-server --mode development --open --port 3000` webpack runs the dev server using the configuration file `webpack.config.js` and starts execution from file `index.js` because `index.js` pointed in `package.json`

To test it let's change the text in `HelloWorld` component to `"Hello Agiliq"`.

<br/>
_Stay tuned for our next post "Understanding State and Props in React"_