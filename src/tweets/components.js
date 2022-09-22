import React,{useEffect,useState} from 'react'
import { loadTweets,createTweet,tweetAction,tweetDetailView } from "./lookup";

export function TweetsComponents(props){
  const textAreaRef = React.createRef()
  const [newTweets,setNewTweets] = useState([])
  const canTweet = props.canTweet==="false" ? false : true
  const handleBackEnd=(response,status)=>{
    let tempNewTweets = [...newTweets]
    if(status===201){
      tempNewTweets.unshift(response)
      setNewTweets(tempNewTweets)
    }else{
      console.log(response)
      alert("there was an error please try again")
    }
  }
  const handleSubmit =(event)=>{
    event.preventDefault()
    const newValue = textAreaRef.current.value
    createTweet(newValue,handleBackEnd)
    textAreaRef.current.value=""
  }
  
    return <div className={props.className}>
              {canTweet === true && <div className="col-12 mb-3">
                            <form onSubmit={handleSubmit}>
                              <textarea ref={textAreaRef} required={true} className="form-control">
                              </textarea>
                              <button className="btn btn-primary my-3">
                                  Post
                              </button>
                            </form>
                        </div>
        }
              <TweetList newTweets={newTweets} {...props}/>
            </div> 
}

export function TweetList(props){
    const [shopInit,setShopInit] = useState([])
    const [tweets,setTweets] = useState([])
    const [tweetDidSet,setTweetDidSet] = useState(false)
    useEffect(()=>{
     let final= [...props.newTweets].concat(shopInit)
     if(final.length!==tweets.length){
          setTweets(final)
     }
    },[props.newTweets,tweets,shopInit])
    useEffect(()=>{
      if(tweetDidSet === false){
      const myCallBack = (response,status) =>{
        if(status === 200){
          setShopInit(response)
          setTweetDidSet(true)
        }else{
          alert("there was an error")
        }
     
      }
      loadTweets(props.username,myCallBack)
    }
    },[shopInit,tweetDidSet,setTweetDidSet,props.username])
   return tweets.map((item,index)=>{
    return <Tweet tweet = {item} className='my-5 py-5 border bg-white text-dark' key={`${index}-{item.id}`}/> 
  })
  } 
export function Actionbtn(props){
    const {tweet,action,didPerformAction} = props
    const likes =tweet.likes ? tweet.likes :0
    const className = props.className ? props.className: 'btn btn-primary btn-sm'
    const actionDisplay = action.display ? action.display : "action"
    const handleBackEndActionEvent= (response,status)=>{
      if((status === 200 || status === 201) && didPerformAction){
        didPerformAction(response)
      }
    }
    const handleClick = (event)=>{
        event.preventDefault()
        tweetAction(tweet.id,action.type,handleBackEndActionEvent)
       
    }
    const display = action.type==="like" ?` ${likes} ${actionDisplay}`:actionDisplay
   
return <button className={className} onClick={handleClick}>{display}</button>
  } 
  
 export function Tweet(props){
    const {tweet} = props
    const [actionTweet,setActionTweet] =useState(props.tweet ? props.tweet : null)
    const className = props.className ? props.className: 'col:10 mx-auto col-md-6'
    const path = window.location.pathname
    const idRejex = /(?<tweetid>\d+)/
    const match = path.match(idRejex)
    const urlTweetId = match ?  match.groups.tweetid : -1
    const isDetail = `${tweet.id}`===`${urlTweetId}`
    const handleClicks = (event)=>{
      event.preventDefault()
      window.location.href = `/${tweet.id}`
    }
    const handlePerformAction= (newActionTweet) =>{
          setActionTweet(newActionTweet)
    }
    return <div className={className}>
              <p>{tweet.id} - {tweet.content}</p>
              {actionTweet &&  <div className="btn btn-group">
                    <Actionbtn tweet = {actionTweet} didPerformAction={handlePerformAction} action= {{type:"like", display:"likes"}}/>
                    <Actionbtn tweet = {actionTweet} didPerformAction={handlePerformAction} action= {{type:"unlike", display:"unlikes"}}/>
                  {isDetail === true ? null : <button className="btn btn-outline-primary" onClick={handleClicks}>view</button>}
                </div>
 } 
           </div>
  }
   
  export function TweetDetailComponent(props){
    const {tweetId} = props
    const [didLookUp,setDidLookUp] = useState(false)
    const [tweet,setTweet] = useState(null)
    const handleBackEndLookUp =(response,status)=>{
        if(status===200){
          setTweet(response)
        }else{
          alert("there was an error findng your tweets")
        }
    }
    useEffect(()=>{
      if(didLookUp===false){
        tweetDetailView(tweetId,handleBackEndLookUp)
        setDidLookUp(true) 
      }

    },[didLookUp,setDidLookUp,tweetId])
    return tweet === null ? null : <Tweet tweet={tweet} className={props.className}/>
  }