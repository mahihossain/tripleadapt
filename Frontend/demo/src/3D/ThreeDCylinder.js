import React, { useRef, useState, Suspense, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { ContactShadows, Environment, useGLTF, OrbitControls } from '@react-three/drei';
import { proxy, useSnapshot } from 'valtio';
import { HexColorPicker } from 'react-colorful';
import { useGesture, useDrag } from "react-use-gesture"
import axios from "axios";
import { useQuery } from "react-query";


const state = proxy({
  current: null,
  items: {
    Material: '#FFFFFF',
    Material009: '#FFFFFF',
    Material015: '#FFFFFF',
    Material018: '#FFFFFF',
    Material016: '#FFFFFF',
    Material014: '#FFFFFF',
    Material003: '#FFFFFF',
    Material008: '#FFFFFF',
    Material002: '#FFFFFF',
    Material011: '#FFFFFF',
    Material013: '#FFFFFF',
    Material001: '#FFFFFF',
    Material010: '#FFFFFF',
    Material017: '#FFFFFF',
    Material019: '#FFFFFF'

  }
})

const materials = {
  "Abschlussdeckel": ["Material"],
  "Mutter": [
    "Material017",
    "Material013",
    "Material015",
    "Material014",
    "Material003",
    "Material016",
    "Material018",
    "Material019"
  ],
  "Kolbenstange": ["Material001"],
  "Kolbenbaugruppe": [
    "Material011",
    "Material009",
    "Material010",
    "Material002"
  ]

}

function getRandomArbitrary(min, max) {
  return Math.random() * (max - min) + min;
}

function Cylinder({ ...props }) {
  const group = useRef()
  const snap = useSnapshot(state)
  const intPos = getRandomArbitrary(0, 3)
  const [position, setPosition] = useState([intPos, intPos, intPos]);
  const { size, viewport } = useThree()
  const aspect = size.width / viewport.width
  const bind = useDrag(({ offset: [x, y] }) => {
    const [, , z] = position;
    setPosition([x / aspect, -y / aspect, z]);
  }, { pointerEvents: true });

  const { nodes, materials } = useGLTF('full_C.glb')
  useFrame((state) => {
    const t = state.clock.getElapsedTime()
    group.current.rotation.z = -0.2 - (1 + Math.sin(t / 1.5)) / 20
    group.current.rotation.x = Math.cos(t / 4) / 8
    group.current.rotation.y = Math.sin(t / 4) / 8
    group.current.position.y = (1 + Math.sin(t / 1.5)) / 10
  })

  const [hovered, set] = useState(null)

  return (
    <group
      ref={group}
      dispose={null}
      onPointerOver={(e) => (e.stopPropagation(), set(e.object.material.name))}
      onPointerOut={(e) => e.intersections.length === 0 && set(null)}
      onPointerMissed={() => (state.current = null)}
      onClick={(e) => (e.stopPropagation(), (state.current = e.object.material.name))}
      {...bind()}>

      {/* onClick={(e) => console.log(e.object.material.name)}> */}
      <group ref={group} {...props} dispose={null} {...bind}>
        <mesh
          geometry={nodes.Cylinder009.geometry}
          material={materials.Material013}
          position={[0.55, -0.53, -4.18]}
          rotation={[Math.PI / 2, 0, 0]}
          scale={0.25}
          material-color={snap.items.Material013}
        >
          <mesh
            geometry={nodes.Cylinder010.geometry}
            material={materials.Material015}
            position={[-4.81, 0, 0]}
            material-color={snap.items.Material015}
          />
          <mesh
            geometry={nodes.Cylinder011.geometry}
            material={materials.Material014}
            position={[-4.81, 0, -4.6]}
            material-color={snap.items.Material014}
          />
          <mesh
            geometry={nodes.Cylinder012.geometry}
            material={materials.Material003}
            position={[-0.02, 0, -4.6]}
            material-color={snap.items.Material003}
          />
        </mesh>
        <mesh
          geometry={nodes.Cylinder008.geometry}
          material={materials.Material019}
          position={[0.55, -0.53, 3.73]}
          rotation={[Math.PI / 2, 0, 0]}
          scale={0.25}
          material-color={snap.items.Material019}
        >
          <mesh
            geometry={nodes.Cylinder005.geometry}
            material={materials.Material017}
            position={[-0.02, 0, -4.6]}
            material-color={snap.items.Material017}
          />
          <mesh
            geometry={nodes.Cylinder006.geometry}
            material={materials.Material016}
            position={[-4.81, 0, -4.6]}
            material-color={snap.items.Material016}
          />
          <mesh
            geometry={nodes.Cylinder007.geometry}
            material={materials.Material018}
            position={[-4.81, 0, 0]}
            material-color={snap.items.Material018}
          />
        </mesh>
        <mesh
          geometry={nodes.Cylinder004.geometry}
          material={materials.Material011}
          position={[0.33, -0.52, 0]}
          rotation={[Math.PI / 2, 0, 0]}
          scale={[0.13, 4.26, 0.13]}
          material-color={snap.items.Material011}
        />
        <mesh
          geometry={nodes.Cylinder003.geometry}
          material={materials.Material002}
          position={[-0.88, -0.52, 0]}
          rotation={[Math.PI / 2, 0, 0]}
          scale={[0.13, 4.26, 0.13]}
          material-color={snap.items.Material002}
        />
        <mesh
          geometry={nodes.Cylinder002.geometry}
          material={materials.Material010}
          position={[-0.88, 0.63, 0]}
          rotation={[Math.PI / 2, 0, 0]}
          scale={[0.13, 4.26, 0.13]}
          material-color={snap.items.Material010}
        />
        <mesh
          geometry={nodes.Cylinder001.geometry}
          material={materials.Material009}
          position={[0.34, 0.63, 0]}
          rotation={[Math.PI / 2, 0, 0]}
          scale={[0.13, 4.26, 0.13]}
          material-color={snap.items.Material009}
        />
        <group position={[-0.04, 0.01, 0]} rotation={[Math.PI / 2, 0, 0]} scale={[0.54, 4.04, 0.54]}>
          <mesh geometry={nodes.Cylinder_1.geometry} material={materials.Material001} material-color={snap.items.Material001} />
          <mesh geometry={nodes.Cylinder_2.geometry} material={materials.Material008} material-color={snap.items.Material008} />
        </group>
        <mesh
          geometry={nodes.Cube001.geometry}
          material={nodes.Cube001.material}
          position={[-0.04, 0, 4.32]}
          material-color={snap.items.Material}
        />
        <mesh
          geometry={nodes.Cube.geometry}
          material={nodes.Cube.material}
          position={[-0.04, 0, -2.39]}
          material-color={snap.items.Material}
        />
      </group>
    </group>
  )
}

function Picker() {
  const snap = useSnapshot(state)
  //Code for Fetching the Updates from /update endpoint
  // const fetchUpdates = () => {
  //   return axios.get('/update')
  // }

  // const { data, isLoading, isError, error, isFetching, isFetched } = useQuery(
  //   'update',
  //   fetchUpdates,
  //   {
  //     refetchInterval: 5000,
  //     refetchIntervalInBackground: true,
  //   }
  // )

  // useEffect(() => {
  //   if (isFetched) {
  //     const updateData = new Object(...data?.data.nodes) 
  //     let name = new String(updateData.name)
  //     name = name.split(' ')[0]
  //     if(data.data.nodes.length){
  //     for(let x in materials){
  //       if(x === name){
  //         materials[x].forEach(element => {
  //           state.items[element] = '#ED9b0C' 
  //         });
  //       }
  //       else
  //         materials[x].forEach(element => {
  //           state.items[element] = "#FFFFFF"
  //         });
  //     }
  //   }
  //   }
  // })

  return (
    <div style={{ display: snap.current ? 'block' : 'none' }}>

      {/* <HexColorPicker className="picker" color={snap.items[snap.current]} onChange={(color) => (state.items[snap.current] = color)} /> */}

      {/* {snap.items[snap.current]} */}
      {snap.current}
    </div>
  )
}

export default function ThreeDCylinder() {
  return (
    <>
      <Picker />
      <Canvas shadows dpr={[1, 2]} camera={{ position: [0, -10, -10], fov: 50 }}>
        <ambientLight intensity={0.7} />
        <spotLight intensity={0.5} angle={0.1} penumbra={1} position={[10, 15, 10]} castShadow />
        <Suspense fallback={null}>
          <Cylinder />
          <Environment preset="city" />
        </Suspense>
        <OrbitControls minPolarAngle={Math.PI / 40} maxPolarAngle={Math.PI / 1} enableZoom={true} enablePan={false} />
      </Canvas>
    </>
  )
}
