import React, { useState } from 'react'
import Modal from '../Modal/Modal'

export default function MapperPlain(props){
  const [mapType,setMapType] = useState(window.location.href.split('/')[5])
  const [projectName,setProjectName] = useState(window.location.href.split('/')[4])
  const [ndviLayerLevel,setNdviLayerLevel] = useState(7)

  let baseUrl = ""
  let ndvi_layer_chooser = null
  let mapLayers = []

  function selectNDVILayer(e){
      let items = document.getElementsByClassName('form-check-input')
      let ndviLayerLevel = 0

      for(let i=0;i<items.length;i++){
        if(items[i].checked === true){
          ndviLayerLevel += Math.pow(2,i)
        }
      }
      console.log(ndviLayerLevel)
      setNdviLayerLevel(ndviLayerLevel)
  }

  if(mapType === 'ndvi'){
    let colors = []

    if( ndviLayerLevel !== 0){
      mapLayers.push(
          <img src={"http://localhost/data/maps/" + mapType + "_maps/" + projectName + "/" + ndviLayerLevel + ".jpg"}
              alt="rgb_layer_map"
              style={{height:"100%",overflow:"scroll",zIndex:"2"}}
              role="presentation"/>
      )
    }

    let items = []
    switch(ndviLayerLevel){
      case 0:
        colors = [];
        items[0] = false;
        items[1] = false;
        items[2] = false;
        break;
      case 1:
        colors = ['blue'];
        items[0] = true;
        items[1] = false;
        items[2] = false;
        break;
      case 2:
        colors = ['green'];
        items[1] = true;
        items[2] = false;
        items[0] = false;
        break;
      case 3:
        colors = ['blue','green'];
        items[0] = true;
        items[1] = true;
        items[2] = false;
        break;
      case 4:
        colors = ['red'];
        items[2] = true;
        items[1] = false;
        items[0] = false;
        break;
      case 5:
        colors = ['blue','red'];
        items[2] = true;
        items[0] = true;
        items[1] = false;
        break;
      case 6:
        colors = ['red','green'];
        items[2] = true;
        items[1] = true;
        items[0] = false;
        break;
      case 7:
        colors = ['blue','red','green'];
        items[0] = true;
        items[1] = true;
        items[2] = true;
        break;
    }

    mapLayers.push(
      <img src={"http://localhost/data/maps/rgb_maps/" + projectName + "/rgb_map.png"}
           alt="map"
           style={{height:"100%",overflow:"scroll"}}
           role="presentation"/>
    )

    ndvi_layer_chooser = (<div className="col-md-3 ndviLayerSelection">
                            <div className="form-check">
                              <input type="checkbox" className="form-check-input" id="blue" onClick={selectNDVILayer} defaultChecked={items[0]}/>
                              <label className="form-check-label" for="exampleCheck1">Non vegetated areas</label>
                              <div style={{backgroundColor:"blue",width:"20px",height:"20px",marginLeft:"40%",display:"inline-flex"}}></div>
                            </div>
                            <div className="form-check">
                              <input type="checkbox" className="form-check-input" id="green" onClick={selectNDVILayer} defaultChecked={items[1]}/>
                              <label className="form-check-label" for="exampleCheck1">Areas with unhealthy Plants</label>
                              <div style={{backgroundColor:"red",width:"20px",height:"20px",marginLeft:"22%",display:"inline-flex"}}></div>
                            </div>
                            <div className="form-check">
                              <input type="checkbox" className="form-check-input" id="red" onClick={selectNDVILayer} defaultChecked={items[2]}/>
                              <label className="form-check-label" for="exampleCheck1">Areas with healthy Plants</label>
                              <div style={{backgroundColor:"green",width:"20px",height:"20px",marginLeft:"28.5%",display:"inline-flex"}}></div>
                            </div>
                          </div>)
  }
  else if(mapType === 'rgb' || mapType === 'nir'){
    mapLayers.push(
      <img src={"http://localhost/data/maps/" + mapType +"_maps/" + projectName + "/" + mapType + "_map.png"}
           alt="map"
           style={{height:"100%",overflow:"scroll"}}
           role="presentation"/>
    )
  }
  else if(mapType === 'cluster'){
    mapLayers.push(
      <img src={"http://localhost/data/maps/rgb_maps/" + projectName + "/modified/" + mapType + "_map.jpg"}
           alt="map"
           style={{height:"100%",overflow:"scroll"}}
           role="presentation"/>
    )
  }

  console.log(baseUrl)
  return(
    <div style={{backgroundColor:"white",height:"100%"}}>
      <input type="button" className='btn btn-default' value="Select Map Type" className='selectionPane' data-toggle="modal" data-target="#mapTypeSelectorModal"/>
      <Modal id='mapTypeSelectorModal' type='map' title="Select a Map Type" setMap={setMapType}/>
        {ndvi_layer_chooser}
        {mapLayers}
    </div>
  )
}
