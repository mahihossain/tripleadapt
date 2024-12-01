import React, { Component } from 'react';
import InteractiveCylinder from '../3D/FestoCylinderInteractive'


function SimulationTest(props) {

    return (
        <>
        {console.log(props.state)}
            <div className='interactiveCylinder'><InteractiveCylinder data={props.state} putMutter={props.putMutter} /></div>
        </>
     );
    
}
 
export default SimulationTest;