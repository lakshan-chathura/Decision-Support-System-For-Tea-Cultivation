import React, { useState, useEffect } from 'react'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import { Map, TileLayer, Marker, Popup } from 'react-leaflet'
import './mapper.css'
import Modal from '../Modal/Modal'

export default function Mapper(props){
  const [lat,setLat] = useState(props.lat)/*(6.149839)*//*(41.30417958333333)*/
  const [lng,setLng] = useState(props.lon)/*(80.270819)*//*(-81.7524315)*/
  const [zoom,setZoom] = useState(20)
  const [mapType,setMapType] = useState(window.location.href.split('/')[5])
  const [projectName,setProjectName] = useState(window.location.href.split('/')[4])
  const [ndviLayerLevel,setNdviLayerLevel] = useState(7)

  var myIcon = L.icon({
    iconUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAApCAYAAADAk4LOAAAFgUlEQVR4Aa1XA5BjWRTN2oW17d3YaZtr2962HUzbDNpjszW24mRt28p47v7zq/bXZtrp/lWnXr337j3nPCe85NcypgSFdugCpW5YoDAMRaIMqRi6aKq5E3YqDQO3qAwjVWrD8Ncq/RBpykd8oZUb/kaJutow8r1aP9II0WmLKLIsJyv1w/kqw9Ch2MYdB++12Onxee/QMwvf4/Dk/Lfp/i4nxTXtOoQ4pW5Aj7wpici1A9erdAN2OH64x8OSP9j3Ft3b7aWkTg/Fm91siTra0f9on5sQr9INejH6CUUUpavjFNq1B+Oadhxmnfa8RfEmN8VNAsQhPqF55xHkMzz3jSmChWU6f7/XZKNH+9+hBLOHYozuKQPxyMPUKkrX/K0uWnfFaJGS1QPRtZsOPtr3NsW0uyh6NNCOkU3Yz+bXbT3I8G3xE5EXLXtCXbbqwCO9zPQYPRTZ5vIDXD7U+w7rFDEoUUf7ibHIR4y6bLVPXrz8JVZEql13trxwue/uDivd3fkWRbS6/IA2bID4uk0UpF1N8qLlbBlXs4Ee7HLTfV1j54APvODnSfOWBqtKVvjgLKzF5YdEk5ewRkGlK0i33Eofffc7HT56jD7/6U+qH3Cx7SBLNntH5YIPvODnyfIXZYRVDPqgHtLs5ABHD3YzLuespb7t79FY34DjMwrVrcTuwlT55YMPvOBnRrJ4VXTdNnYug5ucHLBjEpt30701A3Ts+HEa73u6dT3FNWwflY86eMHPk+Yu+i6pzUpRrW7SNDg5JHR4KapmM5Wv2E8Tfcb1HoqqHMHU+uWDD7zg54mz5/2BSnizi9T1Dg4QQXLToGNCkb6tb1NU+QAlGr1++eADrzhn/u8Q2YZhQVlZ5+CAOtqfbhmaUCS1ezNFVm2imDbPmPng5wmz+gwh+oHDce0eUtQ6OGDIyR0uUhUsoO3vfDmmgOezH0mZN59x7MBi++WDL1g/eEiU3avlidO671bkLfwbw5XV2P8Pzo0ydy4t2/0eu33xYSOMOD8hTf4CrBtGMSoXfPLchX+J0ruSePw3LZeK0juPJbYzrhkH0io7B3k164hiGvawhOKMLkrQLyVpZg8rHFW7E2uHOL888IBPlNZ1FPzstSJM694fWr6RwpvcJK60+0HCILTBzZLFNdtAzJaohze60T8qBzyh5ZuOg5e7uwQppofEmf2++DYvmySqGBuKaicF1blQjhuHdvCIMvp8whTTfZzI7RldpwtSzL+F1+wkdZ2TBOW2gIF88PBTzD/gpeREAMEbxnJcaJHNHrpzji0gQCS6hdkEeYt9DF/2qPcEC8RM28Hwmr3sdNyht00byAut2k3gufWNtgtOEOFGUwcXWNDbdNbpgBGxEvKkOQsxivJx33iow0Vw5S6SVTrpVq11ysA2Rp7gTfPfktc6zhtXBBC+adRLshf6sG2RfHPZ5EAc4sVZ83yCN00Fk/4kggu40ZTvIEm5g24qtU4KjBrx/BTTH8ifVASAG7gKrnWxJDcU7x8X6Ecczhm3o6YicvsLXWfh3Ch1W0k8x0nXF+0fFxgt4phz8QvypiwCCFKMqXCnqXExjq10beH+UUA7+nG6mdG/Pu0f3LgFcGrl2s0kNNjpmoJ9o4B29CMO8dMT4Q5ox8uitF6fqsrJOr8qnwNbRzv6hSnG5wP+64C7h9lp30hKNtKdWjtdkbuPA19nJ7Tz3zR/ibgARbhb4AlhavcBebmTHcFl2fvYEnW0ox9xMxKBS8btJ+KiEbq9zA4RthQXDhPa0T9TEe69gWupwc6uBUphquXgf+/FrIjweHQS4/pduMe5ERUMHUd9xv8ZR98CxkS4F2n3EUrUZ10EYNw7BWm9x1GiPssi3GgiGRDKWRYZfXlON+dfNbM+GgIwYdwAAAAASUVORK5CYII=',
    iconSize: [25, 41],
    iconAnchor: [12.5, 41],
    popupAnchor: [0, -41]
  });

    useEffect(()=>{
      // console.log(window.location.href.split('/'))
      // getLocation()
    },[])

    function selectNDVILayer(e){
        let items = document.getElementsByClassName('form-check-input')
        let ndviLayerLevel = 0

        for(let i=0;i<items.length;i++){
          if(items[i].checked === true){
            ndviLayerLevel += Math.pow(2,i)
          }
        }
        setNdviLayerLevel(ndviLayerLevel)
    }

    function getLocation() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition ((position) => {
          console.log(position)
          setLat(position.coords.latitude)
          setLng(position.coords.longitude)
        })
      } else {
        alert("Geolocation is not supported by this browser.")
      }
    }

    let mapUrl = ""

    const position = [lat, lng]
    let ndvi_layer_chooser = null
    let tileLayer = []

    if(mapType === 'ndvi'){
      let colors = []

      switch(ndviLayerLevel){
        case 1:colors = ['blue'];break;
        case 2:colors = ['green'];break;
        case 3:colors = ['blue','green'];break;
        case 4:colors = ['red'];break;
        case 5:colors = ['blue','red'];break;
        case 6:colors = ['red','green'];break;
        case 7:colors = ['blue','red','green'];break;
      }

      let items = []
      for(let i=0;i<colors.length;i++){
        switch (colors[i]) {
          case 'blue':
            tileLayer.push(<TileLayer key={'ndvi_blue_map'}
                            attribution='custom tiles'
                            url={"http://localhost/data/maps/" + mapType +"_maps/" + projectName + "/ndvi_map_final_blue_layer/{z}/{x}/{y}.png"}
                            minZoom={20}
                            maxZoom={22}
                            tms={true}
                            zIndex={3}
                            />)
            items[0] = true
            break;
          case 'green':
            tileLayer.push(<TileLayer key={'ndvi_green_map'}
                            attribution='custom tiles'
                            url={"http://localhost/data/maps/" + mapType +"_maps/" + projectName + "/ndvi_map_final_green_layer/{z}/{x}/{y}.png"}
                            minZoom={20}
                            maxZoom={22}
                            tms={true}
                            zIndex={3}
                            />)
            items[1] = true
            break;
          case 'red':
            tileLayer.push(<TileLayer key={'ndvi_red_map'}
                            attribution='custom tiles'
                            url={"http://localhost/data/maps/" + mapType +"_maps/" + projectName + "/ndvi_map_final_red_layer/{z}/{x}/{y}.png"}
                            minZoom={20}
                            maxZoom={22}
                            tms={true}
                            zIndex={3}
                            />)
            items[2] = true
            break;
        }
      }
      tileLayer.push(<TileLayer key={'rgb_map'}
                      attribution='custom tiles'
                      url={"http://localhost/data/maps/rgb_maps/" + projectName + "/rgb_map_final/{z}/{x}/{y}.png"}
                      minZoom={20}
                      maxZoom={22}
                      tms={true}
                      zIndex={2}
                      />)
      ndvi_layer_chooser = (<div className="col-md-2 ndviLayerSelection">
                              <div class="form-check">
                                <input type="checkbox" class="form-check-input" id="blue" onClick={selectNDVILayer} checked={items[0]}/>
                                <label class="form-check-label" for="exampleCheck1">Non vegetated areas</label>
                              </div>
                              <div class="form-check">
                                <input type="checkbox" class="form-check-input" id="green" onClick={selectNDVILayer} checked={items[1]}/>
                                <label class="form-check-label" for="exampleCheck1">Areas with healthy Plants</label>
                              </div>
                              <div class="form-check">
                                <input type="checkbox" class="form-check-input" id="red" onClick={selectNDVILayer} checked={items[2]}/>
                                <label class="form-check-label" for="exampleCheck1">Areas with Unhealthy Plants</label>
                              </div>
                            </div>)
    }
    else if(mapType === 'rgb' || mapType === 'nir'){
      tileLayer.push(<TileLayer
                         attribution='custom tiles'
                         url={"http://localhost/data/maps/" + mapType +"_maps/" + projectName + "/" + mapType + "_map_final/{z}/{x}/{y}.png"}
                         minZoom={20}
                         maxZoom={22}
                         tms={true}
                      />)
    }
    else if(mapType === 'cluster'){
      tileLayer.push(<TileLayer key={'rgb_map'}
                         attribution='custom tiles'
                         url={"http://localhost/data/maps/rgb_maps/" + projectName + "/modified/rgb_processed/{z}/{x}/{y}.png"}
                         minZoom={20}
                         maxZoom={22}
                         tms={true}
                         zIndex={3}
                      />)
      tileLayer.push(<TileLayer key={'cluster_map'}
                         attribution='custom tiles'
                         url={"http://localhost/data/maps/rgb_maps/" + projectName + "/rgb_map_final/{z}/{x}/{y}.png"}
                         minZoom={20}
                         maxZoom={22}
                         tms={true}
                         zIndex={2}
                      />)
    }

    return (
      <div style={{height:"100%"}}>
        <Map className="map" center={position} zoom={zoom} style={{paddingTop:'0vh'}}>
            <TileLayer
             attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
             url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {tileLayer}
          <Marker icon={myIcon} position={position}>
            <Popup>
              A pretty CSS3 popup. <br /> Easily customizable.
            </Popup>
          </Marker>
        </Map>
        <input type="button" className='btn btn-default' value="Select Map Type" className='selectionPane' data-toggle="modal" data-target="#mapTypeSelectorModal"/>
        <Modal id='mapTypeSelectorModal' type='map' title="Select a Map Type" setMap={setMapType}/>
        {ndvi_layer_chooser}
      </div>
    );
}
