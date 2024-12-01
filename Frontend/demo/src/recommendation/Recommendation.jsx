import React, { Component, useState, useContext, useEffect } from 'react';
import './Recommendation.css';
import TaskGraph from '../components/TaskGraph';
import Counter from '../components/Counter';
import User from '../components/User';
import Workstation from '../components/workstationCard';
import UserPage from '../profile/UserPage';
import CardMedia from '@mui/material/CardMedia';
import Card from '@mui/material/Card';
import axios from 'axios';
import TaskVis from '../components/TaskVis';
import ModellVideo from '../components/ModellVideo';
import Recommendation3D from '../3D/Recommendation3D';
import Navbar from '../components/Navbar';
import WorkTable from '../3D/WorkTable';
import WorkTableTest from '../3D/WorkTableTest';

import mutterpng from '../images/Mutter.png';
import abschlussdeckelpng from '../images/Abschlussdeckel.png'
import schraubepng from '../images/Schraube.png';
import kolbenstangepng from '../images/Kolbenstange.png';
import kolbenbaugruppepng from '../images/Baugruppe.png';
import lagerdeckelpng from '../images/Lagerdeckel.png';
import messschieber from '../images/Messschieber.png';
import schrauber_grau from '../images/Schrauber_grau.png';
import schrauber_gruen from '../images/Schrauber_grün.png';
import schrauber_blau from '../images/Schrauber_blau.png';

import FestoLogo from '../images/Festologo.PNG';

import * as FiIcons from "react-icons/fi"
import { UserContext } from '../context/UserContext';
import { Link } from "react-router-dom";

function Recommendation(props) {

  const [nodes, setNodes] = useState([]);
  const [testNodes, setTestNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [testEdges, setTestEdges] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const { user, setUser } = useContext(UserContext)
  const [current, setCurrent] = useState('0');
  const [width, setWidth] = useState(0);
  const [current_task, setCurrent_task] = useState('');
  const [task_loading, setTask_loading] = useState(true);
  const [loop, setLoop] = useState(false)

  const [intervalId, setIntervalId] = useState(null);

  const [current_activity, setCurrent_activity] = useState('Activity_0pwu48b')
  // const [current_activity, setCurrent_activity] = useState('Activity_037gp20')

  const [last_node, setLast_node] = useState('TEST')

  // const [current_material, setCurrent_material] = useState('Mutter')
  const [current_material, setCurrent_material] = useState('')
  // const [current_werkzeug, setCurrent_werkzeug] = useState('blauer Schrauber')
  const [current_werkzeug, setCurrent_werkzeug] = useState('')
  const [activity_name, setActivity_name] = useState('')


  const [abschlussdeckel, setAbschlussdeckel] = useState(false);
  const [kolbenstange, setKolbenstange] = useState(false);
  const [baugruppe, setBaugruppe] = useState(false);
  const [mutter, setMutter] = useState(false);
  const [lagerdeckel, setLagerdeckel] = useState(false);
  const [schraubeOne, setSchraubeOne] = useState(false);
  const [schraubeTwo, setSchraubeTwo] = useState(false);
  const [schraubeThree, setSchraubeThree] = useState(false);
  const [schraubeFour, setSchraubeFour] = useState(false);
  const [kolbenstangeBaugruppe, setKolbenstangeBaugruppe] = useState(false);
  const [zylinder, setZylinder] = useState(false);
  const [kolbenbaugruppe, setKolbenbaugruppe] = useState(false);

  const [mutterBox, setMutterBox] = useState(false)
  const [kolbenstangeBox, setKolbenstangeBox] = useState(false)
  const [zylinderBox, setZylinderBox] = useState(false)
  const [bundschraubeBox, setBundschraubeBox] = useState(false)
  const [abschlussdeckelBox, setAbschlussdeckelBox] = useState(false)
  const [lagerdeckelBox, setLagerdeckelBox] = useState(false)
  const [kolbenbaugruppeBox, setKolbenbaugruppeBox] = useState(false)

  const [hervorhebungLagerdeckel, setHervorhebungLagerdeckel] = useState(false);
  const [hervorhebungAbschlussdeckel, setHervorhebungAbschlussdeckel] = useState(false);
  const [hervorhebungKolbenstange, setHervorhebungKolbenstange] = useState(false);
  const [hervorhebungBaugruppe, setHervorhebungBaugruppe] = useState(false);
  const [hervorhebungMutter, setHervorhebungMutter] = useState(false);
  const [hervorhebungSchraubeOne, setHervorhebungSchraubeOne] = useState(false);
  const [hervorhebungSchraubeTwo, setHervorhebungSchraubeTwo] = useState(false);
  const [hervorhebungSchraubeThree, setHervorhebungSchraubeThree] = useState(false);
  const [hervorhebungSchraubeFour, setHervorhebungSchraubeFour] = useState(false);
  const [hervorhebungKolbenstangeBaugruppe, setHervorhebungKolbenstangeBaugruppe] = useState(false);
  const [hervorhebungCylinder, setHervorhebungCylinder] = useState(false);
  const [hervorhebungMessschieber, setHervorhebungMessschieber] = useState(false);
  const [hervorhebungBundschraube, setHervorhebungBundschraube] = useState(false);
  const [hervorhebungBlauerSchrauber, setHervorhebungBlauerSchrauber] = useState(false);
  const [hervorhebungGelberSchrauber, setHervorhebungGelberSchrauber] = useState(false);
  const [hervorhebungScanner, setHervorhebungScanner] = useState(false);

  const [schrauberBlau, setSchrauberBlau] = useState(false)
  const [schrauberGelb, setSchrauberGelb] = useState(false)
  const [messschieber, setMessschieber] = useState(false)
  const [scanner, setScanner] = useState(false)
  const [bundschraube, setBundschraube] = useState(false);
  const [blauerSchrauber, setBlauerSchrauber] = useState(false);
  const [gelberSchrauber, setGelberSchrauber] = useState(false);

  var actual_activity = ''
  var loop_id = null


  useEffect(() => {
    // handleNewActivity('Activity_037gp20')
    const getActivity = () => {
      console.log('useEffect')
      axios.get('/status').then(data => {
        // console.log(data.data)
        if (data.data['nodes'] !== undefined) {
          if (data.data['nodes'][0]['name'] !== 'unknown') {
            if (data.data['nodes'][0]['bpmn_obj']['id'] !== current_activity) {
              setCurrent_activity(data.data['nodes'][0]['bpmn_obj']['id'])
              actual_activity = data.data['subgraph_task']['task_id']
              setCurrent_task(data.data['subgraph_task']['task_id'])
              handleNewActivity(data.data['nodes'][0]['bpmn_obj']['id'])
              // console.log('initial:', data.data['nodes'][0]['bpmn_obj']['id'])
              handleNewGraph(data.data['subgraph_task']['nodes'], data.data['subgraph_task']['edges'], data.data['nodes'][0]['bpmn_obj']['id'])
            }
          }
        }
      })
      renderDifficulty(user.difficulty)
    }

    getActivity()
    axios.get('/model').then(data => {
      // console.log(data.data)
      setTasks(data.data['tasks'])
    })
  }, []);

  const startLoop = () => {
    // console.log('Start Loop')
    setLoop(true)
    clearInterval(intervalId);
    clearInterval(loop_id);
    loop_id =
      setInterval(() => {
        // console.log('test') 
        axios.get('/status').then(data => {
          console.log('____________________')
          console.log(data.data)
          console.log(data.data['nodes'][0])
          if (data.data['nodes'] !== undefined) {
            if (data.data['nodes'][0]['name'] !== 'unknown') {
              // console.log(data.data['nodes'][0]['bpmn_obj']['id'] !== x)
              // console.log('neue Aktivität', data.data['nodes'][0]['bpmn_obj']['id'])
              // console.log('aktuelle Aktivität', x)
              if (data.data['nodes'][0]['bpmn_obj']['id'] !== actual_activity) {
                actual_activity = data.data['nodes'][0]['bpmn_obj']['id']
                setCurrent_activity(data.data['nodes'][0]['bpmn_obj']['id'])
                handleNewActivity(data.data['nodes'][0]['bpmn_obj']['id'])
                setCurrent_task(data.data['subgraph_task']['task_id'])
                handleNewGraph(data.data['subgraph_task']['nodes'], data.data['subgraph_task']['edges'], data.data['nodes'][0]['bpmn_obj']['id'])
              }
            }
          }
          // console.log(data.data['nodes'][0]['bpmn_obj']['id'])
        })
      }, 1500)
    // console.log(intervalId)
    // console.log(loop_id)
    setIntervalId(loop_id)
    // console.log('IntervalId', intervalId)
    startTest()
  }

  const renderStartButton = (loop) => {
    if (!loop) {
      return (
        <div className='startloop' onClick={startLoop} > Starte Test </div>
      )
    } else {
      return (
        <div></div>
      )
    }
  }

  const startTest = () => {
    axios.post('/start_replay_page', {
      user: user['id'],
      timestamp: '2023-04-21T09:24:36.072Z',
    })
      .then(data => {
        console.log(data.data)
      })
  }

  const stopLoop = () => {
    console.log('stop')
    console.log(intervalId)
    console.log(loop_id)
    clearInterval(intervalId)
    clearInterval(loop_id);
    setLoop(false)
    axios.post('/stop_replay_page', {
    })
      .then(function (response) {
        console.log(response.data)
      })
  }

  const deleteMarking = () => {
    // setHervorhebungLagerdeckel(false)
    // setHervorhebungAbschlussdeckel(false)
    // setHervorhebungKolbenstange(false)
    // setHervorhebungBaugruppe(false)
    // setHervorhebungMutter(false)
    // setHervorhebungSchraubeOne(false)
    // setHervorhebungSchraubeTwo(false)
    // setHervorhebungSchraubeThree(false)
    // setHervorhebungSchraubeFour(false)
    // setHervorhebungKolbenstangeBaugruppe(false)
    setMutterBox(false)
    setKolbenstangeBox(false)
    setZylinderBox(false)
    setBundschraubeBox(false)
    setAbschlussdeckelBox(false)
    setLagerdeckelBox(false)
    setKolbenbaugruppeBox(false)
  }



  const handleNewActivity = (activityId) => {
    // activityId = 'Activity_0pwu48b'
    // console.log(activityId)
    setCurrent_activity(activityId)
    deleteMarking()
    switch (activityId) {
      //Assistenz starten
      // case "Activity_0h4egt6":
      case "Activity_0dwnqmx":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Assistenz starten')
        break;
      //Code Scannen
      // case 'Activity_0lasejm':
      case 'Activity_1x5oi6z':
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Code Scannen')
        setAbschlussdeckel(true)
        setAbschlussdeckelBox(true)
        break;
      //Falscher Code
      // case "Activity_0fb5zfa":
      case "Activity_0ys7vtp":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Falscher Code')
        break;
      //Roboter ansteuern Position 1 
      // case "Activity_05on3lu":
      case "Activity_146od25":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Roboter ansteuern Position 1 ')
        break;
      //Roboter Sicherheitshinweis
      // case "Activity_0hhod8x":
      case "Activity_1d8tx27":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Roboter Sicherheitshinweis')
        break;
      //Abschlussdeckel entnehmen
      // case "Activity_163jhyl":
      case "Activity_12xg8b5":
        setCurrent_werkzeug('')
        setCurrent_material('Abschlussdeckel')
        setActivity_name('Abschlussdeckel entnehmen')
        setAbschlussdeckelBox(true)
        break;
      //Abschlussdeckel entnehmen und aufsetzen
      // case "Activity_1fhbots":
      case "Activity_0euh4f7":
        setCurrent_werkzeug('')
        setCurrent_material('Abschlussdeckel')
        setActivity_name('Abschlussdeckel entnehmen und aufsetzen')
        setAbschlussdeckelBox(true)
        break;
      //Falscher Pick (Abschlussdeckel)
      // case "Activity_1patann":
      case "Activity_04gxiqa":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Falscher Pick (Abschlussdeckel)')
        setAbschlussdeckelBox(true)
        break;
      //Abschlussdeckel entnehmen und aufsetzen
      // case "Activity_0pwu48b":
      case "Activity_1e3r9ol":
        setCurrent_werkzeug('')
        setCurrent_material('Abschlussdeckel')
        setActivity_name('Abschlussdeckel entnehmen und aufsetzen')
        setAbschlussdeckel(true)
        setAbschlussdeckelBox(true)
        break;
      //Falscher Pick (Abschlussdeckel)
      case "Activity_1oe9brs":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Falscher Pick (Abschlussdeckel)')
        break;
      //Abschlussdeckel entnehmen
      case "Activity_0m8kg4x":
        setCurrent_werkzeug('')
        setCurrent_material('Abschlussdeckel')
        setActivity_name('Abschlussdeckel entnehmen')
        setAbschlussdeckel(true)
        setAbschlussdeckelBox(true)
        break;
      //Falscher Pick (Abschlussdeckel)
      case "Activity_0smc1qu":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Falscher Pick (Abschlussdeckel)')
        break;
      //Abschlussdeckel aufsetzen
      case "Activity_0fohncm":
        setCurrent_werkzeug('')
        setCurrent_material('Abschlussdeckel')
        setActivity_name('Abschlussdeckel aufsetzen')
        setAbschlussdeckel(true)
        break;
      //Bundschrauben entnehmen
      // case "Activity_1e0vhv7":
      case "Activity_1isp672":
        setCurrent_werkzeug('')
        setCurrent_material('Bundschrauben')
        setActivity_name('Bundschrauben entnehmen')
        break;
      //Bundschrauben entnehmen
      // case "Activity_1lechr5":
      case "Activity_0aintpq":
        setCurrent_werkzeug('')
        setCurrent_material('Bundschrauben')
        setActivity_name('Bundschrauben entnehmen')
        break;
      //Bundschrauben entnehmen und einsetzen
      case "Activity_0c7mtoc":
        setCurrent_werkzeug('')
        setCurrent_material('Bundschrauben')
        setActivity_name('Bundschrauben entnehmen und einsetzen')
        break;
      //Falscher Pick (Bundschrauben)
      case "Activity_1epxwwn":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Falscher Pick (Bundschrauben)')
        break;
      //Bundschrauben entnehmen, einsetzen und festdrehen
      case "Activity_1y4aznv":
        setCurrent_werkzeug('')
        setCurrent_material('Bundschrauben')
        setActivity_name('Bundschrauben entnehmen, einsetzen und festdrehen')
        break;
      //Falscher Pick (Bundschrauben)
      case "Activity_073j171":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Falscher Pick (Bundschrauben)')
        break;
      //Falscher Pick (Bundschrauben)
      case "Activity_1r3jur7":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Falscher Pick (Bundschrauben)')
        break;
      //Bundschrauben einsetzen
      // case "Activity_14cvcvz":
      case "Activity_1phjcfm":
        setCurrent_werkzeug('')
        setCurrent_material('Bundschrauben')
        setActivity_name('Bundschrauben einsetzen')
        setSchraubeThree(true)
        setSchraubeFour(true)
        break;
      //Gelben Schrauber nehmen
      // case "Activity_02edt2c":
      case "Activity_01gdetf":
        setCurrent_werkzeug('gelber Schrauber')
        setCurrent_material('')
        setActivity_name('Gelben Schrauber nehmen')
        break;
      //Bundschrauben festdrehen
      case "Activity_0p1ciux":
        setCurrent_werkzeug('gelber Schrauber')
        setCurrent_material('Bundschrauben')
        setActivity_name('Bundschrauben festdrehen')
        setSchraubeThree(true)
        setSchraubeFour(true)
        break;
      //Roboter parken
      case "Activity_12oktqv":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Roboter parken')
        break;
      //Roboter Sicherheitshinweis
      // case "Activity_1v9ry69":
      case "Activity_1w27oe4":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Roboter Sicherheitshinweis')
        break;
      //Kolbenstange bereitlegen 00536241
      // case "Activity_037gp20":
      case "Activity_0b56vb9":
        setCurrent_werkzeug('')
        setCurrent_material('Kolbenstange')
        setActivity_name('Kolbenstange bereitlegen 00536241')
        break;
      //Kolbenstange bereitlegen 00536352
      // case "Activity_0lmtscs":
      case "Activity_06njxbp":
        setCurrent_werkzeug('')
        setCurrent_material('Kolbenstange')
        setActivity_name('Kolbenstange bereitlegen 00536352')
        break;
      //Kolbenstange bereitlegen 00536249
      // case "Activity_1vx9s22":
      case "Activity_0q63kvz":
        setCurrent_werkzeug('')
        setCurrent_material('Kolbenstange')
        setActivity_name('Kolbenstange bereitlegen 00536249')
        break;
      //Kolbenstange entnehmen
      // case "Activity_06jmsg8":
      case "Activity_0oyr2l6":
        setCurrent_werkzeug('')
        setCurrent_material('Kolbenstange')
        setActivity_name('Kolbenstange entnehmen')
        break;
      //Falscher Pick (Kolbenstange)
      // case "Activity_1sruu4d":
      case "Activity_1w3pfgt":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Falscher Pick (Kolbenstange)')
        break;
      //Kolbenstange messen
      // case "Activity_1pv3djb":
      case "Activity_0mbsduo":
        setCurrent_werkzeug('Messschieber')
        setCurrent_material('Kolbenstange')
        setActivity_name('Kolbenstange messen')
        break;
      //Fehlerhafte Kolbenstange
      // case "Activity_1fjlefr":
      case "Activity_1pfzcr5":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Fehlerhafte Kolbenstange')
        break;
      //Kolbenstange spannen
      // case "Activity_06zvj0k":
      case "Activity_1lyj3pf":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Kolbenstange spannen')
        // setKolbenstange(true)
        break;
      //Kolbenbaugruppe bereitlegen
      // case "Activity_19eo8f7":
      case "Activity_0of1z8f":
        setCurrent_werkzeug('')
        setCurrent_material('Kolbenbaugruppe')
        setActivity_name('Kolbenbaugruppe bereitlegen')
        break;
      //Kolbenbaugruppe entnehmen und aufstecken
      case "Activity_0ql63yt":
        setCurrent_werkzeug('')
        setCurrent_material('Kolbenbaugruppe')
        setActivity_name('Kolbenbaugruppe entnehmen und aufstecken')
        break;
      //Falscher Pick (Kolbenbaugruppe)
      // case "Activity_08lfd67":
      case "Activity_0k23yrd":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Falscher Pick (Kolbenbaugruppe)')
        break;
      //Kolbenbaugruppe entnehmen und aufstecken
      case "Activity_1e3a8cs":
        setCurrent_werkzeug('')
        setCurrent_material('Kolbenbaugruppe')
        setActivity_name('Kolbenbaugruppe entnehmen und aufstecken')
        setBaugruppe(true)
        break;
      //Falscher Pick (Kolbenbaugruppe)
      case "Activity_0jlyede":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Falscher Pick (Kolbenbaugruppe)')
        break;
      //Kolbenbaugruppe entnehmen
      case "Activity_1apqtuz":
        setCurrent_werkzeug('')
        setCurrent_material('Kolbenbaugruppe')
        setActivity_name('Kolbenbaugruppe entnehmen')
        setBaugruppe(true)
        break;
      //Falscher Pick (Kolbenbaugruppe)
      case "Activity_0w86mm6":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Falscher Pick (Kolbenbaugruppe)')
        break;
      //Kolbenbaugruppe aufstecken
      case "Activity_0rl54pk":
        setCurrent_werkzeug('')
        setCurrent_material('Kolbenbaugruppe')
        setActivity_name('Kolbenbaugruppe aufstecken')
        setBaugruppe(true)
        break;
      //Mutter bereitlegen
      case "Activity_0fz0zax":
        setCurrent_werkzeug('')
        setCurrent_material('Mutter')
        setActivity_name('Mutter bereitlegen')
        break;
      //Falscher Pick (Mutter)
      case "Activity_1c35jk8":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Falscher Pick (Mutter)')
        break;
      //Mutter aufdrehen
      case "Activity_0iyarnz":
        setCurrent_werkzeug('')
        setCurrent_material('Mutter')
        setActivity_name('Mutter aufdrehen')
        // setMutter(true)
        break;
      //Mutter entnehmen
      case "Activity_0ar9dg0":
        setCurrent_werkzeug('')
        setCurrent_material('Mutter')
        setActivity_name('Mutter entnehmen')
        // setMutter(true)
        break;
      //Falscher Pick (Mutter)
      case "Activity_0g5ohur":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Falscher Pick (Mutter)')
        break;
      //Mutter entnehmen und aufdrehen
      case "Activity_184jhj3":
        setCurrent_werkzeug('')
        setCurrent_material('Mutter')
        setActivity_name('Mutter entnehmen und aufdrehen')
        // setMutter(true)
        break;
      //Falscher Pick (Mutter)
      case "Activity_15abvim":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Falscher Pick (Mutter)')
        break;
      //Mutter entnehmen, auf- und festdrehen
      case "Activity_0k8r56e":
        setCurrent_werkzeug('')
        setCurrent_material('Mutter')
        setActivity_name('Mutter entnehmen, auf- und festdrehen')
        // setMutter(true)
        break;
      //Falscher Pick (Mutter)
      case "Activity_1jvx4zn":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Falscher Pick (Mutter)')
        break;
      //Mutter aufdrehen
      case "Activity_1yok2oh":
        setCurrent_werkzeug('')
        setCurrent_material('Mutter')
        setActivity_name('Mutter aufdrehen')
        // setMutter(true)
        break;
      //Blauen Schrauber nehmen
      case "Activity_02wekgu":
        setCurrent_werkzeug('blauer Schrauber')
        setCurrent_material('')
        setActivity_name('Blauen Schrauber nehmen')
        break;
      //Mutter festdrehen
      // case "Activity_0dkrmq3":
      case "Activity_1dbzlcf":
        setCurrent_werkzeug('grauer Schrauber')
        setCurrent_material('Mutter')
        setActivity_name('Mutter festdrehen')
        break;
      //Roboter in Montageposition bewegen
      // case "Activity_1048w7a":
      case "Activity_0tszuv3":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Roboter in Montageposition bewegen')
        break;
      //Roboter Sicherheitshinweis
      // case "Activity_1ri9m4b":
      case "Activity_0btmhck":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Roboter Sicherheitshinweis')
        break;
      //Vorbereiten
      // case "Activity_15hk5qa":
      case "Activity_03jb9b2":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Vorbereiten')
        break;
      //Kolbenstangenbaugruppe einführen
      // case "Activity_0agmvsl":
      case "Activity_0axo27h":
        setCurrent_werkzeug('')
        setCurrent_material('Kolbenstangenbaugruppe')
        setActivity_name('Kolbenstangenbaugruppe einführen')
        setBaugruppe(true)
        setKolbenstange(true)
        setMutter(true)
        break;
      //Kolbenstangenbaugruppe vorbereiten und einführen
      case "Activity_07q9gmf":
        setCurrent_werkzeug('')
        setCurrent_material('Kolbenstangenbaugruppe')
        setActivity_name('Kolbenstangenbaugruppe vorbereiten und einführen')
        setBaugruppe(true)
        setKolbenstange(true)
        setMutter(true)
        break;
      //Kolbenstangenbaugruppe vorbereiten und einführen
      case "Activity_0ofzbk3":
        setCurrent_werkzeug('')
        setCurrent_material('Kolbenstangenbaugruppe')
        setActivity_name('Kolbenstangenbaugruppe vorbereiten und einführen')
        setBaugruppe(true)
        setKolbenstange(true)
        setMutter(true)
        break;
      //Lagerdeckel entnehmen
      // case "Activity_1hl5lci":
      case "Activity_16dfci1":
        setCurrent_werkzeug('')
        setCurrent_material('Lagerdeckel')
        setActivity_name('Lagerdeckel entnehmen')
        break;
      //Lagerdeckel entnehmen
      // case "Activity_0urkou2":
      case "Activity_16qudgf":
        setCurrent_werkzeug('')
        setCurrent_material('Lagerdeckel')
        setActivity_name('Lagerdeckel entnehmen')
        break;
      //Falscher Pick (Lagerdeckel)
      // case "Activity_0oqd4w8":
      case "Activity_03o67wt":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Falscher Pick (Lagerdeckel)')
        break;
      //Lagerdeckel entnehmen und aufsetzen
      // case "Activity_0swniv4":
      case "Activity_07e98va":
        setCurrent_werkzeug('')
        setCurrent_material('Lagerdeckel')
        setActivity_name('Lagerdeckel entnehmen und aufsetzen')
        setLagerdeckel(true)
        break;
      //Falscher Pick (Lagerdeckel)
      case "Activity_0mgqzci":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Falscher Pick (Lagerdeckel)')
        break;
      //Lagerdeckel entnehmen und aufsetzen
      case "Activity_00e403m":
        setCurrent_werkzeug('')
        setCurrent_material('Lagerdeckel')
        setActivity_name('Lagerdeckel entnehmen und aufsetzen')
        setLagerdeckel(true)
        break;
      //Falscher Pick (Lagerdeckel)
      case "Activity_1h9k1yq":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Falscher Pick (Lagerdeckel)')
        break;
      //Lagerdeckel aufsetzen
      case "Activity_1lshqnb":
        setCurrent_werkzeug('')
        setCurrent_material('Lagerdeckel')
        setActivity_name('Lagerdeckel aufsetzen')
        setLagerdeckel(true)
        break;
      //Bundschrauben bereitlegen
      // case "Activity_17xv760":
      case "Activity_1dqfvyy":
        setCurrent_werkzeug('')
        setCurrent_material('Bundschrauben')
        setActivity_name('Bundschrauben bereitlegen')
        break;
      //Bundschrauben entnehmen
      case "Activity_0xlnchg":
        setCurrent_werkzeug('')
        setCurrent_material('Bundschrauben')
        setActivity_name('Bundschrauben entnehmen')
        break;
      //Falscher Pick (Bundschrauben)
      // case "Activity_1rmtv39":
      case "Activity_0j0werl":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Falscher Pick (Bundschrauben)')
        break;
      //Falscher Pick (Bundschrauben)
      case "Activity_14cvcvz":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Falscher Pick (Bundschrauben)')
        break;
      //Bundschrauben einsetzen
      case "Activity_1igpgci":
        setCurrent_werkzeug('')
        setCurrent_material('Bundschrauben')
        setActivity_name('Bundschrauben entnehmen')
        break;
      //Gelber Schrauber nehmen
      // case "Activity_0npz5kt":
      case "Activity_0uq9io4":
        setCurrent_werkzeug('gelber Schrauber')
        setCurrent_material('')
        setActivity_name('Gelben Schrauber nehmen')
        break;
      //Bundschrauben festdrehen
      // case "Activity_1t3xlk0":
      case "Activity_06s2l6d":
        setCurrent_werkzeug('gelber Schrauber')
        setCurrent_material('Bundschrauben')
        setActivity_name('Bundschrauben festdrehen')
        setSchraubeOne(true)
        setSchraubeTwo(true)
        setBundschraube(true)
        break;
      //Roboter Baugruppe ablegen lassen
      // case "Activity_1sgwxa1":
      case "Activity_0pk2bbu":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Roboter Baugruppe ablegen lassen')
        break;
      //Sicherheitshinweis - Roboter aktiv!
      case "Activity_1lpcy0y":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Sicherheitshinweis - Roboter aktiv!')
        break;
      //Assistenz erfolgreich abgeschlossen
      // case "Activity_0a7w4ip":
      case "Activity_1ouk6om":
        setCurrent_werkzeug('')
        setCurrent_material('')
        setActivity_name('Assistenz erfolgreich abgeschlossen')
        break;
      default:
        break;
    }
    // switch (user.difficulty) {
    //   case 'DIFFICULT':
    //     console.log('DIFFICULT')
    //     deleteMarking()
    //     setCurrent_material('')
    //     setCurrent_werkzeug('')
    //     break;
    //   case 'MEDIUM':
    //     console.log('MEDIUM')
    //     deleteMarking()
    //     break;
    //   default:
    //     break;
    // }
    return true
  }

  const handleNewGraph = (nodes, edges, active_node) => {
    // console.log('nodes', nodes)
    // console.log('edges', edges)
    // console.log('active_node', active_node)
    setNodes(nodes)
    nodes.map(node => (node['label'] = node['name']))
    nodes.map(node => (node['group'] = 'notactive'))
    setEdges(edges)
    // console.log('active node:', active_node)
    setCurrent_activity(active_node)
    var a_node = nodes.filter(n => String(n.id) === active_node)[0]
    if (a_node !== undefined) {
      // console.log('active')
      a_node['group'] = 'active'
    }
    // console.log('last_node: ', last_node)
    var l_node = nodes.filter(n => String(n.id) === last_node)[0]
    // console.log(l_node)
    if (l_node !== undefined) {
      // console.log('not active')
      l_node['group'] = 'notactive'
    }
    setLast_node(active_node)
    // console.log(this.state.edges)
  }

  const handleLoading = (current_task) => {
    setIsLoading(false)
    setCurrent_task(current_task)
  }

  const renderDifficulty = (diff) => {
    switch (diff) {
      case 'DIFFICULT':
        console.log('DIFFICULT')
        deleteMarking()
        setCurrent_material('')
        setCurrent_werkzeug('')
        return (<div></div>)
      case 'MEDIUM':
        console.log('MEDIUM')
        deleteMarking()
        return (<div> </div>)
      default:
        return (
          <div className='optionalStyle'>
            <ModellVideo />
          </div>
        )
    }
  }

  const currentDate = () => {
    const current = new Date()
    const date = `${current.getDate()}/${current.getMonth() + 1}/${current.getFullYear()}`;

    return date
  }

  // const logout = () => {
  //   this.setState({login: false})
  // }

  return (
    <>
      <div className='NavigationBar'>
        <Navbar />
      </div>

      <Link className='profileStyle_rec' style={{ cursor: 'pointer', textDecoration: 'none' }} to={'/UserPage'}>
        {user.name[0]}
      </Link>

      <Link to="/">
        <img className="logoStyle" style={{ cursor: 'pointer', textDecoration: 'none' }} src={FestoLogo} alt='Festo Logo' />
      </Link>

      <div> {renderStartButton(loop)} </div>
      {/* <div className='startloop' onClick={ startLoop } disabled> Starte Test </div> */}
      <div className='stoploop' onClick={stopLoop}> Stop </div>

      <div className='logoutStyle_rec' style={{ cursor: 'pointer' }} onClick={event => window.location.href = '/'}> <FiIcons.FiLogOut /> </div>
      <Link className='back_rec' style={{ cursor: 'pointer', textDecoration: 'none' }} to={'/'}> Zurück </Link>
      {/* <div className='activityName'> {activity_name} </div> */}
      <div className='personStyle'>
        {/* <div style={{'position' : 'absolute', 'left' : '1%', 'top' : '0%', 'color' : '#A4A4A4'}}>
                    Name:
                </div>
                <div style={{'position' : 'absolute', 'left' : '40%', 'top' : '0%'}}>
                    {user.name}
                </div> */}
        <div style={{ 'position': 'absolute', 'left': '1%', 'top': '0%', 'color': '#A4A4A4' }}>
          Datum:
        </div>
        <div style={{ 'position': 'absolute', 'left': '40%', 'top': '0%' }}>
          {currentDate()}
        </div>
        <div style={{ 'position': 'absolute', 'left': '1%', 'top': '35%', 'color': '#A4A4A4' }}>
          Schwierigkeit:
        </div>
        <div style={{ 'position': 'absolute', 'left': '40%', 'top': '35%' }}>
          {user.difficulty}
        </div>
      </div>

      <div className='werkBankStyle'>
        {/* <WorkTableTest/> */}
        <WorkTable data={{
          mutterBox,
          kolbenstangeBox,
          zylinderBox,
          bundschraubeBox,
          abschlussdeckelBox,
          lagerdeckelBox,
          kolbenbaugruppeBox,
          blauerSchrauber: false,
          gelberSchrauber: false,
          scanner: false,
          messschieber: false,
        }} />

      </div>

      <div className='cylinderStyle'>
        <Recommendation3D data={{
          abschlussdeckel,
          kolbenstange,
          mutter,
          lagerdeckel,
          baugruppe,
          schraubeOne,
          schraubeTwo,
          schraubeThree,
          schraubeFour,
          kolbenstangeBaugruppe,
          schrauberBlau,
          schrauberGelb,
          hervorhebungLagerdeckel,
          hervorhebungAbschlussdeckel,
          hervorhebungKolbenstange,
          hervorhebungBaugruppe,
          hervorhebungMutter,
          hervorhebungSchraubeOne,
          hervorhebungSchraubeTwo,
          hervorhebungSchraubeThree,
          hervorhebungSchraubeFour,
          hervorhebungKolbenstangeBaugruppe
        }}
        />
      </div>
      <div className='taskStyle'>
        <TaskGraph
          nodes={nodes}
          edges={edges}
          tasks={tasks}
          isLoading={isLoading}
          onLoading={handleLoading}
          onNewGraph={handleNewGraph}
          current_task={current_task}
          current_activity={current_activity} />
      </div>
      {/* <div className='ratingStyle'>
        <div>  Rating  </div>
        <div className='redDot'><span className="dot_red"></span></div>
        <div className='yellowDot'><span className="dot_yellow"></span></div>
        <div className='greenDot'><span className="dot_green"></span></div>
      </div> */}
      {/* <div className='counterStyle'>
        <Counter />
      </div> */}


      <div className='lastTaskStyle'>
        <p> Vorherige Task: </p>
        <TaskVis
          Tasks={tasks}
          current_task={current_task - 1}
          isLoading={isLoading} />
      </div>
      <div className='nextTaskStyle'>
        <p> Nächste Task: </p>
        <TaskVis
          Tasks={tasks}
          current_task={current_task + 1}
          isLoading={isLoading} />
      </div>
    </>
  );

}

export default Recommendation;
