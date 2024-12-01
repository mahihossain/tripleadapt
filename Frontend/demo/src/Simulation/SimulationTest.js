import { React, useState } from 'react'
import InteractiveCylinder from '../3D/FestoCylinderInteractive'



export default function SimulationTest() {
    var [states, setStates] = useState({
        abschlussdeckel: false,
        kolbenstange: false,
        mutter: false,
        schraubeOne : false,
        schraubeTwo : false,
        schraubeThree : false,
        schraubeFour : false,
        lagerdeckel : false,
        baugruppe : false,
        schrauber_blue : false,
        schrauber_green : false,
        schrauber_grey : false,
        messschieber : false,
    })


    return (
        <>
            <button onClick={() => setStates({ ...states, abschlussdeckel: true })}>Abschlussdeckel</button>
            <button onClick={() => setStates({ ...states, lagerdeckel: true })}>Lagerdeckel</button>
            <button onClick={() => setStates({ ...states, baugruppe: true })}>Baugruppe</button>
            <button onClick={() => setStates({ ...states, kolbenstange: true })}>Kolbenstange</button>
            <button onClick={() => setStates({ ...states, mutter: true })}>Mutter</button>
            <button onClick={() => setStates({ ...states, schraubeOne: true, schraubeTwo : false, schraubeThree: false, schraubeFour: false})}>Schraube_1</button>
            <button onClick={() => setStates({ ...states, schraubeTwo: true, schraubeOne : false, schraubeThree: false, schraubeFour: false })}>Schraube_2</button>
            <button onClick={() => setStates({ ...states, schraubeThree: true, schraubeTwo : false, schraubeOne: false, schraubeFour: false })}>Schraube_3</button>
            <button onClick={() => setStates({ ...states, schraubeFour: true, schraubeTwo : false, schraubeThree: false, schraubeOne: false })}>Schraube_4</button>
            <button onClick={() => setStates({ ...states, schrauber_blue: true, schrauber_green: false, schrauber_grey: false })}>Blauerschrauber</button>
            <button onClick={() => setStates({ ...states, schrauber_green: true, schrauber_blue: false, schrauber_grey:false })}>Grünerschrauber</button>
            <button onClick={() => setStates({ ...states, schrauber_grey: true, schrauber_blue: false, schrauber_green: false })}>Grauerschrauber</button>
            <button onClick={() => setStates({ ...states, messschieber: true })}>Messschieber</button>
            <InteractiveCylinder data={states} />
        </>
    )
}