import React from 'react';
import {Pie} from 'react-chartjs-2';

export default function Chart(props){
  const data = {
	labels: [
		'Healthy Plants',
		'Non Healthy Plants',
		'Non Vegetated Area'
	],
	datasets: [{
		data: [props.healthyPlants, props.nonHealthyPlants, props.nonVegetatedArea],
		backgroundColor: [
		'#FF6384',
		'#36A2EB',
		'#FFCE56'
		],
		hoverBackgroundColor: [
		'#FF6384',
		'#36A2EB',
		'#FFCE56'
		]
	}]
};

    return (
      <div>
        <Pie data={data}/>
      </div>
    );
}
