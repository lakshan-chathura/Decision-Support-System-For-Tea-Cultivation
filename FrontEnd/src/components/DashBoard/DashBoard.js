import React from 'react'
import Header from './Header';
import './DashBoard.css'
import { Redirect } from 'react-router-dom'

export default function DashBoard(props){

    function getTheClientHeight(){
      var w = window,
      d = document,
      e = d.documentElement,
      g = d.getElementsByTagName('body')[0],
      x = w.innerWidth || e.clientWidth || g.clientWidth,
      y = w.innerHeight|| e.clientHeight|| g.clientHeight;
      return y
    }

    let height = getTheClientHeight()

    if(localStorage.getItem('loggedIn') !== "true" && !props.loggedIn){
      props.setLoggedIn(false)
      localStorage.removeItem('loggedIn')
      return <Redirect to="/"/>
    }
    else{
      return(
          <div style={{height:"100%"}}>
              <Header current={props.to} setLoggedIn={props.setLoggedIn}/>
              <div style={{height: height - 56}} className="dashboardBackground">
                {props.sideComponent}
              </div>
          </div>
      )
    }
}
