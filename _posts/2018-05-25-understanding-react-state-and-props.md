---
layout: post
comments: true
title:  "Understanding State and Props in ReactJS"
description: "React controls the data flow in the components with state and props. The data in states and props are used to render the Component with dynamic data."
keywords: "reactjs state and props, state and props in react"
date:   2018-05-25
categories: [javascript, reactjs, state and props]
author: Anjaneyulu Batta
---

ReactJS is component based. We devide the complex UI into basic components. After developing the basic components we again adds all these components to create a complex UI which also called as complex component. React controls the data flow in the components with state and props. The data in states and props are used to render the Component with dynamic data.

### Understanding ReactJS Props
 * In ReactJS we use props to send data to components.
 * In ReactJS every component is treated as a pure javascript function.
 * In ReactJS props are equivalent to parameters of a pure javascript function.
 * Props are immutable. Because these are developed in the concept of pure functions. In pure functions we cannot change the data of parameters. So, also cannot change the data of a prop in ReactJS.

 * ReactJS funtion based component
	```javascript
import React from "react";
const Profile = (props) => {
	// props.img_url = 'http://via.placeholder.com/350x150'
	const style = {
		padding: '10px',
		border: '1px solid green',
		display: 'block',
	    marginLeft: 'auto',
	    marginRight: 'auto',
	    width: '50%',
	    color: '#4db1e8',
	    textAlign: 'center',
	    fontFamily: 'sans-serif'
	}
	return (
		<div style={style}>
			<img src={props.logo_url} height="250px"/>
			<h1>{props.title}</h1>
		</div>
	);
}
module.exports = Profile;
	```
 * ReactJS class based component
	```javascript
import React from "react";
class Profile extends React.Component {
	render(){
		// this.props.img_url = 'http://via.placeholder.com/350x150'
		const style = {
			padding: '10px',
			border: '1px solid green',
			display: 'block',
		    marginLeft: 'auto',
		    marginRight: 'auto',
		    width: '50%',
		    color: '#4db1e8',
		    textAlign: 'center',
		    fontFamily: 'sans-serif'
		}
		return (
			<div style={style}>
			  <img src={this.props.logo_url} height="250px"/>
			  <h1>{this.props.title}</h1>
			</div>
		);
	}
}
module.exports = Profile;
	```
 * Import and use of one of the above ReactJS components like below
	```javascript
import React from "react";
import ReactDOM from "react-dom";
import Profile from "./components/Profile"
ReactDOM.render(
	<Profile 
		logo_url="https://books.agiliq.com/projects/django-design-patterns/en/latest/_static/logo.png"
		title="Mobile App, Web App and API Development and More"/>,
	document.getElementById("main")
);
	```
	* In above code we have passed two props "logo_url" and "title". As we discussed earlier props are immutable. try to change the data of props if you succeded then let us know. The finished component looks like below image.
	![reactjs state and props](/assets/images/reactjs/agiliq_react_state_and_props.png)
	* we do not need to use `this` for function based components to access props but we have to use `this` to access props(`this.props.<prop_name>`).


### Understanding ReactJS State
* State is like a data store to the ReactJS component. It is mostly used to update the component when user performed some action like `clicking button`, `typing some text`, `pressing some key`, etc.
* `React.Component` is the base class for all class based ReactJS components. Whenever a class inherits the class `React.Component` it's constructor will automatically assigns attribute `state` to the class with intial value is set to `null`. we can change it by overriding the method `constructor`.
	* In many cases we need to update the state. To do that we have to use the method `setState` and directly assigning like `this.state = {'key': 'value'}` is strictly prohibited.
* Let's try to use `state` concept in our component by changing a little code in above ReactJS component that we have created
	```javascript
class Profile extends React.Component {
	constructor(props){
		super(props)
		this.state = {"show_technologies": false}
		this.see_our_technologies = this.see_our_technologies.bind(this);
	}
	see_our_technologies(){
		this.setState({"show_technologies": true})
	}
	render(){
		console.log(this.state)
		const style = {
			padding: '10px',
			border: '1px solid green',
			display: 'block',
		    marginLeft: 'auto',
		    marginRight: 'auto',
		    width: '50%',
		    color: '#4db1e8',
		    textAlign: 'center',
		    fontFamily: 'sans-serif'
		}
		const tech = {
			background: '#4db1e8',
			color: '#fff',
			padding: '5px',
			marginRight: '5px'
		}
		return (
			<div style={style}>
				<img src={this.props.img_url} height="250px"/>
				<h1>{this.props.title}</h1>
				{this.state.show_technologies ?
					<p>
						<span style={tech}>Python</span>
						<span style={tech}>Django</span>
						<span style={tech}>Django REST</span>
						<span style={tech}>ReactJS</span>
						<span style={tech}>Angular</span>
						<span style={tech}> and More</span>
					</p>
					:
					<button onClick={this.see_our_technologies}>Click to see Our Technologies</button>
				}
			</div>
		);
	}
}
module.exports = Profile;
	```
  * After updating the component with above code then UI updates with a button
  ![reactjs state and props](/assets/images/reactjs/agiliq_reactjs_state_button.png)
  * When we click on the button we can see the technologies without button
  ![reactjs state and props](/assets/images/reactjs/agiliq_react_state_technologies.png)
  * In above code we have overriden the method `constructor` and set the initial state with key `show_technologies` to `false`. while rendering the component react checks the `show_technologies` value and if it is set to `false` react only renders the button. we have bind the `click` event to the button. Whenever user clicks on it the event handler will change the state to `{"show_technologies": true}` by using the method `setState`.
  * Now, state is changed so, react will again render the component with new changes. The key `show_technologies` is now set to `true` so, It hide's the button and shows us `technologies` as we have used the conditional operator.
  * Whenever the state updated in the component all of it's children components will also renders again to render/show the latest changes.
  * This is how react handles the `state`.

### Types of ReactJS Components
In ReactJS we have two different types of components.
  1. Stateless ReactJS Component
  * All function based components can be considered as stateless ReactJS components.
  * Stateless ReactJS Components are pure javascript functions so, we don't need to have state.
  2. Stateful ReactJS Component
  * All class based components can be considered as stateful ReactJS components.
  * Stateful ReactJS Components inherits the class `React.Component` so, `state` get's inherited.

<br/>
_Stay tuned for our next post ["Understanding ReactJS Component Lifecycle"](/blog/2018/05/understanding-reactjs-component-lifecycle/)_
