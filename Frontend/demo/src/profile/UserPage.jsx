import React, { Component, useContext } from 'react'
import { UserContext } from '../context/UserContext';
import * as FiIcons from "react-icons/fi"
import * as AiIcons from "react-icons/ai"
import { Link } from "react-router-dom";

function UserPage(props) {
    
    const {user, setUser} = useContext(UserContext);


    return (
        <>
         {user.name} 
        <Link className='profileStyle' style={{cursor: 'pointer', textDecoration: 'none'}} to={'/UserPage'}>
            {user.name[0]} 
        </Link>
        <div className='logoutStyle' style={{cursor: 'pointer'}} onClick={event => window.location.href='/'}> <FiIcons.FiLogOut/> </div>                
        <Link className='Back' style={{cursor: 'pointer', textDecoration: 'none'}} to={'/'}> <AiIcons.AiFillHome/></Link>
        </>
    )
}

export default UserPage;