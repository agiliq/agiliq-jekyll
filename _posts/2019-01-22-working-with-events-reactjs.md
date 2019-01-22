---
layout: post
comments: true
title:  "Working with Events in ReactJS"
description: "Handling events in any react application is inevitable. ReactJS events are just like javascript events they both just differ in a syntatical way"
keywords: "events in ReactJS, event binding react"
date:   2019-01-22
categories: [javascript, reactjs, handling events]
main_category: reactjs
author: Anjaneyulu
---

### Handling events in ReactJS
Handling events in any react application is inevitable. ReactJS events are just like javascript events they both just differ in a syntatical way.(i.e the way of writing the code). As we know ReactJS provides an elegant and simple syntax when compare to the raw javascript.

### Simple Click Event in ReactJS
 * Handling events in react easy very simple.
 * Follow camel case notations rather than lowercase.
 * Try to use arrow functions wherever possible because they are faster.
 * Let's write some code to explore events in reactjs

Html Code
```html
<div id="root">
</div>
```
ReactJS Code
```javascript
 class LogoToggle extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      toggle: true,
    };
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    this.setState(prevState => ({
      toggle: !prevState.toggle
    }));
  }

  render() {
    if(this.state.toggle){
      return (
          <button onClick={this.handleClick}>
            {this.state.toggle ? 'Show Agiliq Logo' : 'Hide Agiliq Logo'}
          </button>
      );
    }else{
      return(
        <div>
          <button onClick={this.handleClick}>
            {this.state.toggle ? 'Show Agiliq Logo' : 'Hide Agiliq Logo'}
          </button>
          <img width="300" src="http://books.agiliq.com/projects/django-design-patterns/en/latest/_static/logo.png"/>
        </div>
      );
    }
  }
}

ReactDOM.render(
  <LogoToggle />,
  document.getElementById('root')
);
```
 * you can check it out in <a target="__blank" href="https://codepen.io/anjaneyulubatta505/pen/KXKgxM">codepen</a> for live example
 * In above code we have bind the function `handleClick` to the button. Based on the `toggle` variable in the state we are rendering the `LogoToggle` component.
 * If `toggle` is set to "true" then we are hiding the image otherwise we are displaying the image.
 * In above example we have just used the `click` event. We can also use more events like `onClickCapture`, `onKeyDown`, `onKeyPress`, etc.
 * You can checkout these events in react official documentation at <a target="__blank" href="https://reactjs.org/docs/events.html">https://reactjs.org/docs/events.html</a>

### Types of Event Binding in ReactJs
  * For every component we have a state. In most of the cases we use it.
  * State is not available directly on the  component method/function.
  * We have to externally bind `this` keyword to the method/function in order to use component state.
  * We can achieve it in two ways. 1. Binding in the constructor method, 2. Binding in the render method.

### Binding in the constructor method

```javascript
class MyComponent extends Component {
  constructor() {
    this.handleClick = this.handleClick.bind(this);
  }
  handleClick(){
    // do something
  }
  render() {
    return (<button onClick={this.handleClick}/>);
  }
}

```
  * In above code we have overriden the method `component` and binded the state.

### Binding in the render method

```javascript
class MyComponent extends Component {
  handleClick(){
    // do something
  }
  render() {
    return (<button onClick={this.handleClick.bind(this)}/>);
  }
}

```
  * In above code we have dynamically binded the state in the render method.

### Points to Note
  * The best place to bind the event handlers is within the constructor because if we use the event handler in more than once then it will lead to performance issues.
  * Do not bind `this` to event handler method if event handler does not requires component state.

