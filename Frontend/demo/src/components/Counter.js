import * as React from 'react';
import AccessTimeFilledOutlinedIcon from '@mui/icons-material/AccessTimeFilledOutlined';
import Card from '@mui/material/Card';

import '../App.css';

function Counter() {
  const [counter, setCounter] = React.useState(0);
  React.useEffect(() => {
    counter >= 0 && setTimeout(() => setCounter(counter + 1), 1000);
  }, [counter]);

  const getMinutes = (time) => {
    var minutes = Math.floor(time / 60);
    var seconds = time - minutes * 60;
    if (seconds < 10) {
      return (String(minutes) + ':0' + String(seconds))
    } else {
      return (String(minutes) + ':' + String(seconds))
    }
  }

  return (
    <>
      {/* <AccessTimeFilledOutlinedIcon style={{left:"0px", right:"0px", position:"relative"}} /> */}
      <div className='taskTime'>Dauer Task 3:</div>
      <div className='taskTime2'> {getMinutes(counter)} min </div>
      <div className='totalTime'>Dauer insgesamt:</div>    
      <div className='totalTime2'> {getMinutes(counter+350)} min </div>
    </>
  );
}

export default Counter;