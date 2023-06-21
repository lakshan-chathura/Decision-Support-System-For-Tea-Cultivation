import React,{ useState } from 'react'
import axios from 'axios'
import './ProjectViewer.css'
import Modal from '../Modal/Modal'
import { Link } from 'react-router-dom'

export default function ProjectViewer(props){
  const [projectList,setProjectList] = useState(null)
  const BASE_URL = 'http://localhost:8000/api/'
  let tr = [],modals = []

  function prepareTable(){
    projectList.map((item,i) => {
      tr.push(<tr key={'row_' + i}>
                  <th scope={"row_" + item.project_data.real_name}>{i + 1}</th>
                  <td>{item.project_data.name}</td>
                  <td><Link className="btn btn-custom btn-primary" to={'mapper/' + item.project_data.real_name + '/rgb'} target='_blank'>Show</Link></td>
                  <td><Link className="btn btn-custom btn-primary" to={'mapper/' + item.project_data.real_name + '/ndvi'} target='_blank'>Show</Link></td>
                  <td><Link className="btn btn-custom btn-primary" to={'mapper/' + item.project_data.real_name +'/cluster'} target='_blank'>Show</Link></td>
                  <td><input type="button" data-toggle="modal" data-target={"#Modal_" + item.project_data.real_name} className="btn btn-custom btn-primary" value="show"/></td>
                </tr>)

      modals.push(<Modal key={'Modal_' + i} type='ndvi'title='NDVI Statistics' id={'Modal_' + item.project_data.real_name} nonPlantPercentage={Math.round(item.non_plants)} healthyPlantPercentage={Math.round(item.good_plant_health)} nonhealthyPlantPercentage={Math.round(item.bad_plant_health)}/>)
      return true
    })
  }

  function retrieveProjectData(){
    axios.get(BASE_URL + 'data/field').then((result) => {
      setProjectList(result.data.data)
    }).catch((error) => {
      console.log(error)
    })
  }

  if(projectList === null){
      retrieveProjectData()
  }
  else{
    prepareTable()
  }
  return(
    <div className="col-md-10 ProjectViewerFrame">
        <h1>Project List</h1>
        <hr/>
        <table className="table table-hover table-bordered">
          <thead>
            <tr>
              <th scope="col" >#</th>
              <th scope="col" >Project Name</th>
              <th scope="col" >RGB Map</th>
              <th scope="col" >NDVI Map</th>
              <th scope="col" >Cluster Map</th>
              <th scope="col" >Plant Health Stats</th>
            </tr>
          </thead>
          <tbody>
              {tr}
          </tbody>
        </table>
        {modals}
    </div>
  )
}
