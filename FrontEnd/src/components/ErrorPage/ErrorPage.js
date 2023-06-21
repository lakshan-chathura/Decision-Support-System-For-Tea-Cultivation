import React from 'react'
import { Link } from 'react-router-dom'
import "./ErrorPage.css"
import errorImage from './2417237.jpg'

export default function ErrorPage(){
    return(
        <div className="errorPageBackground">
          <div style={{height:"80%"}}>
            <img src={errorImage} alt="error" height="80%" style={{position:"absolute",left:"20%"}}/>
          </div>
          <Link style={{color:"#FEC200",textDecoration:"none"}} href="https://www.freepik.com/free-photos-vectors/business">Business vector created by pikisuperstar - www.freepik.com</Link>
          <Link to="/" className="btn btn-primary" style={{position:"absolute",left:"44%"}}>Go back to home page</Link>
        </div>
    )
}
