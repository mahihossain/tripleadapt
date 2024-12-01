import React, { useContext, useEffect, useState } from 'react'
import Graphics from '../components/Graphics';
import Navbar from '../components/Navbar';
import * as FiIcons from "react-icons/fi"
import { UserContext } from '../../context/UserContext';
import { Link } from "react-router-dom";
import './History.css'
import { Card, Container, Row, Col, Table } from "react-bootstrap";
import Plot from 'react-plotly.js';
import axios from 'axios';

function History() {

  const {user, setUser} = useContext(UserContext)
  const [alltime, setAllTime] = useState([])
  const [label, setLabel] = useState([]);

  const AllTime = {
    x: label,
    y: alltime,
    name: "Gesamtzeit",
    type: "bar",
  };

  useEffect(() => {
    console.log(user)
    axios.post('/statistics', {
     userId: user.id,
      // userId: 0,
      userName: user.name,
      // userName: "Ingoi",
      //DataID vereinbaren wie gewollte Daten verständigt werden
      DataID: ['avg_task_duration', 'all_taskdurations_all_iterations', 'avg_failure_per_failure_category'],
    })
    .then(function (response) {
      //Als response dann die genauen Daten zur Person
      console.log(response.data["all_taskdurations_all_iterations"]);
      Object.keys(response.data["all_taskdurations_all_iterations"]).map((index) => {
        setAllTime((allTime) => [...allTime, response.data["all_taskdurations_all_iterations"][index][0]])
        setLabel((label) => [...label, String(index)])
      })
      // setLabel(label.reverse())
      // console.log(label)
    })

  }, [])

  return (
    <>
        <Navbar/>
        <Link className='profileStyle' style={{cursor: 'pointer', textDecoration: 'none'}} to={'/UserPage'}>
            {/* {user.name[0]} */}
        </Link>
        <div className='logoutStyle' style={{cursor: 'pointer'}} onClick={event => window.location.href='/'}> <FiIcons.FiLogOut/> </div>                
        <div className='historyContainer'>
          <Card className='Gesamtzeit'>
              <Plot
                data={[AllTime]}
                layout={ {width: 850, height: 200, title: 'Gesamtzeit', 
                  legend: {
                    x: 0,
                    y: 1.3,
                    orientation: "h",
                  },
                  xaxis: {
                    dtick:1
                  },
                  margin: {
                    b: 50,
                    l: 40,
                    t: 40,
                    r: 0,
                    pad: 0
                    }
                }} />
          </Card>
        </div>
    </>
  )
}

export default History