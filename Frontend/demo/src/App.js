import React, { Component, useContext, useMemo, useState } from 'react';
import { BrowserRouter, Routes, Route, useParams } from "react-router-dom";
import './App.css';
import Recommendation from './recommendation/Recommendation.jsx';
import ThreeDCylinder from './3D/ThreeDCylinder';
import Welcome from './welcome/Welcome.jsx';
import Analytics from './analytics/Analytics';
import LastRun from './analytics/Pages/LastRun';
import History from './analytics/Pages/History';
import TaskData from './analytics/Pages/TaskData';
import RunData from './analytics/Pages/RunData';
import SimulationTest from './Simulation/SimulationTest.js';
import RecommendationTest from './3D/RecommendationTest.js'
import Simulation from './Simulation/Simulation'
import { UserContext } from './context/UserContext.js';
import FestoCylinderInteractive from './3D/FestoCylinderInteractive';
import Tools from './3D/Tools';
import UserPage from './profile/UserPage';
import Dashboard from './components/Dashboard';
import Replay from './replay/Replay.jsx';
// import Model2Text from './model2text/model2text';
import Sensor from './Sensor/Sensor.jsx';
import WorkTableTest from './3D/WorkTableTest.js';
import Teacher from './Teacher/Teacher.jsx';
import Recommendation3D from './3D/Recommendation3D.js';
import Cylinder from './cylinder/Cylinder.jsx';
import Test from './Test/Test.jsx';
import WorkTable from './3D/WorkTableWithZylinder.js';

// for docker, use "proxy": "http://172.16.238.1:5000" in package.json

function App() {
  const [user, setUser] = useState();
  const [login, setLogin] = useState(false)
  const providerValue = useMemo(() => ({
    user, setUser,
    login, setLogin,
  }), [user, login]);

  return (
    <BrowserRouter>
      <div className="App">
        <UserContext.Provider value={providerValue}>
          <Routes>
            <Route path="/" element={<Welcome />} />
            <Route path="/teacher" element={<Teacher />} />
            <Route path="/recommendation" element={<Recommendation />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path='/last' element={<LastRun />} />
            <Route path='/cylinder' element={<Cylinder />} />
            <Route path='/festocylinder' element={<FestoCylinderInteractive />} />
            <Route path='/simulationtest' element={<SimulationTest />} />
            <Route path='/recommendationtest' element={<RecommendationTest />} />
            <Route path='/simulation' element={<Simulation />} />
            <Route path='/history' element={<History />} />
            <Route path='/taskdata' element={<TaskData />} />
            <Route path='/rundata' element={<RunData />} />
            <Route path='/userpage' element={<UserPage />} />
            <Route path='/dashboard' element={<Dashboard />} />
            <Route path='/tools' element={<Tools data={{ schrauber: false }} />} />
            <Route path='/sensor' element={<Sensor />} />
            <Route path='/replay' element={<Replay />} />
            {/* <Route path='/model2text' element={<Model2Text />} /> */}
            <Route path='/worktable' element={<WorkTableTest />} />
            <Route path='/worktablewithzylinder' element={<WorkTable />} />
            <Route path='/test' element={<Test />} />
          </Routes>
        </UserContext.Provider>
      </div>

    </BrowserRouter>
  );

}

export default App;