import React, { Component } from 'react'
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import ThreeDCylinder from '../3D/ThreeDCylinder.js';
import ModellVideo from './ModellVideo.jsx';
import InteractiveCylinder from '../3D/FestoCylinderInteractive.js';
import SimulationTest from '../Simulation/SimulationTest.jsx';

function CylinderCard(props) {
        return (
        <>
            {/* <ThreeDCylinder /> */}
            <InteractiveCylinder data={props.state}/>
        </>
        );
    }
 
export default CylinderCard;