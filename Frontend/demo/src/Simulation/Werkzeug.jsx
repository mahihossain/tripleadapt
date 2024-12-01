import React, { Component } from 'react'
import './simulation.css';
import messschieber from '../images/Messschieber.png'
import schrauber_grau from '../images/Schrauber_grau.png'
import schrauber_gruen from '../images/Schrauber_grün.png'
import schrauber_blau from '../images/Schrauber_blau.png'

class Werkzeug extends Component {
    state = {  } 
    render() { 
        return (
            <>  
                <div className='BlauerSchrauber' onClick={this.props.pressblauerSchrauber}>
                    <div className='WerkzeugId'> ID 136 </div>
                    <img className='WerkzeugPng' src={schrauber_blau} alt='Schrauber_blau' />
                    <div className='WerkzeugTxt'> blauer Schrauber </div>
                    <div className='WerkzeugSize'> Size 6 </div>
                </div>
                <div className='GruenerSchrauber' onClick={this.props.pressgruenerSchrauber}>
                    <div className='WerkzeugId'> ID 138 </div>
                    <img className='WerkzeugPng' src={schrauber_gruen} alt='Schrauber_grün' />
                    <div className='WerkzeugTxt'> grüner Schrauber </div>
                    <div className='WerkzeugSize'> Size 8 </div>
                </div>
                <div className='GrauerSchrauber' onClick={this.props.pressgrauerSchrauber}>
                    <div className='WerkzeugId'> ID 140 </div>
                    <img className='WerkzeugPng' src={schrauber_grau} alt='Schrauber_grau' />
                    <div className='WerkzeugTxt'> grauer Schrauber </div>
                    <div className='WerkzeugSize'> Size 10 </div>
                </div>
                <div className='Messschieber' onClick={this.props.pressMesschieber}>
                    <div className='WerkzeugId'> ID 7 </div>
                    <img className='WerkzeugPng' src={messschieber} alt='Messchieber' />
                    <div className='WerkzeugTxt'> Messschieber </div>
                </div>
            </>
        );
    }
}
 
export default Werkzeug;