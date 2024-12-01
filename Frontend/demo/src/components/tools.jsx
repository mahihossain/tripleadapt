import React, { Component } from 'react'
import Tool from './tool'
import CardMedia from '@mui/material/CardMedia';
import 'bootstrap/dist/css/bootstrap.css';
import "./styles.css"

class Tools extends Component {
    putIcon = (toolName) => {
        switch(toolName) {
            case 'screwdriver':
                return (
                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-screwdriver" viewBox="0 0 16 16">
                    <path d="M0 .995.995 0l3.064 2.19a.995.995 0 0 1 .417.809v.07c0 .264.105.517.291.704l5.677 5.676.909-.303a.995.995 0 0 1 1.018.24l3.338 3.339a.995.995 0 0 1 0 1.406L14.13 15.71a.995.995 0 0 1-1.406 0l-3.337-3.34a.995.995 0 0 1-.24-1.018l.302-.909-5.676-5.677a.995.995 0 0 0-.704-.291H3a.995.995 0 0 1-.81-.417L0 .995Zm11.293 9.595a.497.497 0 1 0-.703.703l2.984 2.984a.497.497 0 0 0 .703-.703l-2.984-2.984Z"/>
                </svg>)
            case 'wrench':
                return (
                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-wrench" viewBox="0 0 16 16">
                    <path d="M.102 2.223A3.004 3.004 0 0 0 3.78 5.897l6.341 6.252A3.003 3.003 0 0 0 13 16a3 3 0 1 0-.851-5.878L5.897 3.781A3.004 3.004 0 0 0 2.223.1l2.141 2.142L4 4l-1.757.364L.102 2.223zm13.37 9.019.528.026.287.445.445.287.026.529L15 13l-.242.471-.026.529-.445.287-.287.445-.529.026L13 15l-.471-.242-.529-.026-.287-.445-.445-.287-.026-.529L11 13l.242-.471.026-.529.445-.287.287-.445.529-.026L13 11l.471.242z"/>
                </svg>)
            case 'hammer':
                return(
                    <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-hammer" viewBox="0 0 16 16">
                    <path d="M9.972 2.508a.5.5 0 0 0-.16-.556l-.178-.129a5.009 5.009 0 0 0-2.076-.783C6.215.862 4.504 1.229 2.84 3.133H1.786a.5.5 0 0 0-.354.147L.146 4.567a.5.5 0 0 0 0 .706l2.571 2.579a.5.5 0 0 0 .708 0l1.286-1.29a.5.5 0 0 0 .146-.353V5.57l8.387 8.873A.5.5 0 0 0 14 14.5l1.5-1.5a.5.5 0 0 0 .017-.689l-9.129-8.63c.747-.456 1.772-.839 3.112-.839a.5.5 0 0 0 .472-.334z"/>
                    </svg>
                )
            default:
                return <div>no picture</div>
        }
        
    }
    
    render() { 
        const { onSelect, onReset, onDelete, onIncrement, tools, selected } = this.props
        return ( 
            <div>
                <div>
                    <span> </span>
                </div> 
                { tools.map(tool => (
                    <Tool 
                        key={tool.id} 
                        onDelete={onDelete} 
                        onIncrement={onIncrement}
                        tool = {tool}
                        onSelect = {onSelect}
                        selected = {selected}>
                        <div className='tools'> 
                            ID:{tool.id}
                            {this.putIcon(tool.value)}
                            <span> </span>
                            <toolname>{tool.value}</toolname><span> </span>
                            <toolsize>{tool.size}</toolsize>
                        </div>
                            
                    </Tool>
                ))}
            </div>);
    }
}
 
export default Tools;