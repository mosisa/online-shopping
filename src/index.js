import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import { TweetsComponents,TweetDetailComponent } from "./tweets";

const appEl = document.getElementById('root')
if(appEl){
  ReactDOM.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
    appEl
  );
}
const e = React.createElement
const compEl = document.getElementById('shop')
if(compEl){
  ReactDOM.render( 
     e(TweetsComponents,compEl.dataset),
     compEl
  );
}
const tweetDetailElement = document.querySelectorAll(".shop-detail")
tweetDetailElement.forEach(container=>{
  ReactDOM.render(  
  e(TweetDetailComponent,container.dataset),
       container);
})
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
