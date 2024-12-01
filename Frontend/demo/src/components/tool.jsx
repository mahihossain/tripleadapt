import React, { Component } from 'react'
import "./styles.css"

class Tool extends Component { 
    render() { 
        const { selected, tool, onIncrement, onDelete, onSelect} = this.props
        return (
            <div onClick = {() => onSelect(tool.id)} id = {tool.id} className={selected === tool.id ? "active" : "inactive"} style={{height: 60}}>
                {this.props.children}
            </div>
        );
    }
}
 
export default Tool;