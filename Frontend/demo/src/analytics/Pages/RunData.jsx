import React, { useContext, useEffect, useState } from 'react'
import Navbar from '../components/Navbar';
import * as FiIcons from "react-icons/fi"
import * as FcIcons from "react-icons/fc";
import { UserContext } from '../../context/UserContext';
import { Link, useNavigate } from "react-router-dom";
import './RunData.css'
import axios from 'axios';
import { Card, Container, Row, Col, Table } from "react-bootstrap";
import Plot from 'react-plotly.js';

function RunData(props) {
    let navigate = useNavigate();
    const { user, setUser } = useContext(UserContext)
    const [timePerRun, setTimePerRun] = useState([])
    const [failurePerRun, setFailurePerRun] = useState([])
    const [scorePerRun, setScorePerRun] = useState([])
    const [label, setLabel] = useState([]);
    const [sumTime, setSumTime] = useState(0)
    const [sumFailure, setSumFailure] = useState(0)
    const [sumScore, setSumScore] = useState(0)
    const [current, setCurrent] = useState(0);
    const [instances, setInstances] = useState([])

    var Time = {
        x: label,
        y: timePerRun,
        name: "Zeiten des Durchlaufs",
        type: "bar",
        marker: {
            color: '#0091dc'
        }
    }

    const Failure = {
        x: label,
        y: failurePerRun,
        name: "Fehler des Durchlaufs",
        type: "bar",
        marker: {
            color: '#0091dc'
        }
    };

    const Score = {
        x: label,
        y: scorePerRun,
        name: "Score des Durchlaufs",
        type: "bar",
        marker: {
            color: '#0091dc'
        }
    };

    useEffect(() => {
        axios.post('/statistics', {
            userId: user.id,
            // userId: 0,
            userName: user.name,
            // userName: "Ingoi",
            DataID: ['task_names', 'failures_per_run', 'durations_per_run', 'score_per_run']
        })
            .then(function (response) {
                let last_item = Object.keys(response.data['durations_per_run'])[Object.keys(response.data['durations_per_run']).length - 1]
                setCurrent(last_item)
                let sumTime = 0
                let sumFailure = 0
                let sumScore = 0

                setInstances([])

                for (const [key, value] of Object.entries(response.data['task_names'])) {
                    setLabel((label) => [...label, value])
                }

                for (const [key, value] of Object.entries(response.data['durations_per_run'])) {
                    setInstances((instances) => [...instances, key])
                }

                for (const [key, value] of Object.entries(response.data['durations_per_run'][last_item])) {
                    // setLabel((label) => [...label, Number(key)+ 1])
                    sumTime = sumTime + Number(value)
                    setSumTime(sumTime)
                }

                for (const [key, value] of Object.entries(response.data['failures_per_run'][last_item])) {
                    sumFailure = sumFailure + Number(value)
                    setSumFailure(sumFailure)
                }

                for (const [key, value] of Object.entries(response.data['score_per_run'][last_item])) {
                    sumScore = sumScore + Number(value)
                    setSumScore(sumScore)
                    if (key !== '0') {
                        setScorePerRun((score) => [...score, value])
                    }
                }

                setTimePerRun(response.data['durations_per_run'][last_item])
                setFailurePerRun(response.data['failures_per_run'][last_item])
            })
    }, [])

    const handleChange = (event) => {
        setCurrent(instances[event.target.selectedIndex])
        setScorePerRun([])

        axios.post('/statistics', {
            userId: user.id,
            // userId: 0,
            userName: user.name,
            // userName: "Ingoi",
            DataID: ['failures_per_run', 'durations_per_run', 'score_per_run']
        })
            .then(function (response) {
                // console.log(instances[event.target.selectedIndex])
                // let last_item = Object.keys(response.data['durations_per_run'])[Object.keys(response.data['durations_per_run']).length-1]
                setCurrent(instances[event.target.selectedIndex])
                let sumTime = 0
                let sumFailure = 0
                let sumScore = 0

                for (const [key, value] of Object.entries(response.data['durations_per_run'][instances[event.target.selectedIndex]])) {
                    sumTime = sumTime + Number(value)
                    setSumTime(sumTime)
                }

                for (const [key, value] of Object.entries(response.data['failures_per_run'][instances[event.target.selectedIndex]])) {
                    sumFailure = sumFailure + Number(value)
                    setSumFailure(sumFailure)
                }

                for (const [key, value] of Object.entries(response.data['score_per_run'][instances[event.target.selectedIndex]])) {
                    sumScore = sumScore + Number(value)
                    setSumScore(sumScore)
                    if (key !== '0') {
                        setScorePerRun((score) => [...score, value])
                    }

                }

                setTimePerRun(response.data['durations_per_run'][instances[event.target.selectedIndex]])
                setFailurePerRun(response.data['failures_per_run'][instances[event.target.selectedIndex]])
                // setScorePerRun(response.data['score_per_run'][instances[event.target.selectedIndex]])
            })
    };

    return (
        <>
            <Navbar />
            <Link className='profileStyle' style={{ cursor: 'pointer', textDecoration: 'none' }} to={'/UserPage'}>
                {user.name[0]}
            </Link>
            <div className='logoutStyle' style={{ cursor: 'pointer' }} onClick={() => window.location.href = '/'}> <FiIcons.FiLogOut /> </div>
            <label className='instances'>
                <select value={current} onChange={handleChange}>
                    {instances.map(i => (
                        <option value={i}>{i}</option>
                    ))}
                </select>
            </label>
            <div className='connectReplay' style={{ cursor: 'pointer' }} onClick={(event) => navigate('/replay', {
                state: {
                    RunName: current,
                }
            })}>
                Durchlauf in Replay Page
            </div>
            <div className='RunDataContainer'>
                <Card className='ZeitRun'>
                    <Plot
                        className='PlotAutosize'
                        data={[Time]}
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
                                showticklabels: false
                            },
                            margin: {
                                b: 10,
                                l: 30,
                                t: 30,
                                r: 0,
                                pad: 0
                            },
                            font: {
                                size: 10,
                                color: 'black'
                            }
                        }}
                    />
                </Card>
                <Card className='FailureRun'>
                    <Plot
                        className='PlotAutosize'
                        data={[Failure]}
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
                                t: 30,
                                r: 0,
                                pad: 0
                            },
                            font: {
                                size: 10,
                                color: 'black'
                            }
                        }} />
                </Card>
                <Card className='ScoreRun'>
                    <Plot
                        className='PlotAutosize'
                        data={[Score]}
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
                                t: 30,
                                r: 0,
                                pad: 0
                            },
                            font: {
                                size: 10,
                                color: 'black'
                            }
                        }} />
                </Card>
                <Card className='TimeAvg'>
                    <Card.Body>
                        <Row>
                            <Col xs="4">
                                <div className="RunIcon">
                                    <FcIcons.FcClock size={'60%'} />
                                </div>
                            </Col>
                            <Col xs="8">
                                <Card.Title className='RunNumber'>
                                    <div style={{ fontWeight: 'bold', color: 'grey' }}>
                                        Zeit <br /><br />
                                    </div>
                                    {Math.floor(sumTime / label.length / 60)} min <br />
                                    {Math.floor((sumTime / label.length) % 60)} sek
                                </Card.Title>
                            </Col>
                        </Row>
                    </Card.Body>
                    <Card.Footer>
                        <hr></hr>
                        <div className="stats">
                            Durchschnitt pro Task
                        </div>
                    </Card.Footer>
                </Card>
                <Card className='FailureAvg'>
                    <Card.Body>
                        <Row>
                            <Col xs="4">
                                <div className="RunIcon">
                                    <FcIcons.FcHighPriority size={'60%'} />
                                </div>
                            </Col>
                            <Col xs="8">
                                <Card.Title className='RunNumber'>
                                    <div style={{ fontWeight: 'bold', color: 'grey' }}>
                                        Fehler <br /><br />
                                    </div>
                                    {Math.round(sumFailure / label.length * 100 + Number.EPSILON) / 100} </Card.Title>
                            </Col>
                        </Row>
                    </Card.Body>
                    <Card.Footer>
                        <hr></hr>
                        <div className="stats">
                            Durchschnitt pro Task
                        </div>
                    </Card.Footer>
                </Card>
                <Card className='ScoreAvg'>
                    <Card.Body>
                        <Row>
                            <Col xs="4">
                                <div className="RunIcon">
                                    <FcIcons.FcInspection size={'60%'} />
                                </div>
                            </Col>
                            <Col xs="8">
                                <Card.Title className='RunNumber'>
                                    <div style={{ fontWeight: 'bold', color: 'grey' }}>
                                        Score <br /><br />
                                    </div>
                                    {Math.round(sumScore / label.length * 100 + Number.EPSILON) / 100} </Card.Title>
                            </Col>
                        </Row>
                    </Card.Body>
                    <Card.Footer>
                        <hr></hr>
                        <div className="stats">
                            Durchschnitt pro Task
                        </div>
                    </Card.Footer>
                </Card>
            </div>
        </>
    )
}

export default RunData