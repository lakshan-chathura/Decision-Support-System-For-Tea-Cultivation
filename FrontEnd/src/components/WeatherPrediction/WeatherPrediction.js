import React, { useState } from 'react'
import WeatherPredictionCard from './WeatherPredictionCard'
import brokenClouds from '../../asset/img/broken_clouds.png'
import clearSky from '../../asset/img/clear_sky.png'
import fewClouds from '../../asset/img/few_clouds.png'
import mist from '../../asset/img/mist.png'
import scatteredClouds from '../../asset/img/scattered_clouds.png'
import overcastClouds from '../../asset/img/overcast_clouds.png'
import showerRain from '../../asset/img/shower_rain.png'
import thunderStorm from '../../asset/img/thunderstorm.png'
import rain from '../../asset/img/rain.png'
import axios from 'axios'
import './WeatherPredictionCard.css'

export default function WeatherPrediction(props){
  const [weatherPredictionCards,setWeatherPredictionCards] = useState(null)
  const APIKey = 'e1d0f30e5b35130a4f48aab038559843'
  const cityID = '1246294'
  const url = 'http://api.openweathermap.org/data/2.5/forecast'

  function getWeatherData(){
    axios.get(url, {params: {
      id: cityID,
      appid: APIKey,
      units:'metric'
    }})
    .then((response) => {
      let weatherPredictionCardList = []
      console.log(response.data)
      for(let i=0;i<response.data.list.length;i+=8){
        let image = null
        let description = response.data.list[i].weather[0].description
        let date = response.data.list[i].dt_txt.split(' ')[0]
        let temperature = response.data.list[i].main.temp
        let humidity = response.data.list[i].main.humidity
        let id = response.data.list[i].weather[0].id

        switch(id){
          case 200:
          case 201:
          case 202:
          case 210:
          case 211:
          case 212:
          case 221:
          case 230:
          case 231:
          case 232:image = thunderStorm;break;
          case 300:
          case 301:
          case 302:
          case 310:
          case 311:
          case 312:
          case 313:
          case 314:
          case 321:image = 'drizzle';break;
          case 500:
          case 501:
          case 502:
          case 503:
          case 504:image = rain;break;
          case 511:
          case 520:
          case 521:
          case 522:
          case 531:image = showerRain;break;
          case 701:
          case 711:
          case 721:
          case 731:
          case 741:
          case 751:
          case 761:
          case 762:
          case 771:
          case 781:image = mist;break;
          case 800:image = clearSky;break;
          case 801:image = fewClouds;break;
          case 802:image = scatteredClouds;break;
          case 803:image = brokenClouds;break;
          case 804:image = overcastClouds;break;
          default:image = null;break;
        }

        let instruction = showInstructions(id)
        weatherPredictionCardList.push(
          <WeatherPredictionCard key={i} image={image} description={description}
            date={date} temp={temperature} humidity={humidity} instruction={instruction}/>
        )
      }

      console.log(weatherPredictionCards);

      if(weatherPredictionCards === null){
        setWeatherPredictionCards(weatherPredictionCardList)
      }
    }).catch((error) => {
      console.log(error)
    })
  }

  function showInstructions(weatherID){
    let instruction = ""
    switch(weatherID){
      case 200:
      case 201:
      case 202:
      case 210:
      case 211:
      case 212:
      case 221:
      case 230:
      case 231:
      case 232:
      case 500:
      case 501:
      case 502:
      case 503:
      case 504:
      case 511:
      case 520:
      case 521:
      case 522:
      case 531:instruction = "If atleast 50% of tea buds in the cultivation is suitable for plucking, do the pruning immediately.\
                             There is a possibility of loosing a considerable amount of harvest due to rain";break;
      case 800:instruction = "Take care about watering the plants.Sunlight might make the tea plants stressed";break;                       
      case 801:
      case 802:
      case 803:
      case 804:instruction = "low sunlight might result from clouds which affects negatively to the growing of tea buds.\
                              So the pruning might has to be done lately.";break;
      default:instruction = "Invalid weather code";break;
    }
    return instruction
  }
  getWeatherData()

  return(
    <div className="cardHolder">
      <h1>Weather Prediction For Next 5 Days</h1>
      <div style={{margin:"auto",position:"absolute",top:"15%"}}>
          {weatherPredictionCards}
      </div>
    </div>
  )
}
