import React, { useContext, useEffect, useState } from 'react'
import Navbar from '../components/Navbar';
import * as FiIcons from "react-icons/fi"
import * as FcIcons from "react-icons/fc";
import { UserContext } from '../../context/UserContext';
import { Link, useLocation } from "react-router-dom";
import './TaskData.css'
import axios from 'axios';
import { Card, Container, Row, Col, Table } from "react-bootstrap";
import Plot from 'react-plotly.js';

function TaskData(props) {
    const { user, setUser } = useContext(UserContext)
    const location = useLocation();
    const [taskName, setTaskName] = useState('');
    const [taskId, setTaskId] = useState('');
    const [taskList, setTaskList] = useState([])
    const [avgScoreTasks, setAvgScoreTasks] = useState([])
    const [avgFailureTasks, setAvgFailureTasks] = useState([])
    const [avgTimeTasks, setAvgTimeTasks] = useState([])
    const [specificTaskDuration, setSpecificTaskDuration] = useState([])
    const [label, setLabel] = useState([]);
    const [scoreList, setScoreList] = useState([]);
    const [failureList, setFailureList] = useState([]);
    const [sumFailure, setSumFailure] = useState(0)
    const [current, setCurrent] = useState(0);
    const [tasks, setTasks] = useState([])


    const Time = {
        x: label,
        y: specificTaskDuration[taskId],
        name: "letzten Zeiten",
        type: "bar",
        marker: {
            color: '#0091dc'
        }
    };

    const Failure = {
        x: label,
        y: failureList,
        name: "letzten Fehler",
        type: "bar",
        marker: {
            color: '#0091dc'
        }
    };

    const Score = {
        x: label,
        y: scoreList,
        name: "letzten Scores",
        type: "bar",
        marker: {
            color: '#0091dc'
        }
    };

    useEffect(() => {
        let TaskId = 1
        let TaskName = 'Starten'

        if (location.state !== null) {
            setTaskId(location.state['IdList'][location.state['TaskName']])
            setTaskName(location.state.TaskName)
            setCurrent(location.state.TaskName)
            TaskId = location.state['IdList'][location.state['TaskName']]
            TaskName = location.state.TaskName
        } else {
            setTaskId(TaskId)
            setTaskName(TaskName)
            setCurrent(TaskName)
        }

        axios.post('/statistics', {
            userId: user.id,
            // userId: 0,
            userName: user.name,
            // userName: "Ingoi",
            DataID: ['avg_score_tasks', 'history_of_specific_task_duration', 'avg_task_duration', 'avg_failure_per_failure_category',
                'score_per_run', 'failures_per_run', 'task_names']
        })
            .then(function (response) {
                let sumFailure = 0
                setTasks([])

                for (const [key, value] of Object.entries(response.data["task_names"])) {
                    setTasks((task) => [...task, value])
                }

                for (const [key, value] of Object.entries(response.data['history_of_specific_task_duration'][1])) {
                    setLabel((label) => [...label, Number(key) + 1])
                }

                setSpecificTaskDuration(response.data["history_of_specific_task_duration"])
                setAvgTimeTasks(response.data["avg_task_duration"])
                for (const [key, value] of Object.entries(response.data['failures_per_run'])) {
                    setFailureList((failure) => [...failure, value[TaskId]])
                    sumFailure = sumFailure + Number(value[TaskId])
                    setSumFailure(sumFailure)
                }

                for (const [key, value] of Object.entries(response.data['score_per_run'])) {
                    setScoreList((score) => [...score, value[TaskId]])
                }
                setAvgScoreTasks(response.data["avg_score_tasks"])
            })
    }, [])

    const handleChange = (event) => {
        setCurrent(tasks[event.target.selectedIndex])
        setTaskId(event.target.selectedIndex + 1)

        axios.post('/statistics', {
            userId: user.id,
            // userId: 0,
            userName: user.name,
            // userName: "Ingoi",
            DataID: ['avg_score_tasks', 'history_of_specific_task_duration', 'avg_task_duration', 'avg_failure_per_failure_category',
                'score_per_run', 'failures_per_run']
        })
            .then(function (response) {
                let sumFailure = 0
                setFailureList([])
                setScoreList([])


                for (const [key, value] of Object.entries(response.data['history_of_specific_task_duration'][1])) {
                    setLabel((label) => [...label, Number(key) + 1])
                }

                setSpecificTaskDuration(response.data["history_of_specific_task_duration"])
                setAvgTimeTasks(response.data["avg_task_duration"])
                for (const [key, value] of Object.entries(response.data['failures_per_run'])) {
                    setFailureList((failure) => [...failure, value[event.target.selectedIndex + 1]])
                    sumFailure = sumFailure + Number(value[event.target.selectedIndex + 1])
                    setSumFailure(sumFailure)
                }

                for (const [key, value] of Object.entries(response.data['score_per_run'])) {
                    setScoreList((score) => [...score, value[event.target.selectedIndex + 1]])
                }
                setAvgScoreTasks(response.data["avg_score_tasks"])

            })
    };

    return (
        <>
            <Navbar />
            <Link className='profileStyle' style={{ cursor: 'pointer', textDecoration: 'none' }} to={'/UserPage'}>
                {user.name[0]}
            </Link>
            <div className='logoutStyle' style={{ cursor: 'pointer' }} onClick={() => window.location.href = '/'}> <FiIcons.FiLogOut /> </div>
            <label className='tasks'>
                <select value={current} onChange={handleChange}>
                    {tasks.map(i => (
                        <option value={i}>{i}</option>
                    ))}
                </select>
            </label>
            <div className='TaskDataContainer'>
                <Card className='ZeitHistogram'>
                    <Plot
                        className='PlotAutosize'
                        data={[Time]}
                        layout={{
                            autosize: true,
                            title: 'Zeit des Tasks in den letzten Durchläufen',
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
                <Card className='FailureHistogram'>
                    <Plot
                        className='PlotAutosize'
                        data={[Failure]}
                        layout={{
                            autosize: true,
                            title: 'Fehler des Tasks in den letzten Durchläufen',
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
                <Card className='ScoreHistogram'>
                    <Plot
                        className='PlotAutosize'
                        data={[Score]}
                        layout={{
                            autosize: true,
                            title: 'Score des Tasks in den letzten Durchläufen',
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

                <Card className='avgTime'>
                    <Card.Body>
                        <Row>
                            <Col xs="4">
                                <div className="TaskIcon">
                                    <FcIcons.FcClock size={'60%'} />
                                </div>
                            </Col>
                            <Col xs="8">
                                <Card.Title className='TaskNumber'>
                                    <div style={{ fontWeight: 'bold', color: 'grey' }}>
                                        Zeit <br /><br />
                                    </div>
                                    {Math.floor(avgTimeTasks[taskId] / 60)} min <br />
                                    {Math.floor(avgTimeTasks[taskId] % 60)} sek
                                </Card.Title>
                            </Col>
                        </Row>
                    </Card.Body>
                    <Card.Footer>
                        <hr></hr>
                        <div className="stats">
                            Durchschnitt des Tasks
                        </div>
                    </Card.Footer>
                </Card>
                <Card className='avgFailure'>
                    <Card.Body>
                        <Row>
                            <Col xs="4">
                                <div className="TaskIcon">
                                    <FcIcons.FcClock size={'60%'} />
                                </div>
                            </Col>
                            <Col xs="8">
                                <Card.Title className='TaskNumber'>
                                    <div style={{ fontWeight: 'bold', color: 'grey' }}>
                                        Fehler <br /><br />
                                    </div>
                                    {Math.round(sumFailure / label.length * 100 + Number.EPSILON) / 100}</Card.Title>
                            </Col>
                        </Row>
                    </Card.Body>
                    <Card.Footer>
                        <hr></hr>
                        <div className="stats">
                            Durchschnitt des Tasks
                        </div>
                    </Card.Footer>
                </Card>
                <Card className='avgTaskScore'>
                    <Card.Body>
                        <Row>
                            <Col xs="4">
                                <div className="TaskIcon">
                                    <FcIcons.FcInspection size={'60%'} />
                                </div>
                            </Col>
                            <Col xs="8">
                                <Card.Title className='TaskNumber'>
                                    <div style={{ fontWeight: 'bold', color: 'grey' }}>
                                        Score <br /><br />
                                    </div>
                                    {Math.round(avgScoreTasks[taskId] * 100 + Number.EPSILON) / 100}</Card.Title>
                            </Col>
                        </Row>
                    </Card.Body>
                    <Card.Footer>
                        <hr></hr>
                        <div className="stats">
                            Durchschnitt des Tasks
                        </div>
                    </Card.Footer>
                </Card>
            </div>
        </>
    )
}

export default TaskData