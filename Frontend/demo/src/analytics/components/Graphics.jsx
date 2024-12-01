import axios from 'axios';
import React, { Component, useState } from 'react';
import '../Analytics.css'
import { Card } from '@mui/material';
import Chart from './Chart'

import { Chart as ChartJS } from 'chart.js/auto'
import { Bar } from 'react-chartjs-2'
import { useEffect } from 'react';


function Graphics(props) {
    const [dataset, setDataset] = useState([]);
    const [label, setLabel] = useState([]);
    const [daten, setDaten] = useState([]);

    useEffect(() => {
        axios.get('/graphics').then(data => {
            console.log('Graphics')
            console.log(data.data)
            Object.keys(data.data['failure one cat all iterations']).map((index) => {
                setDataset((dataset) => [...dataset, data.data['failure one cat all iterations'][index]])
                setLabel((label) => [...label, index])
            })
        })
    }, [])

    return (

        <>
        <div className='diagram'>
            {/* <Chart /> */}
            <Bar
                data= {{
                    labels: label,
                    datasets: [
                        {
                            label: '# of Errors',
                            data: dataset,
                            backgroundColor: [
                                'rgba(255, 99, 132, 0.2)',
                                'rgba(54, 162, 235, 0.2)',
                                'rgba(255, 206, 86, 0.2)',
                                'rgba(75, 192, 192, 0.2)',
                                'rgba(153, 102, 255, 0.2)',
                                'rgba(255, 159, 64, 0.2)'
                            ],
                            borderColor: [
                                'rgba(255, 99, 132, 1)',
                                'rgba(54, 162, 235, 1)',
                                'rgba(255, 206, 86, 1)',
                                'rgba(75, 192, 192, 1)',
                                'rgba(153, 102, 255, 1)',
                                'rgba(255, 159, 64, 1)'
                            ],
                            borderWidth: 1
                        },
                    ]
                }}
                height= {400}
                width= {600}
                options= {{
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }}
            />
        </div>
        </>
    );
}

export default Graphics;
