import React from 'react'
import Card from '@mui/material/Card';
import Dates from './Dates';
import Analogclock from './Analogclock';

function Clockandcalendar() {
    return (
        <div>
             <div style={{width:"400px", position:"absolute"}}>
             <Dates />
             </div>
             <div style={{position:"relative", left:"360px"}}>
             <Analogclock />
             </div>  
        </div>
    )
}

export default Clockandcalendar
