---
layout: post
comments: true
title:  "Setting up reactjs development environment from scratch"
date:   2018-05-23
categories: [javascript, reactjs, dev-environment]
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
1. React: To work with react we need to install it's dependencies like react, react-dom, etc.
2. Babel: ReactJS uses JSX syntax to speed up the development process. But the syntax is not understandable by browsers. So, we need a transcompiler (Babel) to convert JSX into a javascript code.
3. Webpack: It is a javascript code bundler. In ReactJS we deal with the components so, every component is written in a seperate file to quickly navigate to the component and make changes. It will be difficult to add all these files to webpage. So, we use webpack to to bundle all these components.

### Let's work on setting up dev environment for a simple app

1. create  and navigate to the directory "react_app"
	```bash
	mkdir react_app && cd react_app
	```
2. create a react package using command `npm init`. It will ask us some questions, just answer it. It will create a `package.json` file to manage the react app dependencies.
`package.json` file look similar as
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
	* `webpack`: to generate a single javascript files out of all components and host it on the dev server.
	* `webpack-dev-server`: it helps us to recompile the jsx every time we make changes to any component and loads the newly generated file onto the development server. Install it with the below command
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
	* **babel-loader**: It is a webpack helper to transforms JavaScript dependencies with babel
	* **babel-preset-env**: It determines the plugins to use and provides modern functionality on older browsers that do not natively support it.
	* **babel-preset-react**: Babel preset for all React plugins, for example turning JSX into javascript functions
	* **style-loader**: 
	* **css-loader**: we import `css` files in JSX files, it helps to resolve them.
	* **html-webpack-plugin**: It is needed to inject this into our DOM — adding a <style> tag into the <head> element of our HTML.
5. Now, create a directory  

6. Configure webpack to run using webpack-dev-server
	create a `webpack.config.js` and add below code to it.
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
