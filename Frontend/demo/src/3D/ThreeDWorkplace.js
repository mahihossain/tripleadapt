import React, { useRef, useState, Suspense } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { ContactShadows, Environment, useGLTF, OrbitControls } from '@react-three/drei'
import { proxy, useSnapshot } from 'valtio'

const state = proxy({
  current: null,
  items: {
    Material: '#FFFFFF',
    Material009: '#FFFFFF',
    Material015: '#FFFFFF',
    Material018: '#FFFFFF',
    Material015: '#FFFFFF',
    Material014: '#FFFFFF',
    Material003: '#FFFFFF',
    Material008: '#FFFFFF',
    Material002: '#FFFFFF',
    Material011: '#FFFFFF',
    Material013: '#FFFFFF'
  }
})

function Workplace({ ...props }) {
  const group = useRef()
  const snap = useSnapshot(state)

  const { nodes, materials } = useGLTF('combined_scene_festo_compressed.glb')

  const [hovered, set] = useState(null)

  return (
    <group
      ref={group}
      dispose={null}
      onPointerOver={(e) => (e.stopPropagation(), set(e.object.material.name))}
      onPointerOut={(e) => e.intersections.length === 0 && set(null)}
      onPointerMissed={() => (state.current = null)}
      onClick={(e) => (e.stopPropagation(), (state.current = e.object.material.name))}
      >
      <group ref={group} {...props} dispose={null}>
        <mesh geometry={nodes.Tisch.geometry} material={materials.tisch} position={[-0.23, 0.88, 1.43]} />
        <mesh
          geometry={nodes.scanner.geometry}
          material={materials.scanner}
          position={[-0.37, 1.23, 1.43]}
          rotation={[1.43, 1.51, -2.93]}
          scale={0.002}
        />
        <group position={[-0.15, 1.24, 1.57]} rotation={[0.35, 0, 0]} scale={-0.000286}>
          <mesh geometry={nodes.Verniew_1.geometry} material={materials.al} />
          <mesh geometry={nodes.Verniew_2.geometry} material={materials.Part2} />
        </group>
        <mesh
          geometry={nodes.drill1.geometry}
          material={materials.drill1}
          position={[-0.15, 1.24, 1.45]}
          rotation={[0.08, 0, 0]}
          scale={0.000518}
        />
        <mesh
          geometry={nodes.drill2.geometry}
          material={materials.drill2}
          position={[-0.01, 1.25, 1.45]}
          rotation={[-0.08, 0, 3.08]}
          scale={0.000518}
        />
      </group>
    </group>
  )
}

function Picker() {
  const snap = useSnapshot(state)
  return (
    <div style={{ display: snap.current ? 'block' : 'none' }}>

      {snap.current}
    </div>
  )
}

export default function ThreeDWorkplace() {
  return (
    <>
      <Picker />
      <Canvas shadows dpr={[1, 2]} camera={{ position: [-0.1, 1.8, 2.1] }}>
        <ambientLight intensity={-0.1} />
        <spotLight intensity={0.5} angle={0.1} penumbra={1} position={[10, 15, 10]} castShadow />
        <Suspense fallback={null}>
          <Workplace />
          <Environment preset="warehouse" />
        </Suspense>
        {/* <OrbitControls minPolarAngle={Math.PI / 40} maxPolarAngle={Math.PI / 1} enableZoom={true} enablePan={false} /> */}
      </Canvas>
    </>
  )
}
