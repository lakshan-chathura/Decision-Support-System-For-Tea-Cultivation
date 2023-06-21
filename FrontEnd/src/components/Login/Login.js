import React from 'react'
import './Login.css'
import { Redirect } from 'react-router-dom'

export default function Login(props){
    function login(){
      let username = document.getElementById('txtusername').value
      let password = document.getElementById('txtpassword').value
      let errorcode = ""
      let loginMessage = ""

      if(username === ""){
        errorcode += "eu"
      }
      else if(username !== "admin"){
        errorcode += "wu"
      }

      if(password === ""){
        errorcode += "ep"
      }
      else if(password !== "admin"){
        errorcode += "wp"
      }

      let loginBox = document.getElementById("loginBox")
      let loginAlert = document.getElementById("loginAlert")

      if(errorcode === ""){
        loginMessage = "Login is successfull.Wait for a moment"
        loginAlert.className = "alert alert-success alert-success-custom"
        localStorage.setItem('loggedIn',true)
        setTimeout(function(){
          props.setLoggedIn(true)
        },3000)
      }
      else{
        switch (errorcode) {
          case "euep":loginMessage = "Please enter the username and password";break;
          case "euwp":loginMessage = "Please enter the username";break;
          case "wuep":loginMessage = "Please enter the password";break;
          case "wuwp":loginMessage = "Password or username is invalid";break;
          default:loginMessage = "Unknown error encountered";break;
        }
        loginBox.className = "alert alert-danger alert-danger-custom"
      }
      loginBox.style.height = "42%"
      loginAlert.style.display = "flex"
      loginAlert.innerHTML = loginMessage
    }
    // <!--38-42->
    console.log(props.loggedIn)
    if(props.loggedIn || localStorage.getItem('loggedIn')){
      return <Redirect to="/setup"/>
    }
    else{
      return(
          <div className="loginPageBackground">
              <div style={{width:"100%",height:"100%",backgroundColor:"black",opacity:"0.5"}}></div>
              <div id="loginBox" className="loginBoxBackground" style={{height: "36%"}}>
                  <h3 style={{textAlign:"center"}}><b>Welcome to the Decision Support System</b></h3>
                  <form className="col-12 loginForm">
                      <div className="form-group">
                          <label>Username</label>
                          <input type="text" className="form-control form-control-custom" id="txtusername"/>
                      </div>
                      <div className="form-group">
                          <label>Password</label>
                          <input type="text" className="form-control form-control-custom" id="txtpassword"/>
                      </div>
                      <div style={{textAlign:"center"}}>
                        <button type="button" className="btn btn-custom btn-primary" onClick={login}>Log In</button>
                      </div>
                      <div id="loginAlert" className="alert alert-danger alert-danger-custom" role="alert" style={{marginTop:"10px",display:"none"}}></div>
                  </form>
              </div>
          </div>
      )
    }
}
