---
layout: post
comments: true
title:  "Understanding ReactJS Component Lifecycle"
description: "React component has 7 lifecycle methods.They are categorized to (1) Mounting Methods (2) Updating Methods (3) Unmounting Methods. "
keywords: "component lifecycle methods, react lifecycle methods"
date:   2018-05-25
categories: [javascript, reactjs, component lifecycle methods, react lifecycle methods]
author: Anjaneyulu
---

We know that ReactJS is a component based javascript library. In every ReactJS application components are rendered onto virtual DOM. Before/After rendering onto the virtual DOM every component goes through some of the methods. We call these methods as ReacjJS Component Lifecycle Methods. We can categorize these methods into three based on component initialization, updation and destruction. They are (1) Mounting Methods(initialization) (2) Updating Methods (updation) (3) Unmounting Methods (destruction)

### ReactJS Component Mounting Methods
 * These methods are called when the component is being rendered for the first time.
 * Whenever a component is rendered the first method called is "constructor".
 * In the constructor we can provide default/initial data for component state and props.
 * After constructor, Mounting Methods will be called. They are
   1. **static getDerivedStateFromProps**:
   	* It is called just before `render` method.
   	* It takes two parameters `props` and `state` and it should return an `object` with data or `null` for empty object to update the state.
   2. **render**:
    * It is called after method `componentWillMount`. It simply renders the react component onto the DOM by using props and state of the component. 
   3. **componentDidMount**:
    * It is called after method `render`.
    * In this method we can do stuff like calling REST API to update the state, etc.

### ReactJS Component Updating Methods
 * We know ReactJS is very quick to user actions. Some times we need to updated DOM based on user actions. To update the React DOM with respect to user actions we use ReactJS component updating methods. They are
   1. **shouldComponentUpdate**:
   	* It is called before component re-renders right after change in props of state.
   	* It's a boolean method which tells react to re-render the DOM or not. Default return value for this method is `true`.
   2. **render**:
    * It will update the DOM with new props and new state.
   3. **componentDidUpdate**:
   	* It is called immediately after updating occurs. It is not called for the initial render.
   	* It works just like method `componentDidMount`.


### ReactJS Component Unmounting Methods
 * It has only one method `componentWillUnmount` which executed just before ReactJS component removed.
 * It is called as "cleanup method". Because, here we can remove the unused data, unwanted network requests, etc.
 * We should not call method `setState` here because the component will never be re-rendered.

### Play with below component to know more
* open your browser console to see the logs.
```javascript
import React from "react";
class LifeCycleMethods extends React.Component{
	constructor(props){
		super(props)
		console.log('constructor')
		this.state = {"username": ""}
		this.handleChange = this.handleChange.bind(this);
	}
	// component methods
	// ReactJS Component Mounting Methods
	static getDerivedStateFromProps(props, state){
		console.log("getDerivedStateFromProps")
		console.log(props, state)
		return {}
	}
	componentDidMount(){
		console.log("componentDidMount")
	}
	// ReactJS Component Updating Methods
	shouldComponentUpdate(){
		console.log("shouldComponentUpdate")
		return true
	}
	componentDidUpdate(){
		console.log("componentDidUpdate")
	}
	// ReactJS Component Unmounting Methods
	componentWillUnmount(){
		console.log("componentWillUnmount")
	}
	// custom methods
	handleChange(event) {
    	this.setState({username: event.target.value});
	}
	render(){
		console.log("render")
		return(
			<form>
				<label>Name: </label>
				<input name="username" onChange={this.handleChange}/>
				<br/>
				Your name is "{this.state.username}"
			</form>
		);
	}
}
module.exports = LifeCycleMethods;
```  


<br/>
_Stay tuned for our next post "Working with Events in ReactJS"_
