import React, { useContext, useState } from 'react';
import ReactPlayer from "react-player";
import './Sensor.css'
import { UserContext } from '../context/UserContext';
import { Link } from "react-router-dom";
import * as FiIcons from "react-icons/fi"
import * as BsIcons from "react-icons/bs"
import { Card } from "react-bootstrap";
import { Line } from 'react-chartjs-2';
import Plot from 'react-plotly.js';
import video from '../images/video.mp4';

function Sensor(props) {

    const {user, setUser} = useContext(UserContext)

    const [videoFilePath, setVideoFilePath] = useState(null);

    const handleVideoUpload = (event) => {
      setVideoFilePath(URL.createObjectURL(event.target.files[0]));
    };

    return (
        <>
            
            <div className='video'>
              {/* <ReactPlayer src={video} width="90%" height="90%" controls={true} /> */}
              <video   src={video}
                position="absolute!important"
                width="100%" 
                height="100%"
                autoPlay
                // controls
                muted
                disablePictureInPicture
                loop
                >
              </video>
            </div>

            <Card className='sensordata'>
              <Line 
                  data={{
                    labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                    datasets: [
                      {
                        label: 'Datensatz 1',
                        data: [0, 0.4, 0.6, -0.65, 0.6, -0.5, -0.25, -0.15, 0.3, 1.05, 2.6, 1.1, -0.4, 0.5, 0.8],
                        borderColor: 'rgb(53, 162, 235)',
                        backgroundColor: 'rgba(53, 162, 235, 0.5)',
                      },
                      {
                        label: '0 Linie',
                        data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        borderColor: 'red',
                        backgroundColor: 'red',
                      }
                  ]
                  }}
                  options={{
                    indexAxis: 'x',
                    pointBorderWidth: 0,
                    pointRadius: 0,
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: 'Sensor Daten',
                        },
                    },
                  }} 
                />
            </Card>
            {/* <Card className='plot'> */}
              <Plot 
                className='plot'
                data={[
                    {
                        x: [40],
                        y: [-20],
                        z: [-40],
                        type: 'scatter3d',
                        mode: 'markers',
                        marker: {color: 'red'},
                        name: 'initiale Position'
                    },
                    {
                      x: [35],
                      y: [-30],
                      z: [-45],
                      type: 'scatter3d',
                      mode: 'markers',
                      marker: {color: 'blue'},
                      name: 'aktuelle Position'
                  }
                ]}
                layout = {{
                  legend: {
                    x: 0.7,
                    y: 0.9
                  },
                  margin: {
                    autoexpand: true,
                    b: 20,
                    l: 0,
                    t: 0,
                    r: 0,
                    pad: 80
                  }

                }
                  // 'zaxis': {
                  //   'range': [-40, 40]
                  // },
                  // 'xaxis': {
                  //   'range': [-40, 40]
                  // },
                  // 'yaxis': {
                  //   'range': [-40, 40]
                  // },
                }
              />
            {/* </Card> */}
            <Link className='profileStyle_sensor' style={{cursor: 'pointer', textDecoration: 'none'}} to={'/UserPage'}>
                {user.name[0]}
            </Link>
            <div className='logoutStyle_sensor' style={{cursor: 'pointer'}} onClick={event => window.location.href='/'}> <FiIcons.FiLogOut/> </div>
            <Link className='Back_sensor' style={{cursor: 'pointer', textDecoration: 'none'}} to={'/'}> <BsIcons.BsBackspaceFill/> </Link>
        </>
    )
}

export default Sensor;