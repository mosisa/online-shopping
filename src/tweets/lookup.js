import { backendLookup } from "../lookup";


export function createTweet(newTweet,callback){
    backendLookup("POST","/shop/create/",callback,{content:newTweet})   
  }

export function tweetAction(tweetId,action,callback){
  const data = {id:tweetId,action:action}
  backendLookup("POST","/shop/like/",callback,data)   
} 
export function tweetDetailView(tweetId,callback){
  backendLookup("GET", `/shop/${tweetId}`,callback)    
} 
export function loadTweets(username,callback){
    let endpoint = "/shop/"
    if(username){
      endpoint = `/shop/?username=${username}`
    }
    backendLookup("GET",endpoint,callback)    
}