import React, {useState} from 'react'
import * as FaIcons from "react-icons/fa"
import * as AiIcons from "react-icons/ai"
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { SidebarData } from './SidebarData'
import './MainNavbar.css';
import { IconContext } from 'react-icons'

function Navbar() {
    const [sidebar, setSidebar] = useState(false)

    const showSidebar = () => setSidebar(!sidebar);
    const location = useLocation();

    const navigate = useNavigate();

  return (
    <>
    <IconContext.Provider value={{color: 'black'}}>
        <div className="main-navbar">
            <Link to='#' className='main-menu-bars'>
                <FaIcons.FaBars onClick={showSidebar}/>
            </Link>
        </div>
        <nav className={sidebar ? 'main-nav-menu active' : 'main-nav-menu'}>
            <ul className='main-nav-menu-items' >
                <li className='main-navbar-toggle'>
                    <AiIcons.AiOutlineClose onClick={showSidebar} className='main-menu-bars'/>
                </li>
                {SidebarData.map((item, index) => {
                        return (
                            <li key={index} className={item.path === location.pathname ? 'main-nav-text-active' : item.cName}>
                                <Link to={item.path}>
                                    {item.icon}
                                    <span>{item.title}</span>
                                </Link>
                            </li>
                        )
                })}
            </ul>
        </nav>
        </IconContext.Provider>
    </>
  )
}

export default Navbar