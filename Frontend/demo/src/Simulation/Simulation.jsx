import React, { Component, useState, useContext } from 'react'
import SimulationTest from './SimulationTest.jsx';
import './simulation.css';
// import WorkTable from '../3D/WorkTable';
import InteractiveCylinder from '../3D/FestoCylinderInteractive'
import WorkTable from '../3D/WorkTableWithZylinder.js';
import Arbeitsschritt from './Arbeitschritt.jsx';
import * as FiIcons from "react-icons/fi"
import * as BsIcons from "react-icons/bs"
import { UserContext } from '../context/UserContext';
import { useNavigate, Link } from "react-router-dom";
import Navbar from '../components/Navbar.js';
import axios from 'axios';
import { act } from '@react-three/fiber';



function Simulation(props) {
    const [abschlussdeckel, setAbschlussdeckel] = useState(false);
    const [bundschrauben, setBundschrauben] = useState(false);
    const [bundschraube, setBundschraube] = useState(false);
    const [kolbenstange, setKolbenstange] = useState(false);
    const [baugruppe, setBaugruppe] = useState(false);
    const [mutter, setMutter] = useState(false);
    const [lagerdeckel, setLagerdeckel] = useState(false);
    const [schraubeOne, setSchraubeOne] = useState(false);
    const [schraubeTwo, setSchraubeTwo] = useState(false);
    const [schraubeThree, setSchraubeThre] = useState(false);
    const [schraubeFour, setSchraubeFour] = useState(false);
    const [zylinder, setZylinder] = useState(false);
    const [kolbenbaugruppe, setKolbenbaugruppe] = useState(false);

    const [flagAbschlussdeckel, setFlagAbschlussdeckel] = useState(false);
    const [flagBundschrauben, setFLagBundschrauben] = useState(false);
    const [flagKolbenstange, setFlagKolbenstange] = useState(false);
    const [flagBaugruppe, setFlagBaugruppe] = useState(false);
    const [flagMutter, setFlagMutter] = useState(false);
    const [flagLagerdeckel, setFlagLagerdeckel] = useState(false);


    const [blauerSchrauber, setBlauerSchrauber] = useState(false);
    const [gruenerSchrauber, setGruenerSchrauber] = useState(false);
    const [gelberSchrauber, setGelberSchrauber] = useState(false);
    const [grauerSchrauber, setGrauerSchrauber] = useState(false);
    const [messschieber, setMessschieber] = useState(false);
    const [scanner, setScanner] = useState(false)

    const { user, setUser } = useContext(UserContext)

    // const [activityId, setActivityId] = useState('Activity_0npz5kt')
    const [activityId, setActivityId] = useState('Activity_0dwnqmx')
    const [activityName, setActivityName] = useState('Assistenz starten')
    const [time, setTime] = useState(12)
    const [error, setError] = useState(false)
    const [level, setLevel] = useState('')
    const [isLast, setIsLast] = useState(false)

    const currentDate = () => {
        const current = new Date()
        const date = `${current.getDate()}/${current.getMonth() + 1}/${current.getFullYear()}`;

        return date
    }

    const pressabschlussdeckel = () => {
        setAbschlussdeckel(!abschlussdeckel)
    }

    const pressbundschrauben = () => {
        // setBundschrauben(!bundschrauben)
        setSchraubeOne(!schraubeOne)
    }

    const presskolbenstange = () => {
        setKolbenstange(!kolbenstange)
    }

    const presskolbenbaugruppe = () => {
        setBaugruppe(!baugruppe)
    }

    const pressmutter = () => {
        setMutter(!mutter)
    }

    const presslagerdeckel = () => {
        setLagerdeckel(!lagerdeckel)
    }

    const putAbschlussdeckel = () => {
        setFlagAbschlussdeckel(true)
    }

    const putBundschrauben = () => {
        setFLagBundschrauben(true)
    }

    const putKolbenstange = () => {
        setFlagKolbenstange(true)
    }

    const putKolbenbaugruppe = () => {
        setFlagBaugruppe(true)
    }

    const putMutter = () => {
        setFlagMutter(true)
    }

    const putLagerdeckel = () => {
        setFlagLagerdeckel(true)
    }

    const pressblauerSchrauber = () => {
        setBlauerSchrauber(!blauerSchrauber)
        setGruenerSchrauber(false)
        setGrauerSchrauber(false)
    }

    const pressgruenerSchrauber = () => {
        setGruenerSchrauber(!gruenerSchrauber)
        setBlauerSchrauber(false)
        setGrauerSchrauber(false)
    }

    const pressgrauerSchrauber = () => {
        setGrauerSchrauber(!grauerSchrauber)
        setBlauerSchrauber(false)
        setGruenerSchrauber(false)
    }

    const pressMesschieber = () => {
        setMessschieber(!messschieber)
    }

    const getStatus = (activity) => {
        switch (activity) {
            case 'Assistenz starten':
                setTimeout(nextStep, 1500);
                return true
            case 'Code Scannen':
                setTimeout(nextStep, 1000);
                return true
            case 'Roboter ansteuern Position 1':
                setTimeout(nextStep, 1000);
                return true
            case 'Roboter Sicherheitshinweis':
                setTimeout(nextStep, 1000);
                return true
            case 'Mutter entnehmen':
                if (mutter) {
                    setTimeout(nextStep, 1500);
                }
                return mutter
            case 'Mutter entnehmen und aufdrehen':
                return flagMutter
            case 'Mutter entnehmen, auf- und festdrehen':
                return flagMutter
            case 'Mutter aufdrehen':
                return flagMutter
            case 'Blauen Schrauber nehmen':
                return blauerSchrauber
            case 'Mutter festdrehen':
                return true
            case 'Roboter in Montageposition bewegen':
                setTimeout(nextStep, 1000);
                return true
            case 'Lagerdeckel entnehmen':
                return lagerdeckel
            case 'Lagerdeckel entnehmen und aufsetzen':
                return flagLagerdeckel
            case 'Lagerdeckel aufsetzen':
                return flagLagerdeckel
            case 'Bundschrauben bereitlegen':
                return bundschrauben
            case 'Bundschrauben entnehmen':
                return bundschraube
            case 'Bundschrauben entnehmen und einsetzen':
                return flagBundschrauben
            case 'Bundschrauben entnehmen, einsetzen und festdrehen':
                return flagBundschrauben
            case 'Bundschrauben einsetzen':
                return flagBundschrauben
            case 'Gelben Schrauber nehmen':
                return gelberSchrauber
            case 'Bundschrauben festdrehen':
                return flagBundschrauben
            case 'Roboter Baugruppe ablegen lassen':
                setTimeout(nextStep, 1000);
                return true
            case 'Sicherheitshinweis - Roboter aktiv!':
                setTimeout(nextStep, 1000);
                return true
            case 'Assistenz erfolgreich abgeschlossen':
                return true
            // existierende Cases die im Moment nicht im Aufbau sind
            case 'Abschlussdeckel entnehmen':
                return abschlussdeckel
            case 'Abschlussdeckel aufsetzen':
                return flagAbschlussdeckel
            case 'Blauen Schrauber nehmen':
                return blauerSchrauber
            case 'Kolbenstange bereitlegen':
                return kolbenstange
            // case 'Kolbenstange messen':
            //     return true
            case 'Kolbenbaugruppe bereitlegen':
                return baugruppe
            case 'Kolbenbaugruppe aufstecken':
                return flagBaugruppe
            case 'Mutter bereitlegen':
                return mutter
            // case 'Grauen Schrauber nehmen':
            //     return true
            // case 'Mutter festdrehen':
            //     return true             
            // case 'Kolbenbaugruppe einsetzen':
            //     return true
            default:
                return false
        }
    }

    const nextStep = () => {
        // console.log('hier senden an Backend')
        // console.log('ActivityId: ', activityId)
        // console.log('Time: ', time)
        // console.log('Error: ', error)
        axios.post('/task', {
            activityId: activityId,
            time: time,
            error: error,
        })
            .then(function (response) {
                // console.log(response.data);
                setActivityId(response.data['Next_activity_id'])
                setIsLast(response.data['is_last'])
                setActivityName(response.data['Next_activity_name'])
                setLevel(response.data['level'])
            })
    }

    const renderNextStep = (last) => {
        if (!last) {
            return (
                <>
                    <div
                        className={'nextStep'}
                        onClick={nextStep}
                        style={{ cursor: 'pointer' }}>
                        nächster Schritt
                    </div>
                </>
            )
        } else {
            return (
                <>
                </>
            )
        }
    }

    const colorActivity = (activity) => {
        if (getStatus(activity)) {
            return { 'backgroundColor': '#81F781' }
        } else {
            return { 'backgroundColor': '#F3F781' }
        }

    }

    return (
        <>
            <div className='NavigationBar'>
                <Navbar />
            </div>
            <Link className='Profile' style={{ cursor: 'pointer', textDecoration: 'none' }} to={'/UserPage'}>
                {user.name[0]}
            </Link>
            <div className='Logout' style={{ cursor: 'pointer' }} onClick={event => window.location.href = '/'}> <FiIcons.FiLogOut /> </div>
            <Link className='Back' style={{ cursor: 'pointer', textDecoration: 'none' }} to={'/'}> Zurück </Link>

            <div>
                {renderNextStep(isLast)}
            </div>

            <div className='Werkbank'>
                <WorkTable data={{
                    mutter,
                    kolbenstange,
                    zylinder,
                    messschieber,
                    bundschraube,
                    abschlussdeckel,
                    lagerdeckel,
                    blauerSchrauber,
                    gelberSchrauber,
                    scanner,
                    kolbenbaugruppe,

                }}
                    putMutter={putMutter}
                    putKolbenstange={putKolbenstange}
                    putBundschrauben={putBundschrauben}
                    putAbschlussdeckel={putAbschlussdeckel}
                    putLagerdeckel={putLagerdeckel}
                    putKolbenbaugruppe={putKolbenbaugruppe}
                    pressMesschieber={pressMesschieber}
                    pressabschlussdeckel={pressabschlussdeckel}
                    pressbundschrauben={pressbundschrauben}
                    presskolbenstange={presskolbenstange}
                    presskolbenbaugruppe={presskolbenbaugruppe}
                    pressmutter={pressmutter}
                    presslagerdeckel={presslagerdeckel}
                    pressblauerSchrauber={pressblauerSchrauber}
                />

            </div>

            {/* <div className='Cylinder'>
                <WorkTable /> */}
            {/* <InteractiveCylinder data={{
                    abschlussdeckel,
                    kolbenstange,
                    mutter,
                    schrauber_blue: blauerSchrauber,
                    schrauber_green: gruenerSchrauber,
                    schrauber_grey: grauerSchrauber,
                    messschieber,
                    lagerdeckel,
                    baugruppe,
                    schraubeOne,
                    schraubeTwo,
                    schraubeThree,
                    schraubeFour
                }} /> */}
            {/* <SimulationTest
                    state={{
                        abschlussdeckel,
                        kolbenstange,
                        mutter,
                        schrauber_blue: blauerSchrauber,
                        schrauber_green: gruenerSchrauber,
                        schrauber_grey: grauerSchrauber,
                        messschieber,
                        lagerdeckel,
                        baugruppe,
                        schraubeOne,
                        schraubeTwo,
                        schraubeThree,
                        schraubeFour
                    }}
                    putMutter={putMutter}
                    putKolbenstange={putKolbenstange}
                /> */}
            {/* </div> */}

            <div className='Arbeitsschritt' style={colorActivity(activityName)}>
                <Arbeitsschritt
                    activityId={activityId}
                    activityName={activityName}
                />
            </div>
            <div className='Schwierigkeitsgrad'>
                <div style={{ 'position': 'absolute', 'left': '1%', 'top': '15%', 'color': '#A4A4A4' }}>
                    Name:
                </div>
                <div style={{ 'position': 'absolute', 'left': '40%', 'top': '15%' }}>
                    {user.name}
                </div>
                <div style={{ 'position': 'absolute', 'left': '1%', 'top': '50%', 'color': '#A4A4A4' }}>
                    Date:
                </div>
                <div style={{ 'position': 'absolute', 'left': '40%', 'top': '50%' }}>
                    {currentDate()}
                </div>
                <div style={{ 'position': 'absolute', 'left': '1%', 'top': '85%', 'color': '#A4A4A4' }}>
                    Difficulty:
                </div>
                <div style={{ 'position': 'absolute', 'left': '40%', 'top': '85%' }}>
                    {user.difficulty}
                </div>
            </div>
        </>
    );

}

export default Simulation;