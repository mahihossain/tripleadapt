import React, { Component } from 'react'

class TaskVis extends Component {
    state = { } 

    handleTask = () => {
        //console.log(this.props.Tasks)
        //console.log(this.props.TaskID)
        //console.log(typeof(this.props.TaskID))
        var x = this.props.Tasks.filter(t => t.task_id === this.props.current_task)
        //console.log(x)
        if (x.length === 0) {
            return ""
        } else {
            return x[0].task_name
        }
        
    }

    loading( isLoading ) {
        if (isLoading) {
            return (    
                <div>
                    <p>  </p>
                </div>
            );
        }
        else {
            return (    
                <div>
                    <h5> {this.handleTask()} </h5>  
                </div>
            );
        }
    }

    render() {
        const { current_task, Tasks, isLoading} = this.props
        return ( this.loading(isLoading));
    }
}
 
export default TaskVis;