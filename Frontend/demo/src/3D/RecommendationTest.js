import { React, useState } from 'react'
import Recommendation3D from '../3D/Recommendation3D'



export default function RecommendationTest() {
    let [states, setStates] = useState({
        abschlussdeckel: false,
        kolbenstange: false,
        mutter: false,
        schraubeOne: false,
        schraubeTwo: false,
        schraubeThree: false,
        schraubeFour: false,
        lagerdeckel: false,
        baugruppe: false,
        kolbenstangeBaugruppe: false,
        schrauberBlau: false,
        schrauberGrau: false,
        // Hervorhebung block
        hervorhebungLagerdeckel: false,
        hervorhebungAbschlussdeckel: false,
        hervorhebungKolbenstange: false,
        hervorhebungBaugruppe: false,
        hervorhebungMutter: false,
        hervorhebungSchraubeOne: false,
        hervorhebungSchraubeTwo: false,
        hervorhebungSchraubeThree: false,
        hervorhebungSchraubeFour: false,
        hervorhebungKolbenstangeBaugruppe: false,
    })


    return (
        <>
            <button onClick={() => setStates({ ...states, abschlussdeckel: true })}>Abschlussdeckel</button>
            <button onClick={() => setStates({ ...states, lagerdeckel: true })}>Lagerdeckel</button>
            <button onClick={() => setStates({ ...states, kolbenstange: true })}>Kolbenstange</button>
            <button onClick={() => setStates({ ...states, baugruppe: true })}>Baugruppe</button>
            <button onClick={() => setStates({ ...states, mutter: true })}>Mutter</button>
            <button onClick={() => setStates({ ...states, schraubeOne: true, })}>Schraube_1</button>
            <button onClick={() => setStates({ ...states, schraubeTwo: true, })}>Schraube_2</button>
            <button onClick={() => setStates({ ...states, schraubeThree: true, })}>Schraube_3</button>
            <button onClick={() => setStates({ ...states, schraubeFour: true, })}>Schraube_4</button>
            <button onClick={() => setStates({
                ...states, schrauberBlau: true,
            })}>Schrauber Blau</button>
            <button onClick={() => setStates({
                ...states, schrauberGrau: true,
            })}>Schrauber Grau</button>
            <button onClick={() => setStates({
                ...states, kolbenstangeBaugruppe: true,
                kolbenstange: false, baugruppe: false, mutter: false
            })}>Kolbenstangebaugruppe</button>
            <button onClick={() => setStates({
                ...states, hervorhebungLagerdeckel:
                    !states.hervorhebungLagerdeckel,
            })}>Hervorhebung Lagerdeckel</button>
            <button onClick={() => setStates({
                ...states, hervorhebungAbschlussdeckel:
                    !states.hervorhebungAbschlussdeckel,
            })}>Hervorhebung Abschlussdeckel</button>
            <button onClick={() => setStates({
                ...states, hervorhebungKolbenstange:
                    !states.hervorhebungKolbenstange,
            })}>Hervorhebung Kolbenstange</button>
            <button onClick={() => setStates({
                ...states, hervorhebungBaugruppe:
                    !states.hervorhebungBaugruppe,
            })}>Hervorhebung Baugruppe</button>
            <button onClick={() => setStates({
                ...states, hervorhebungMutter:
                    !states.hervorhebungMutter,
            })}>Hervorhebung Mutter</button>
            <button onClick={() => setStates({
                ...states, hervorhebungSchraubeOne:
                    !states.hervorhebungSchraubeOne,
            })}>Hervorhebung Schraube_1</button>
            <button onClick={() => setStates({
                ...states, hervorhebungSchraubeTwo:
                    !states.hervorhebungSchraubeTwo,
            })}>Hervorhebung Schraube_2</button>
            <button onClick={() => setStates({
                ...states, hervorhebungSchraubeThree:
                    !states.hervorhebungSchraubeThree,
            })}>Hervorhebung Schraube_3</button>
            <button onClick={() => setStates({
                ...states, hervorhebungSchraubeFour:
                    !states.hervorhebungSchraubeFour,
            })}>Hervorhebung Schraube_4</button>
            <button onClick={() => setStates({
                ...states, hervorhebungKolbenstangeBaugruppe:
                    !states.hervorhebungKolbenstangeBaugruppe,
            })}>Hervorhebung Kolbenstangebaugruppe</button>
            <Recommendation3D data={states} />
        </>
    )
}