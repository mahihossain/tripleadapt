import React, { useContext, useEffect, useState } from 'react'
import Navbar from './components/Navbar';
import * as FiIcons from "react-icons/fi"
import { UserContext } from '../context/UserContext';
import { Link, useNavigate } from "react-router-dom";
import './Analytics.css'
import axios from 'axios';
import { Card, Container, Row, Col, Table } from "react-bootstrap";
import { Line } from 'react-chartjs-2';
import Plot from 'react-plotly.js';

import * as FcIcons from "react-icons/fc";

function Analytics(props) {
  let navigate = useNavigate();
  const { user, setUser } = useContext(UserContext)
  const [label, setLabel] = useState([]);
  const [avgTime, setAvgTime] = useState([]);
  const [lastTime, setLastTime] = useState([])
  const [avgFailure, setAvgFailure] = useState([])
  const [lastFailure, setLastFailure] = useState([])
  const [avgScore, setAvgScore] = useState([])
  const [lastScore, setLastScore] = useState([])
  const [avgScoreHistory, setAvgScoreHistory] = useState([])
  const [avgFailureHistory, setAvgFailureHistory] = useState([])
  const [avgTimeHistory, setAvgTimeHistory] = useState([]);
  const [avgScoreAll, setAvgScoreAll] = useState([]);
  const [avgFailureAll, setAvgFailureAll] = useState([]);
  const [avgTimeAll, setAvgTimeAll] = useState([]);


  const namesList = {
    'Starten': 1,
    'Abschlussdeckel': 2,
    'Bundschrauben festdrehen': 3,
    'Kolbenstange': 4,
    'Kolbenbaugruppe': 5,
    'Mutter festdrehen': 6,
    'Kolbenstangenbaugruppe einsetzen': 7,
    'Lagerdeckel': 8,
    'Bundschrauben einsetzen': 9,
  }

  const Time1 = {
    x: label,
    y: lastTime,
    name: "Letzte Zeit",
    type: "bar",
    marker: {
      color: '#0bdbb0'
    }
  };

  const Time2 = {
    x: label,
    y: avgTime,
    name: "Ihr Durchschnitt",
    type: "bar",
    marker: {
      color: '#0091dc'
    }
  };

  const Time3 = {
    x: label,
    y: avgTimeAll,
    name: "Allg. Durchschnitt",
    type: "bar",
    marker: {
      color: '#FFFF00'
    }
  };

  const Failure1 = {
    x: label,
    y: lastFailure,
    name: "Letzte Fehleranzahl",
    type: "bar",
    marker: {
      color: '#0bdbb0'
    }
  };

  const Failure2 = {
    x: label,
    y: avgFailure,
    name: "Ihr Durchsch.",
    type: "bar",
    marker: {
      color: '#0091dc'
    }
  };

  const Failure3 = {
    x: label,
    y: avgFailureAll,
    name: "Allg. Durchsch.",
    type: "bar",
    marker: {
      color: '#FFFF00'
    }
  };

  const Score1 = {
    x: label,
    y: lastScore,
    name: "Letzter Score",
    type: "bar",
    marker: {
      color: '#0bdbb0'
    }
  };

  const Score2 = {
    x: label,
    y: avgScore,
    name: "Ihr Durchschnitt",
    type: "bar",
    marker: {
      color: '#0091dc'
    }
  };

  const Score3 = {
    x: label,
    y: avgScoreAll,
    name: "Allg. Durchschnitt",
    type: "bar",
    marker: {
      color: '#FFFF00'
    }
  };

  const Time = [Time1, Time2, Time3]
  const Failure = [Failure1, Failure2, Failure3]
  const Score = [Score1, Score2, Score3]

  useEffect(() => {
    // console.log(user)
    axios.post('/statistics', {
      userId: user.id,
      // userId: 0,
      userName: user.name,
      // userName: "Ingoi",
      DataID: ['task_names', 'avg_task_duration', 'history_of_specific_task_duration',
        'avg_failure_per_failure_category', 'failures_per_run', 'avg_score_tasks', 'score_per_run',
        'individual_average_completion_duration', 'individual_average_completion_failure', 'avg_score_history',
        'avg_score_all_user', 'avg_duration_all_user', 'avg_failure_all_user'],
    })
      .then(function (response) {
        // console.log(response.data);
        // console.log(response.data["score_per_run"])
        // console.log(Object.entries(response.data["score_per_run"]))
        console.log(response.data)
        for (const [key, value] of Object.entries(response.data["task_names"])) {
          setLabel((label) => [...label, value])
        }

        for (const [key, value] of Object.entries(response.data["avg_task_duration"])) {
          // console.log(key)
          // setLabel((label) => [...label, key])
          // console.log(value)
          setAvgTime((avgTime) => [...avgTime, value])
        }

        for (const [key, value] of Object.entries(response.data["history_of_specific_task_duration"])) {
          // console.log(key)
          // setLabel((label) => [...label, key])
          // console.log(value[value.length-1])
          setLastTime((lastTime) => [...lastTime, value[value.length - 1]])
        }

        for (const [key, value] of Object.entries(response.data["avg_failure_per_failure_category"])) {
          // console.log(key)
          // setLabel((label) => [...label, key])
          // console.log(value)
          setAvgFailure((avgFailure) => [...avgFailure, value])
        }

        for (const [key, value] of Object.entries(response.data["avg_score_all_user"])) {
          // console.log(key)
          // setLabel((label) => [...label, key])
          // console.log(value)
          if (key !== '0') {
            setAvgScoreAll((avgScoreAll) => [...avgScoreAll, value])
          }
        }

        for (const [key, value] of Object.entries(response.data["avg_duration_all_user"])) {
          // console.log(key)
          // setLabel((label) => [...label, key])
          // console.log(value)
          setAvgTimeAll((avgTimeAll) => [...avgTimeAll, value])
        }

        for (const [key, value] of Object.entries(response.data["avg_failure_all_user"])) {
          // console.log(key)
          // setLabel((label) => [...label, key])
          // console.log(value)
          setAvgFailureAll((avgFailureAll) => [...avgFailureAll, value])
        }

        setLastFailure(Object.entries(response.data["failures_per_run"])[Object.entries(response.data["failures_per_run"]).length - 1][1])

        response.data["avg_score_tasks"].shift()
        setAvgScore(response.data["avg_score_tasks"])

        Object.entries(response.data["score_per_run"])[Object.entries(response.data["score_per_run"]).length - 1][1].shift()
        setLastScore(Object.entries(response.data["score_per_run"])[Object.entries(response.data["score_per_run"]).length - 1][1])

        setAvgTimeHistory(response.data["individual_average_completion_duration"])
        setAvgFailureHistory(response.data["individual_average_completion_failure"])
        setAvgScoreHistory(response.data["avg_score_history"])


      })

  }, [])

  return (
    <>
      <Navbar />
      <Link className='profileStyle' style={{ cursor: 'pointer', textDecoration: 'none' }} to={'/UserPage'}>
        {user.name[0]}
      </Link>
      <div className='logoutStyle' style={{ cursor: 'pointer' }} onClick={() => window.location.href = '/'}> <FiIcons.FiLogOut /> </div>
      <div className='lastDataContainer'>
        <Card className='TimeHistogram'>
          <Plot
            className='PlotAutosize'
            data={Time}
            layout={{
              autosize: true,
              title: 'Zeit/Task',
              legend: {
                x: 0,
                y: 1.3,
                orientation: "h",
              },
              xaxis: {
                dtick: 1,
                // labelalias:{"Kolbenstangenbaugruppe einsetzen":'Kolbenstangenbaugruppe'},
                showticklabels: false
              },
              margin: {
                b: 10,
                l: 30,
                t: 0,
                r: 0,
                pad: 0
              },
              font: {
                size: 10,
                color: 'black'
              }
            }}
            // onClick={(event) => console.log(event)}
            onClick={(event) => navigate('/taskdata', {
              state: {
                TaskName: event.points[0].label,
                TaskList: label,
                IdList: namesList
              }
            })}
          />
        </Card>
        <Card className='FailureHistogram'>
          <Plot
            className='PlotAutosize'
            data={Failure}
            layout={{
              autosize: true,
              title: 'Fehler/Task',
              legend: {
                x: 0,
                y: 1.3,
                orientation: "h",
              },
              xaxis: {
                dtick: 1,
                showticklabels: false
              },
              margin: {
                b: 10,
                l: 30,
                t: 0,
                r: 0,
                pad: 0
              },
              font: {
                size: 10,
                color: 'black'
              }
            }}
            onClick={(event) => navigate('/taskdata', {
              state: {
                TaskName: event.points[0].label,
                TaskList: label,
                IdList: namesList
              }
            })}
          />
        </Card>
        <Card className='ScoreHistogram'>
          <Plot
            className='PlotAutosize'
            data={Score}
            layout={{
              autosize: true,
              title: 'Score/Task',
              legend: {
                x: 0,
                y: 1.3,
                orientation: "h",
              },
              xaxis: {
                dtick: 1,
                showticklabels: false
              },
              margin: {
                b: 10,
                l: 30,
                t: 0,
                r: 0,
                pad: 0
              },
              font: {
                size: 10,
                color: 'black'
              }
            }}
            onClick={(event) => navigate('/taskdata', {
              state: {
                TaskName: event.points[0].label,
                TaskList: label,
                IdList: namesList
              }
            })}
          />
        </Card>
        <Card className='ZeitAllgemein'>
          <Card.Body>
            <Row>
              <Col xs="4">
                <div className="AnalyticsIcon">
                  <FcIcons.FcClock size={'60%'} />
                </div>
              </Col>
              <Col xs="8">
                <Card.Title className='AnalyticsNumber'>
                  <div style={{ fontWeight: 'bold', color: 'grey' }}>
                    Zeit <br /><br />
                  </div>
                  {Math.floor(avgTimeHistory / 60)} min <br />
                  {Math.floor(avgTimeHistory % 60)} sek
                </Card.Title>
              </Col>
            </Row>
          </Card.Body>
          <Card.Footer>
            <hr></hr>
            <div className="stats">
              Durchschnitt pro Durchlauf
            </div>
          </Card.Footer>
        </Card>
        <Card className='FehlerAllgemein'>
          <Card.Body>
            <Row>
              <Col xs="4">
                <div className="AnalyticsIcon">
                  <FcIcons.FcHighPriority size={'60%'} />
                </div>
              </Col>
              <Col xs="8">
                <Card.Title className='AnalyticsNumber'>
                  <div style={{ fontWeight: 'bold', color: 'grey' }}>
                    Fehler <br /><br />
                  </div>
                  {Math.round(avgFailureHistory * 100 + Number.EPSILON) / 100} </Card.Title>
              </Col>
            </Row>
          </Card.Body>
          <Card.Footer>
            <hr></hr>
            <div className="stats">
              Durchschnitt pro Durchlauf
            </div>
          </Card.Footer>
        </Card>

        <Card className='ScoreAllgemein'>
          <Card.Body>
            <Row>
              <Col xs="4">
                <div className="AnalyticsIcon">
                  <FcIcons.FcInspection size={'60%'} />
                </div>
              </Col>
              <Col xs="8">
                <Card.Title className='AnalyticsNumber'>
                  <div style={{ fontWeight: 'bold', color: 'grey' }}>
                    Score <br /><br />
                  </div>
                  {Math.round(avgScoreHistory * 100 + Number.EPSILON) / 100}</Card.Title>
              </Col>
            </Row>
          </Card.Body>
          <Card.Footer>
            <hr></hr>
            <div className="stats">
              Durchschnitt pro Durchlauf
            </div>
          </Card.Footer>
        </Card>
      </div>
    </>
  )
}

export default Analytics