import React,{ useState } from 'react'
import { BrowserRouter as Router,Route,Switch} from 'react-router-dom'
import Login from './Login/Login'
import DashBoard from './DashBoard/DashBoard';
import ErrorPage from './ErrorPage/ErrorPage';
import Mapper from './DashBoard/Mapper/Mapper';
import ProjectSetup from './DashBoard/ProjectSetup/ProjectSetup'
import ProjectViewer from './DashBoard/ProjectViewer/ProjectViewer'
import WeatherPrediction from './WeatherPrediction/WeatherPrediction'
import MapperPlain from './DashBoard/Mapper/MapperPlain'

export default function Main(){
    let [loggedIn,setLoggedIn] = useState(false)

    const routes = [
        {
            'path':'/',
            'render':<Login loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>
        },
        {
            'path':'/mapper_geotile_foreign/:projectId/:mapType',
            'render':<DashBoard sideComponent={<Mapper lat={41.30417958333333} lon={-81.7524315}/>} to='/' loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>,
            'redirect':'/'
        },
        {
            'path':'/mapper_geotile_local/:projectId/:mapType',
            'render':<DashBoard sideComponent={<Mapper  lat={6.149839} lon={80.270819}/>} to='/' loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>,
            'redirect':'/'
        },
        {
            'path':'/mapper/:projectId/:mapType',
            'render':<DashBoard sideComponent={<MapperPlain/>} to='/' loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>,
            'redirect':'/'
        },
        {
            'path':'/setup',
            'render':<DashBoard sideComponent={<ProjectSetup/>} to='/' loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>,
            'redirect':'/'
        },
        {
            'path':'/viewer',
            'render':<DashBoard sideComponent={<ProjectViewer/>} to='/' loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>,
            'redirect':'/'
        },
        {
            'path':'/weatherprediction',
            'render':<DashBoard sideComponent={<WeatherPrediction/>} to='/' loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>,
            'redirect':'/'
        }
    ]

    return(
        <Router>
          <Switch>
              {
                  routes.map((item,i) => {
                          return <Route key={i} path={item.path} exact strict render = {() => (item.render)}/>
                  })
              }
            <Route render = {() => <ErrorPage/>}/>
          </Switch>
        </Router>
    )
}
