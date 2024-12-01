import React, { Component, useEffect, useState } from 'react'
import './model2text.css'
import axios from 'axios';
import Button from '@mui/material/Button';
import textFile from './model2text.txt'

function Model2text(props) {
    const [model, setModel] = useState(
        [
            { id: 0, name: 'Gebäudeeinsturz Szenario', path: 'Evaluation_Gebaeudeeinsturz.json' },
            { id: 1,  name: 'Modell 1', path: 'Modell1.json' },
            { id: 2,  name: 'Modell 2', path: 'Modell2.json' },
            { id: 3,  name: 'Modell 3', path: 'Modell3.json' },
        ]
    )
    const [current, setCurrent] = useState('')
    const [text, setText] = useState('')

    const handleChange = (event) => {
        console.log(event.target)
        setCurrent(event.target.value)
    }

    const useModel = () => {
        console.log('ModelID: ', current)
        console.log(model[current]['path'])
        // axios.get('/Data2Text').then(data => {
        //     console.log(data)
        // })
        axios.post('/Data2Text', {
            modelId: model[current]['path']
        })
        .then(function (response) {
            console.log(response.data)
        })
    }

    useEffect(() => {
        // fetch(textFile)
        //     .then(r => r.text())
        //     .then(text => {
        //         console.log('text decoded:', text);
        //         setText(text)
        //     });
    }, [])

    return(
        <>
        <div className='modellist'>
            <label>
                <select value={current} onChange={handleChange}>
                { model.map(model => (
                    <option value={model.id}>{model.name}</option>
                ))}
                </select>
            </label>  
        </div>
        <div className='createText' onClick={useModel}> 
            Erzeugung der textuellen Version
        </div>
        <div>
            {text}
        </div>
        </>
    )

}

export default Model2text