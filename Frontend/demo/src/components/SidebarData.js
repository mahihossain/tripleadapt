import React from 'react';
import * as FaIcons from "react-icons/fa"
import * as AiIcons from "react-icons/ai"
import * as IoIcons from 'react-icons/io'
import * as CgIcons from 'react-icons/cg'
import * as BiIcons from 'react-icons/bi'
import * as FiIcons from 'react-icons/fi'
import * as BsIcons from 'react-icons/bs'
import * as MdIcons from 'react-icons/md'
import * as VscIcons from 'react-icons/vsc'

export const SidebarData = [
    {
        title: 'Assistenz (local)',
        path: '/recommendation',
        icon: <VscIcons.VscDebugStart/>,
        cName: 'main-nav-text'
    },
    {
        title: 'Assistenz (Festo)',
        path: '/',
        icon: <VscIcons.VscDebugStart/>,
        cName: 'main-nav-text'
    },
    {
        title: 'Virtueller Workspace',
        path: '/simulation',
        icon: <BsIcons.BsCollectionPlay/>,
        cName: 'main-nav-text'
    },
    {
        title: 'Analytic',
        path: '/analytics',
        icon: <BiIcons.BiPulse/>,
        cName: 'main-nav-text'
    },
    {
        title: 'Letzter Durchlauf',
        path: '/replay',
        icon: <BsIcons.BsCollectionPlay/>,
        cName: 'main-nav-text'
    },
    {
        title: 'Zurück',
        path: '/',
        icon: <BsIcons.BsBackspaceFill/>,
        cName: 'main-back'
    }

]