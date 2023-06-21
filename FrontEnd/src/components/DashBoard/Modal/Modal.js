import React from 'react'
import Chart from './Chart/Chart'

export default function Modal(props){
  let body = null

  function setMap(e){
      props.setMap(e.target.value)
  }

  if (props.type === 'ndvi'){
    body = (
      <div className="row">
        <div className="col-md-7">
          <p className="p-custom">Non plant vegetation percentage&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:{props.nonPlantPercentage + '%'}</p>
          <p className="p-custom">Healthy plant vegetation percentage&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:{props.healthyPlantPercentage + '%'}</p>
          <p className="p-custom">Non healthy plant vegetation percentage  :{props.nonhealthyPlantPercentage + '%'}</p>
        </div>
        <div className="col-md-5">
          <Chart healthyPlants={props.healthyPlantPercentage} nonHealthyPlants={props.nonhealthyPlantPercentage} nonVegetatedArea={props.nonPlantPercentage}/>
        </div>
      </div>
    )
  }
  else if(props.type === 'map'){
    body = (
      <div className="row">
        <div className="col-md-7">
          <input onClick={setMap} type="radio" value='rgb' name='mapSelect'/><span style={{fontSize:'28px'}}>RGB Map</span><br/>
          <input onClick={setMap} type="radio" value='cluster' name='mapSelect'/><span style={{fontSize:'28px'}}>Cluster Map</span><br/>
          <input onClick={setMap} type="radio" value='ndvi' name='mapSelect'/><span style={{fontSize:'28px'}}>NDVI Map</span><br/>
        </div>
      </div>
    )
  }
  return(
    <div id={props.id}  className="modal fade" tabIndex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div className="modal-dialog modal-dialog-centered modal-xl" role="document">
        <div className="modal-content">
          <div className="modal-header">
            <h3 className="modal-title">{props.title}</h3>
            <button type="button" className="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div className="modal-body">
            {body}
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-secondary btn-secondary-custom" data-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
  )
}
