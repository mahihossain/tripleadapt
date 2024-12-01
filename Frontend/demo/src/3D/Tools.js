import React, { Suspense, useState } from "react";
import {
    useGLTF,
    OrbitControls,
    Environment,
} from "@react-three/drei";
import { Canvas, useThree } from "@react-three/fiber";
import { useDrag } from "react-use-gesture";

export function Schrauber({ ...props }) {

    const [position, setPosition] = useState([0, 5, -6]);
    const { size, viewport } = useThree()
    const aspect = size.width / viewport.width
    const bind = useDrag(({ offset: [z] }) => {
        const [x, y,] = position;
        setPosition([x / aspect, -y / aspect, z / aspect]);
    }, { pointerEvents: true });

    const { nodes, materials } = useGLTF('/Schrauber.gltf')
    if (props.blue) {
        return (
            <mesh geometry={nodes.m_Drill_OBJ.geometry} material={materials.Material__25} material-color='#0000FF'
                position={position} rotation={[-Math.PI / 2, 0, -0.37]} scale={.5} {...bind()} />
        )

    }
    else if (props.green) {
        return (
            <mesh geometry={nodes.m_Drill_OBJ.geometry} material={materials.Material__25} material-color='#228B22'
                position={position} rotation={[-Math.PI / 2, 0, -0.37]} scale={.5} {...bind()} />
        )
    }
    else if (props.grey) {
        return (
            <mesh geometry={nodes.m_Drill_OBJ.geometry} material={materials.Material__25} material-color='#708090'
                position={position} rotation={[-Math.PI / 2, 0, -0.37]} scale={.5} {...bind()} />
        )
    }
    else {
        return (
            <mesh>

            </mesh>
        )
    }
}

export function Messschieber({ ...props }) {
    const { nodes, materials } = useGLTF('/messschieber.gltf')
    const [position, setPosition] = useState([0, 5, -6]);
    const { size, viewport } = useThree()
    const aspect = size.width / viewport.width
    const bind = useDrag(({ offset: [z] }) => {
        const [x, y,] = position;
        setPosition([x / aspect, -y / aspect, z / aspect]);
    }, { pointerEvents: true });
    if (props.appear) {
        return (
            <mesh {...props} dispose={null} scale={.03}>
                <mesh position={position} rotation={[Math.PI / 2, 0, 0]} {...bind()}>
                    <mesh geometry={nodes.Verniew_1.geometry} material={materials.al} />
                    <mesh geometry={nodes.Verniew_2.geometry} material={materials['Part2:color:128:128:128']} />
                </mesh>
            </mesh>
        )
    }
    else {
        return (
            <mesh>

            </mesh>
        )
    }
}



export default function Tools({ data }) {
    return (
        <div className="App">
            <Canvas shadows dpr={[1, 2]} camera={{ position: [-20, 0, -5] }}>
                <ambientLight intensity={1} />
                <Suspense fallback={null}>
                    <Environment preset="city" />
                </Suspense>
                <OrbitControls
                    minPolarAngle={Math.PI / 40}
                    maxPolarAngle={Math.PI / 1}
                    enableZoom={true}
                    enablePan={false}
                />
            </Canvas>
        </div>
    );
}