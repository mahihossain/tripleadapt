import React, { Component, useEffect, useState } from 'react';
import ReactDOM from "react-dom";
import Graph from 'react-vis-network-graph';
import '../recommendation/Recommendation.css'



function GraphVis(props) {
  const [active, setActive] = useState(false)


    useEffect(() => {
      // console.log(props.nodes)
      var active_node = props.nodes.filter(n => String(n.id) === props.current_activity)[0]
      if (active_node !== undefined) {
        // console.log('Activity vorhanden')
        // console.log(active_node)
        // active_node['group'] = 'active'
        setActive(true)
      }
    });
    
    var events = {
      select: function(event) {
        var { nodes, edges } = event;
      }
    };
  
    var options = {
        width: '100%',
        height: "100%",
        physics: {
            enabled: false,
            barnesHut: {
              "springConstant": 0,
              "avoidOverlap": 0.2
            },
          },
        layout: {
          // hierarchical: {
          //   direction: "LR",
          //   levelSeparation: 180,
          // }
        },
        edges: {
          color: "#000000",
          chosen: false,
        },
        nodes: {
            widthConstraint: 150,
            shape: "box",
            chosen: false,
            color: {
              border: "#000000",
              background: "white"
            },
            font: {
              size: 20,
            },
        },
        groups: {
          active: {
            borderWidth:3,
            color: {
              border: "#0092e2"
              // border: "#000000"
            }
          },
          notactive: {
            borderWidth: 1,
            color: {
              border: "#000000"
            }
          } 
        }
      };

      const renderGraph = (active) => {
        if (!active) {
          return(
            <></>
          )
        } else {
          return (
            <Graph
                graph={{nodes: props.nodes, edges: props.edges}}
                options={options}
                events={events}
                getNetwork={network => {
                  network.stabilize()
                    //  if you want access to vis.js network api you can set the state in a parent component using this property
                  
                }} 
            />
            
            
          )
          
        }
      }
        return (
          <>
            {renderGraph(active)}
          </>
        );
    }
 
export default GraphVis;