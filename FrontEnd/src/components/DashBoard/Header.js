import React from 'react'
import { Link } from 'react-router-dom'

export default function Header(props){
    const routes = [
      {
        name:'Setup Projects',
        to:'/setup'
      },
      {
        name:'View Projects',
        to:'/viewer'
      },
      {
        name:'Weather Prediction',
        to:'/weatherprediction'
      }
    ]
    let navLinks = routes.map((item,i) => {
        if(props.current === item.to){
          return(
            <li key={i} className="nav-item active">
                <Link to={item.to} className="nav-link">{item.name}<span className="sr-only">(current)</span></Link>
            </li>
          )
        }
        else{
          return(
            <li key={i} className="nav-item">
                <Link to={item.to} className="nav-link">{item.name}<span className="sr-only">(current)</span></Link>
            </li>
          )
        }
    })

    function logOut(){
      localStorage.removeItem('loggedIn')
      alert('You have logged out successfully')
      props.setLoggedIn(false)
    }

    return(
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo03" aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
            </button>
            <Link className="navbar-brand" to='/'>D3STC</Link>

            <div className="collapse navbar-collapse" id="navbarTogglerDemo03">
                <ul className="navbar-nav mr-auto mt-2 mt-lg-0">
                    {navLinks}
                </ul>
                <ul className="navbar-nav">
                    <li className="nav-item">
                      <button className="btn btn-danger" onClick={logOut}>Log Out</button>
                        {/* <Link className="nav-link dropdown-toggle" to='/' id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Dropdown
                        </Link>
                        <div className="dropdown-menu dropdown-menu-right mr-sm-2" aria-labelledby="navbarDropdown">
                            <Link className="dropdown-item" to='/'>Action</Link>
                            <Link className="dropdown-item" to='/'>Another action</Link>
                            <div className="dropdown-divider"></div>
                            <Link className="dropdown-item" to='/'>Something else here</Link>
                        </div> */}
                    </li>
                </ul>
            </div>
        </nav>
    )
}
