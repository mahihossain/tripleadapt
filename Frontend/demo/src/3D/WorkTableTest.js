import React, { useState } from 'react';
import WorkTable from './WorkTable';

export default function WorkTableTest() {
    const [partsState, setPartsState] = useState({
        mutterBox: false,
        kolbenstangeBox: false,
        zylinderBox: false,
        messschieber: false,
        bundschraubeBox: false,
        abschlussdeckelBox: false,
        lagerdeckelBox: false,
        blauerSchrauber: false,
        gelberSchrauber: false,
        scanner: false,
        kolbenbaugruppeBox: false
    });

    return (
        <div>
            {Object.keys(partsState).map(part => {
                console.log(partsState);
                return (
                    <button 
                        key={part}
                        onClick={() => setPartsState(prevState => ({ ...prevState, [part]: !prevState[part] }))}>
                        {part}
                    </button>
                );
            })}
            <WorkTable data={partsState} />
        </div>
    );
}
