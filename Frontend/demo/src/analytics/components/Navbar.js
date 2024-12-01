import React, {useState} from 'react'
import * as FaIcons from "react-icons/fa"
import * as AiIcons from "react-icons/ai"
import { Link } from 'react-router-dom'
import { SidebarData } from './SidebarData'
import './Navbar.css';
import { IconContext } from 'react-icons'
import { useLocation } from 'react-router-dom'

function Navbar() {
    const [sidebar, setSidebar] = useState(true)

    const showSidebar = () => setSidebar(!sidebar);
    const location = useLocation();

  return (
    <>
    <IconContext.Provider value={{color: 'black'}}>
        <div className="analytic-navbar">
            <Link to='#' className='analytic-menu-bars'>
                <FaIcons.FaBars onClick={showSidebar}/>
            </Link>
        </div>
        <nav className={sidebar ? 'analytic-nav-menu active' : 'analytic-nav-menu'}>
            <ul className='analytic-nav-menu-items' >
                <li className='analytic-navbar-toggle'>
                    <AiIcons.AiOutlineClose onClick={showSidebar} className='analytic-menu-bars'/>
                </li>
                {SidebarData.map((item, index) => {
                        if (item.path === '/analytics' && (location.pathname === '/rundata' || location.pathname === '/taskdata')) {
                            return (
                                <li key={index} className={'under-analytics'}>
                                    <Link to={item.path}>
                                        {item.icon}
                                        <span>{item.title}</span>
                                    </Link>
                                </li>
                            )     
                        } else {
                            return (
                                <li key={index} className={item.path === location.pathname ? item.cName + '-active' : item.cName}>
                                    <Link to={item.path}>
                                        {item.icon}
                                        <span>{item.title}</span>
                                    </Link>
                                </li>
                            )                                 
                        }
                        
                })}
            </ul>
        </nav>
        </IconContext.Provider>
    </>
  )
}

export default Navbar