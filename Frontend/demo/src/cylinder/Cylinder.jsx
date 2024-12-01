import React, { Component, useState, useContext, useEffect } from 'react';
import Recommendation3D from '../3D/Recommendation3D';
import axios from 'axios';
import './Cylinder.css'

function Cylinder(props) {
    const [abschlussdeckel, setAbschlussdeckel] = useState(false);
    const [kolbenstange, setKolbenstange] = useState(false);
    const [baugruppe, setBaugruppe] = useState(false);
    const [mutter, setMutter] = useState(false);
    const [lagerdeckel, setLagerdeckel] = useState(false);
    const [schraubeOne, setSchraubeOne] = useState(false);
    const [schraubeTwo, setSchraubeTwo] = useState(false);
    const [schraubeThree, setSchraubeThree] = useState(false);
    const [schraubeFour, setSchraubeFour] = useState(false);
    const [bundschraube, setBundschraube] = useState(false);
    const [kolbenstangeBaugruppe, setKolbenstangeBaugruppe] = useState(false);


    const [schrauberBlau, setSchrauberBlau] = useState(false)
    const [schrauberGelb, setSchrauberGelb] = useState(false)

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


    const [current_activity, setCurrent_activity] = useState('Activity_0pwu48b')
    const [current_werkzeug, setCurrent_werkzeug] = useState('')
    const [current_material, setCurrent_material] = useState('')
    const [activity_name, setActivity_name] = useState('')
    var actual_activity = ''
    var loop_id = null


    useEffect(() => {
        console.log('Cylinder')

        //Test per start_replay_page
        // axios.post('/start_replay_page', {
        //     user: 'Tester_all',
        //     timestamp: '2023-04-21T09:24:36.072Z',
        // })
        //     .then(data => {
        //         console.log(data.data)
        //     })

        loop_id =
            setInterval(() => {
                // console.log('test') 
                axios.get('/status').then(data => {
                    // console.log('____________________')
                    // console.log(data.data)
                    // console.log(data.data['nodes'][0])
                    if (data.data['nodes'] !== undefined) {
                        if (data.data['nodes'][0]['name'] !== 'unknown') {
                            if (data.data['nodes'][0]['bpmn_obj']['id'] !== actual_activity) {
                                actual_activity = data.data['nodes'][0]['bpmn_obj']['id']
                                setCurrent_activity(data.data['nodes'][0]['bpmn_obj']['id'])
                                handleNewActivity(data.data['nodes'][0]['bpmn_obj']['id'])
                            }
                        }
                    }
                    // console.log(data.data['nodes'][0]['bpmn_obj']['id'])
                })
            }, 1500)
    }, [])


    const handleNewActivity = (activityId) => {
        // activityId = 'Activity_0pwu48b'
        // console.log(activityId)
        setCurrent_activity(activityId)
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
                break;
            //Abschlussdeckel entnehmen und aufsetzen
            // case "Activity_1fhbots":
            case "Activity_0euh4f7":
                setCurrent_werkzeug('')
                setCurrent_material('Abschlussdeckel')
                setActivity_name('Abschlussdeckel entnehmen und aufsetzen')
                break;
            //Falscher Pick (Abschlussdeckel)
            // case "Activity_1patann":
            case "Activity_04gxiqa":
                setCurrent_werkzeug('')
                setCurrent_material('')
                setActivity_name('Falscher Pick (Abschlussdeckel)')
                break;
            //Abschlussdeckel entnehmen und aufsetzen
            // case "Activity_0pwu48b":
            case "Activity_1e3r9ol":
                setCurrent_werkzeug('')
                setCurrent_material('Abschlussdeckel')
                setActivity_name('Abschlussdeckel entnehmen und aufsetzen')
                setAbschlussdeckel(true)
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

    return (
        <>
            <div className='CylinderMain'>
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
        </>
    )
}

export default Cylinder;