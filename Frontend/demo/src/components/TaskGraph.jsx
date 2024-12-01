import React, { Component } from 'react';
import { Card } from '@mui/material';
import GraphVis from './GraphVis.jsx';
import axios from 'axios';
import graphPng from '../images/graph.png'
import { useEffect } from 'react';

function TaskGraph(props) {
    
  //ComponentDidMount
    useEffect(() => {
        axios.get('/model').then(data => {
            console.log(data.data)
            props.onNewGraph(data.data['init_model'].nodes, data.data['init_model'].edges, "Activity_0h4egt6")
            props.onLoading(data.data['init_model'].task_id)
        })
    },[])


    //ComponentDidUpdate
    useEffect(() => {
      // console.log(props.nodes)
      // console.log(props.edges)
      // props.onNewGraph(props.nodes, props.edges)
      // // console.log('TaskGraph')
      //   // console.log(prevProps)
      //   // console.log(prevProps['nodes'])
      //   // console.log(props.nodes)
      //   // console.log(prevProps['edges'])
      //   // console.log(props.edges)
      //   if (prevProps.nodes !== props.nodes && prevProps.edges !== props.edges) {
      //     // setState({
      //     //     nodes: props.nodes,
      //     //     edges: props.edges
      //     // })
      //     props.onNewGraph(props.nodes, props.edges)
      // }
    })  

    const loading = ( isLoading ) => {
        if (isLoading) {
            return (  
              <>  
                {/* <Card>
                    <button onClick={testUpdate}> Test Update </button>
                    <button onClick={startTest}> Start Test </button>
                    <button onClick={stopUpdate}> Stop Update </button>
                </Card> */}
                <img className='GraphPng' src={graphPng} alt='Graph' />
              </>
            );
        }
        else {
            return (    
                <>
                    <GraphVis
                    nodes={props.nodes}
                    edges={props.edges}
                    current_activity= {props.current_activity}
                    />
                </>
            );
        }
    }
    return(
            loading(props.isLoading)
        )
    }

export default TaskGraph;