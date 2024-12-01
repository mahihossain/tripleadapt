import React, { Component } from 'react'
import './simulation.css';

function Arbeitsschritt(props) {
    
        return (
            <>
                <div>
                    Arbeitsschritt
                </div>
                <div className='Schritt'>
                    {props.activityName}
                    {/* {props.activityId} */}
                </div>
            </>
        );
}
 
export default Arbeitsschritt;