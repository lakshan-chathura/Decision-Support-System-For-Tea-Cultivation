import React from 'react'
import './WeatherPredictionCard.css'

export default function WeatherPredictionCard(props){
  return(
    <div className="card col-md-2 col-md-2-custom" style={{width: "28rem",display:"inline-flex",margin:"5px"}}>
      <div className="card-header card-header-custom">
        {props.date}
      </div>
      <img src={props.image} className="card-img-top" alt="..." height={240} width={100}/>
      <div className="card-body">
        <h5 className="card-title card-title-custom">{props.description}</h5>
        <p className="card-text card-text-custom" style={{textAlign:"justify",minHeight:"280px"}}>{props.instruction}</p>
      </div>
      <ul className="list-group list-group-flush">
        <li className="list-group-item list-group-item-custom">{'Temperature : ' + props.temp + '\u00b0C'}</li>
        <li className="list-group-item list-group-item-custom">{'Humidity : ' + props.humidity + ' RH%'}</li>
      </ul>
    </div>
  )
}
