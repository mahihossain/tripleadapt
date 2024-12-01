import React, { Component, useState, useContext, useEffect } from 'react';
import './Teacher.css'
import * as FiIcons from "react-icons/fi"
import * as FcIcons from "react-icons/fc";
import { Link, useNavigate } from "react-router-dom";
import { Card, Container, Row, Col, Table } from "react-bootstrap";
import Plot from 'react-plotly.js';
import axios from 'axios';


function Teacher(props) {
    let navigate = useNavigate();
    const [current, setCurrent] = useState({});
    const [user, setUser] = useState([])

    const [label, setLabel] = useState([]);

    const [avgTime, setAvgTime] = useState([]);
    const [lastTime, setLastTime] = useState([]);
    const [avgTimeAll, setAvgTimeAll] = useState([]);

    const [avgFailure, setAvgFailure] = useState([]);
    const [lastFailure, setLastFailure] = useState([]);
    const [avgFailureAll, setAvgFailureAll] = useState([]);

    const [avgScore, setAvgScore] = useState([]);
    const [lastScore, setLastScore] = useState([]);
    const [avgScoreAll, setAvgScoreAll] = useState([]);

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
        //Anfrage nach allgemeinen Daten über alle Schüler (fehlen Daten)
        setUser([])
        axios.get('/user').then(data => {
            for (const u in data.data) {
                setUser((user) => [...user, { id: data.data[u][0], name: data.data[u][1], difficulty: data.data[u][2] }])
            }
        })
    }, [])

    const handleChange = (event) => {
        setCurrent(user[event.target.selectedIndex])
        axios.post('/statistics', {
            userId: user[event.target.selectedIndex].id,
            userName: user[event.target.selectedIndex].name,
            DataID: ['task_names', 'avg_task_duration', 'history_of_specific_task_duration',
                'avg_failure_per_failure_category', 'failures_per_run', 'avg_score_tasks', 'score_per_run',
                'individual_average_completion_duration', 'individual_average_completion_failure', 'avg_score_history',
                'avg_score_all_user', 'avg_duration_all_user', 'avg_failure_all_user']
        })
            .then(function (response) {
                console.log(response)

                for (const [key, value] of Object.entries(response.data["task_names"])) {
                    setLabel((label) => [...label, value])
                }

                for (const [key, value] of Object.entries(response.data["avg_task_duration"])) {
                    setAvgTime((avgTime) => [...avgTime, value])
                }

                for (const [key, value] of Object.entries(response.data["history_of_specific_task_duration"])) {
                    setLastTime((lastTime) => [...lastTime, value[value.length - 1]])
                }

                for (const [key, value] of Object.entries(response.data["avg_duration_all_user"])) {
                    setAvgTimeAll((avgTimeAll) => [...avgTimeAll, value])
                }

                for (const [key, value] of Object.entries(response.data["avg_failure_per_failure_category"])) {
                    setAvgFailure((avgFailure) => [...avgFailure, value])
                }

                setLastFailure(Object.entries(response.data["failures_per_run"])[Object.entries(response.data["failures_per_run"]).length - 1][1])

                for (const [key, value] of Object.entries(response.data["avg_failure_all_user"])) {
                    setAvgFailureAll((avgFailureAll) => [...avgFailureAll, value])
                }

                setAvgScore(response.data["avg_score_tasks"])

                Object.entries(response.data["score_per_run"])[Object.entries(response.data["score_per_run"]).length - 1][1].shift()
                setLastScore(Object.entries(response.data["score_per_run"])[Object.entries(response.data["score_per_run"]).length - 1][1])

                for (const [key, value] of Object.entries(response.data["avg_score_all_user"])) {
                    if (key !== '0') {
                        setAvgScoreAll((avgScoreAll) => [...avgScoreAll, value])
                    }
                }

            })
    };


    return (
        <>
            <Link className='profileStyle' style={{ cursor: 'pointer', textDecoration: 'none' }} to={'/UserPage'}>
                Te
            </Link>
            <div className='logoutStyle' style={{ cursor: 'pointer' }} onClick={() => window.location.href = '/'}> <FiIcons.FiLogOut /> </div>
            <label className='UserDropdown'>
                <select value={current['name']} onChange={handleChange}>
                    {user.map(i => (
                        <option value={i.name} key={i.id}>
                            {i.name}</option>
                    ))}
                </select>
            </label>

            <div className='TeacherContainer'>
                <Card className='TeacherTime'>
                    <Plot
                        className='PlotAutosizeTeacher'
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
                <Card className='TeacherFailure'>
                    <Plot
                        className='PlotAutosizeTeacher'
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
                <Card className='TeacherScore'>
                    <Plot
                        className='PlotAutosizeTeacher'
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
                <Card className='TeacherTimeAvg'>
                    <Card.Body>
                        <Row>
                            <Col xs="4">
                                <div className="Icon">
                                    <FcIcons.FcClock size={'60%'} />
                                </div>
                            </Col>
                            <Col xs="8">
                                <Card.Title className='Number'>
                                    <div style={{ fontWeight: 'bold', color: 'grey' }}>
                                        Zeit <br /><br />
                                    </div>
                                    20 min 30 sek
                                    {/* {Math.floor(sumTime / label.length / 60)} min
                                    {Math.floor((sumTime / label.length) % 60)} sek */}
                                </Card.Title>
                            </Col>
                        </Row>
                    </Card.Body>
                    <Card.Footer>
                        <hr></hr>
                        <div className="stats">
                            Durchschnitt pro Task (alle Schüler)
                        </div>
                    </Card.Footer>
                </Card>
                <Card className='TeacherFailureAvg'>
                    <Card.Body>
                        <Row>
                            <Col xs="4">
                                <div className="Icon">
                                    <FcIcons.FcHighPriority size={'60%'} />
                                </div>
                            </Col>
                            <Col xs="8">
                                <Card.Title className='Number'>
                                    <div style={{ fontWeight: 'bold', color: 'grey' }}>
                                        Fehler <br /><br />
                                    </div>
                                    0.5
                                    {/* {Math.round(sumFailure / label.length * 100 + Number.EPSILON) / 100} */}
                                </Card.Title>
                            </Col>
                        </Row>
                    </Card.Body>
                    <Card.Footer>
                        <hr></hr>
                        <div className="stats">
                            Durchschnitt pro Task (alle Schüler)
                        </div>
                    </Card.Footer>
                </Card>
                <Card className='TeacherScoreAvg'>
                    <Card.Body>
                        <Row>
                            <Col xs="4">
                                <div className="Icon">
                                    <FcIcons.FcInspection size={'60%'} />
                                </div>
                            </Col>
                            <Col xs="8">
                                <Card.Title className='Number'>
                                    <div style={{ fontWeight: 'bold', color: 'grey' }}>
                                        Score <br /><br />
                                    </div>
                                    78
                                    {/* {Math.round(sumScore / label.length * 100 + Number.EPSILON) / 100} */}
                                </Card.Title>
                            </Col>
                        </Row>
                    </Card.Body>
                    <Card.Footer>
                        <hr></hr>
                        <div className="stats">
                            Durchschnitt pro Task (alle Schüler)
                        </div>
                    </Card.Footer>
                </Card>
            </div >
        </>
    )
}

export default Teacher;