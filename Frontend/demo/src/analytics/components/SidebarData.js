import React from 'react';
import * as FaIcons from "react-icons/fa"
import * as AiIcons from "react-icons/ai"
import * as IoIcons from 'react-icons/io'
import * as CgIcons from 'react-icons/cg'
import * as BiIcons from 'react-icons/bi'
import * as FiIcons from "react-icons/fi"
import * as BsIcons from "react-icons/bs"
import * as GrIcons from "react-icons/gr"
import * as VscIcons from 'react-icons/vsc'

export const SidebarData = [
    
    {
        title: 'Assistenz (local)',
        path: '/recommendation',
        icon: <VscIcons.VscDebugStart/>,
        cName: 'analytic-nav-text'
    },
    {
        title: 'Assistenz (Festo)',
        path: '/',
        icon: <VscIcons.VscDebugStart/>,
        cName: 'analytic-nav-text'
    },
    {
        title: 'Virtueller Workspace',
        path: '/simulation',
        icon: <BsIcons.BsCollectionPlay/>,
        cName: 'analytic-nav-text'
    },
    {
        title: 'Analytic Überblick',
        path: '/analytics',
        icon: <CgIcons.CgLoadbarSound/>,
        cName: 'analytic-nav-text'
    },
    {
        title: 'Durchlauf Daten',
        path: '/rundata',
        icon: <BiIcons.BiPulse/>,
        cName: 'analytic-sub-nav-text'
    },
    {
        title: 'Task Daten',
        path: '/taskdata',
        icon: <GrIcons.GrTasks/>,
        cName: 'analytic-sub-nav-text'
    },
    {
        title: 'Letzter Durchlauf',
        path: '/replay',
        icon: <BsIcons.BsCollectionPlay/>,
        cName: 'analytic-nav-text'
    },
    {
        title: 'Zurück',
        path: '/',
        icon: <BsIcons.BsBackspaceFill/>,
        cName: 'analytic-back'
    },
    
]