import React, { Component } from 'react'
import './simulation.css';
import mutter from '../images/Mutter.png';
import abschlussdeckel from '../images/Abschlussdeckel.png'
import schraube from '../images/Schraube.png';
import kolbenstange from '../images/Kolbenstange.png';
import kolbenbaugruppe from '../images/Baugruppe.png';
import lagerdeckel from '../images/Lagerdeckel.png';
class Material extends Component {
    state = {  } 
    render() { 
        return (
            <>
                <div className='abschlussdeckel' onClick={this.props.pressabschlussdeckel} style={{cursor: 'pointer'}}> 
                    <img className='MaterialPng' src={abschlussdeckel} alt="Abschlussdeckel" />
                    <div className='MaterialTxt'> Abschlussdeckel </div>
                </div>
                <div className='bundschrauben' onClick={this.props.pressbundschrauben} style={{cursor: 'pointer'}}>
                    <img className='MaterialPng' src={schraube} alt="Bundschrauben" />
                    <div className='MaterialTxt'> Bundschrauben </div>
                </div>
                <div className='kolbenstange' onClick={this.props.presskolbenstange} style={{cursor: 'pointer'}}>
                    <img className='MaterialPng' src={kolbenstange} alt="Kolbenstange" />
                    <div className='MaterialTxt'> Kolbenstange </div>
                </div>
                <div className='kolbenbaugruppe' onClick={this.props.presskolbenbaugruppe} style={{cursor: 'pointer'}}> 
                    <img className='MaterialPng' src={kolbenbaugruppe} alt="Kolbenbaugruppe" />
                    <div className='MaterialTxt'> Kolbenbaugruppe </div> 
                </div>
                <div className='mutter' onClick={this.props.pressmutter} style={{cursor: 'pointer'}}> 
                    <img className='MaterialPng' src={mutter} alt="Mutter" />
                    <div className='MaterialTxt'> Mutter </div>
                </div>
                <div className='lagerdeckel' onClick={this.props.presslagerdeckel} style={{cursor: 'pointer'}}> 
                    <img className='MaterialPng' src={lagerdeckel} alt="Lagerdeckel" />
                    <div className='MaterialTxt'> Lagerdeckel </div>
                </div>
            </>
        );
    }
}
 
export default Material;