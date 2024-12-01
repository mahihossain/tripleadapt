import React, { Component, useContext, useEffect, useRef, useState } from 'react'
import Hovercard from '../components/Hovercard';
import Button from '@mui/material/Button';
import User from '../components/User';
import './Welcome.css'
import * as FiIcons from "react-icons/fi"
import * as BiIcons from "react-icons/bi"
import { LoginContext, UserContext } from '../context/UserContext';
import { Link } from "react-router-dom";
import GaugeChart from 'react-gauge-chart'
import axios from 'axios';
import FestoLogo from '../images/Festologo.PNG';
// import DFKILogo from '../images/DFKILogo.png';
import DFKILogo from '../images/dfki_Logo_digital_black.png';

import CLEVRLogo from '../images/CLEVRLogo1.png';

import { Card, Container, Row, Col, Table } from "react-bootstrap";
import ChartistGraph from "react-chartist";
import { Line } from 'react-chartjs-2';
import TextField from '@mui/material/TextField';


function Welcome(props) {
  const { user, setUser } = useContext(UserContext);
  const { login, setLogin } = useContext(UserContext);

  const [register, setRegister] = useState(false)
  const [newName, setNewName] = useState('')
  const [PW1, setPW1] = useState('')
  const [PW2, setPW2] = useState('')
  const [role, setRole] = useState(['user', 'admin'])
  const [currentRole, setCurrentRole] = useState('user')
  const [differentPW, setDifferentPW] = useState(false)

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const [existingRuns, setExistingRuns] = useState(false)
  const [loading, setLoading] = useState(false)
  const [wrongPW, setWrongPW] = useState(false)

  const inputRef = useRef(null);

  useEffect(() => {
    setRegister(false)
    // var user_list = []
    // axios.get('/user').then(data => {
    //   console.log(data.data)
    //   for (const user in data.data) {
    //     user_list.push({ id: data.data[user][0], name: data.data[user][1], difficulty: data.data[user][2] })
    //   }
    //   // setAllUser(user_list)
    //   // setUserSet(true)
    // })

    if (login) {
      axios.post('/statistics', {
        userId: user.id,
        userName: user.name,
        DataID: [],
      })
        .then(function (response) {
          if (response.data.length != 0) {
            setExistingRuns(true)
          }
        })
    }


  }, [])

  const dologin = () => {
    setExistingRuns(false)
    setLoading(true)
    setWrongPW(false)
    // console.log(username)
    // console.log(password)
    axios.post('/login', {
      username: username,
      password: password,
    })
      .then(data => {
        if (data.data != 'False') {
          setLogin(true)
          setUser(data.data)
          setCurrentRole(data.data['role'])
          axios.post('/statistics', {
            userId: username,
            userName: username,
            DataID: [],
          })
            .then(function (response) {
              if (response.data.length != 0) {
                setExistingRuns(true)
              }
            })
        } else {
          setLoading(false)
          setWrongPW(true)
          console.log('falsches PW')
        }

      })

  }

  const registerNewUser = () => {
    if (PW1 !== PW2) {
      setDifferentPW(true)
    } else {
      setDifferentPW(false)
      axios.post('/register', {
        username: newName,
        password: PW1,
        role: currentRole,
      })
        .then(data => {
          if (data.data != 'False') {
            var user_list = []
            // axios.get('/user').then(data => {
            //   for (const user in data.data) {
            //     user_list.push({ id: data.data[user][0], name: data.data[user][1], difficulty: data.data[user][2] })
            //   }
            //   // setAllUser(user_list)
            //   // setUserSet(true)
            // })

            setUsername(newName)
            setPassword(PW1)

            //do login
            setExistingRuns(false)
            axios.post('/login', {
              username: newName,
              password: PW1,
            })
              .then(data => {
                if (data.data != 'False') {
                  setLogin(true)
                  setUser(data.data)
                  setCurrentRole(data.data['role'])
                  axios.post('/statistics', {
                    userId: newName,
                    userName: newName,
                    DataID: [],
                  })
                    .then(function (response) {
                      if (response.data.length != 0) {
                        setExistingRuns(true)
                      }
                    })
                } else {
                  console.log('falsches PW')
                }

              })
          }
        })

    }
  }

  const goToregister = () => {
    setRegister(true)
    setNewName(username)
    setPW1(password)
  }

  const BackToLogin = () => {
    setRegister(false)
    setUsername(newName)
    setPassword(PW1)
  }

  const dologout = () => {
    setLogin(false)
    setUser(null)
    setRegister(false)
    setUsername('')
    setPassword('')
    setCurrentRole(0)
    setNewName('')
    setPW1('')
    setPW2('')
  }

  const handleName = (name) => {
    setUsername(name)
  }

  const handlePW = (pw) => {
    setPassword(pw)
  }

  const handleNewName = (name) => {
    setNewName(name)
  }

  const handlePW1 = (pw) => {
    setPW1(pw)
  }

  const handlePW2 = (pw) => {
    setPW2(pw)
  }

  const handleChange = (event) => {
    setCurrentRole(role[event.target.selectedIndex])
  }



  const renderDifferentPW = (different) => {
    if (different) {
      return (
        <>
          <div>
            Passwörter stimmen nicht überein.
          </div>
        </>
      )
    }
  }

  const renderLogin = (login) => {
    if (!login) {
      if (register) {
        return (
          <>
            <div className='newUserStyle'>
              <div style={{ 'position': 'absolute', 'left': '1%', 'top': '3%' }}>
                Name:
              </div>
              <TextField
                className='namefield'
                id={"Satzfeld"}
                variant="outlined"
                size="small"
                ref={inputRef}
                type="text"
                name={"v"}
                defaultValue=''
                onChange={(event) => handleNewName(event.target.value)}
              />
              <div style={{ 'position': 'absolute', 'left': '1%', 'top': '23%' }}>
                Passwort:
              </div>
              <TextField
                className='pw1field'
                id={"Satzfeld"}
                variant="outlined"
                size="small"
                ref={inputRef}
                type="text"
                name={"v"}
                defaultValue=''
                onChange={(event) => handlePW1(event.target.value)}
              />
              <div style={{ 'position': 'absolute', 'left': '1%', 'top': '43%' }}>
                Passwort wiederholen:
              </div>
              <TextField
                className='pw2field'
                id={"Satzfeld"}
                variant="outlined"
                size="small"
                ref={inputRef}
                type="text"
                name={"v"}
                defaultValue=''
                onChange={(event) => handlePW2(event.target.value)}
              />
              <div style={{ 'position': 'absolute', 'left': '1%', 'top': '63%' }}>
                Rolle zuweisen:
              </div>
              <label className='rolefield'>
                <select value={currentRole} onChange={handleChange}>
                  {role.map(i => (
                    <option value={i} key={i}>
                      {i}</option>
                  ))}
                </select>
              </label>
              <div className='differentPWStyle'>
                {renderDifferentPW(differentPW)}
              </div>

              <button style={{ 'position': 'absolute', 'left': '60%', 'top': '90%' }} onClick={() => registerNewUser()}> Registrieren </button>
              <button style={{ 'position': 'absolute', 'left': '1%', 'top': '90%' }} onClick={BackToLogin}> Zurück zum Login </button>
            </div>
            {/* <Link to={'/teacher'}>
              <button style={{ 'position': 'absolute', 'left': '90%', 'top': '2%' }} onClick={() => registerNewUser()}> Lehrer Seite </button>
            </Link> */}
          </>
        )
      }
      return (
        <>
          <div className='userStyle'>
            <div style={{ 'position': 'absolute', 'left': '1%', 'top': '3%' }}>
              Name:
            </div>
            <TextField
              required
              className='namefield'
              id="outlined-required"
              label="Benutzername"
              size="small"
              defaultValue=''
              onChange={(event) => handleName(event.target.value)}
            />
            <div style={{ 'position': 'absolute', 'left': '1%', 'top': '23%' }}>
              Passwort:
            </div>
            <TextField
              className='pw1field'
              id="outlined-password-input"
              label="Passwort"
              // type="password"
              type="text"
              autoComplete="current-password"
              size="small"
              onChange={(event) => handlePW(event.target.value)}
            />
          </div>
          {loading ?
            <div className='LoadingStyle'> Lädt ... </div>
            :
            <div className='LoadingStyle'> </div>}
          {wrongPW ?
            <div className='LoadingStyle'> falsches Passwort </div>
            :
            <div className='LoadingStyle'> </div>}
          <button className='loginStyle' onClick={dologin}> Login </button>
          <button className='registerStyle' onClick={goToregister}> Registrieren </button>
        </>
      )
    } else {
      console.log(user['role'])
      if (user['role'] == 'user') {
        return (
          <>
            {/* <Navbar/> */}
            <Link className='profileStyle' style={{ cursor: 'pointer', textDecoration: 'none' }} to={'/UserPage'}>
              {user.name[0]}
            </Link>
            <div className='logoutStyle' style={{ cursor: 'pointer' }} onClick={dologout}> <FiIcons.FiLogOut /> </div>

            <Link style={{ cursor: 'pointer', textDecoration: 'none' }} to={'/recommendation'}>
              <Card className='assistance'>
                Montageassistenz (local)
              </Card>
            </Link>
            {/* <Link style={{ cursor: 'pointer', textDecoration: 'none' }} to={'http://localhost:8080/link/login'}> */}
            <Card className='assistance_clevr' onClick={() => window.location.href = 'http://localhost:8080/link/login'}>
              Montageassistenz (Festo)
            </Card>
            {/* </Link> */}
            <Link style={{ cursor: 'pointer', textDecoration: 'none' }} to={'/simulation'}>
              <Card className='workspace'>
                Virtueller Workspace
              </Card>
            </Link>
            <Link style={existingRuns ? { cursor: 'pointer', textDecoration: 'none' } : { cursor: 'default' }} to={existingRuns ? '/analytics' : '/'} >
              <Card className='analytics'>
                Analytics <br />
                {existingRuns ? '' : '(Keine Durchläufe vorhanden)'}
              </Card>
            </Link>
            <Link style={{ cursor: 'pointer', textDecoration: 'none' }} to={'/replay'}>
              <Card className='last'>
                Letzter Durchlauf
              </Card>
            </Link>
          </>
        )
      } else {
        return (
          <>
            <Link className='profileStyle' style={{ cursor: 'pointer', textDecoration: 'none' }} to={'/UserPage'}>
              {user.name[0]}
            </Link>
            <div className='logoutStyle' style={{ cursor: 'pointer' }} onClick={dologout}> <FiIcons.FiLogOut /> </div>
            <Link style={{ cursor: 'pointer', textDecoration: 'none' }} to={'/teacher'}>
              <Card className='last'>
                Statistiken
              </Card>
            </Link>
          </>
        )
      }
    }
  }

  return (
    <div>
      <img className="FESTOlogo" style={{ textDecoration: 'none' }} src={FestoLogo} alt='Festo Logo' />
      <img className="DFKIlogo" style={{ textDecoration: 'none' }} src={DFKILogo} alt='DFKI Logo' />
      <img className="CLEVRLogo" style={{ textDecoration: 'none' }} src={CLEVRLogo} alt='CLEVR Logo' />

      {renderLogin(login)}
    </div>
  );

}

export default Welcome;