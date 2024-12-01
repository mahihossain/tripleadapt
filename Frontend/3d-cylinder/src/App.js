import React, { useRef, useState, Suspense } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { ContactShadows, Environment, useGLTF, OrbitControls } from '@react-three/drei'
import { proxy, useSnapshot } from 'valtio'

const state = proxy({
  current: null,
  items: {
    material1: '#0330fc',
    material2: '#fc033d'
  }
})

function Cylinder({ ...props }) {
  const group = useRef()
  const snap = useSnapshot(state)

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
      {...props}
      dispose={null}
      dispose={null}
      onPointerOver={(e) => (e.stopPropagation(), set(e.object.material.name))}
      onPointerOut={(e) => e.intersections.length === 0 && set(null)}
      onPointerMissed={() => (state.current = null)}
      onClick={(e) => (e.stopPropagation(), (state.current = e.object.material.name))}>
      <group ref={group} {...props} dispose={null}>
        <mesh
          geometry={nodes.Cylinder009.geometry}
          material={materials['Material.013']}
          position={[0.55, -0.53, -4.18]}
          rotation={[Math.PI / 2, 0, 0]}
          scale={0.25}>
          <mesh geometry={nodes.Cylinder010.geometry} material={materials['Material.015']} position={[-4.81, 0, 0]} />
          <mesh geometry={nodes.Cylinder011.geometry} material={materials['Material.014']} position={[-4.81, 0, -4.6]} />
          <mesh geometry={nodes.Cylinder012.geometry} material={materials['Material.003']} position={[-0.02, 0, -4.6]} />
        </mesh>
        <mesh
          geometry={nodes.Cylinder008.geometry}
          material={materials['Material.019']}
          position={[0.55, -0.53, 3.73]}
          rotation={[Math.PI / 2, 0, 0]}
          scale={0.25}>
          <mesh geometry={nodes.Cylinder005.geometry} material={materials['Material.017']} position={[-0.02, 0, -4.6]} />
          <mesh geometry={nodes.Cylinder006.geometry} material={materials['Material.016']} position={[-4.81, 0, -4.6]} />
          <mesh geometry={nodes.Cylinder007.geometry} material={materials['Material.018']} position={[-4.81, 0, 0]} />
        </mesh>
        <mesh
          geometry={nodes.Cylinder004.geometry}
          material={materials['Material.011']}
          position={[0.33, -0.52, 0]}
          rotation={[Math.PI / 2, 0, 0]}
          scale={[0.13, 4.26, 0.13]}
        />
        <mesh
          geometry={nodes.Cylinder003.geometry}
          material={materials['Material.002']}
          position={[-0.88, -0.52, 0]}
          rotation={[Math.PI / 2, 0, 0]}
          scale={[0.13, 4.26, 0.13]}
        />
        <mesh
          geometry={nodes.Cylinder002.geometry}
          material={materials['Material.010']}
          position={[-0.88, 0.63, 0]}
          rotation={[Math.PI / 2, 0, 0]}
          scale={[0.13, 4.26, 0.13]}
        />
        <mesh
          geometry={nodes.Cylinder001.geometry}
          material={materials['Material.009']}
          position={[0.34, 0.63, 0]}
          rotation={[Math.PI / 2, 0, 0]}
          scale={[0.13, 4.26, 0.13]}
        />
        <group position={[-0.04, 0.01, 0]} rotation={[Math.PI / 2, 0, 0]} scale={[0.54, 4.04, 0.54]}>
          <mesh geometry={nodes.Cylinder_1.geometry} material={materials['Material.001']} />
          <mesh geometry={nodes.Cylinder_2.geometry} material={materials['Material.008']} />
        </group>
        <mesh geometry={nodes.Cube001.geometry} material={nodes.Cube001.material} position={[-0.04, 0, 4.32]} />
        <mesh geometry={nodes.Cube.geometry} material={nodes.Cube.material} position={[-0.04, 0, -2.39]} />
      </group>
    </group>
  )
}

function Picker() {
  const snap = useSnapshot(state)
  return <div className="picker">{snap.current}</div>
}

export default function App() {
  return (
    <>
      <Picker />
      <Canvas>
        <ambientLight intensity={0.7} />
        <spotLight intensity={0.5} angle={0.1} penumbra={1} position={[10, 15, 10]} castShadow />
        <Suspense fallback={null}>
          <Cylinder />
        </Suspense>
        <OrbitControls minPolarAngle={Math.PI / 40} maxPolarAngle={Math.PI / 1} enableZoom={true} enablePan={false} />
      </Canvas>
    </>
  )
}
