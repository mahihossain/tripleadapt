import React, { useRef, Suspense, useState } from "react"
import { useGLTF, Environment } from "@react-three/drei"
import { Canvas } from "@react-three/fiber"

export function WorkPlace(props) {
  const { nodes, materials } = useGLTF('/WorkTable/WorkTable.gltf')
  return (
    <group {...props} dispose={null}>
      <mesh
        geometry={nodes.messSchieber.geometry}
        material={materials.messSchieber}
        position={[-0.601, -0.399, 0]}
        rotation={[3.101, 0, 0]}
        scale={0.001}
      />
      <mesh
        geometry={nodes.Table.geometry}
        material={materials.table}
        scale={0.003}
      />
      <mesh
        geometry={nodes.zylinder.geometry}
        material={materials.boxZylinder}
        position={[1.318, 0.408, 0.705]}
        rotation={[Math.PI / 2, 0, 1.568]}
        scale={0.007}
      />
      <mesh
        geometry={nodes.mutter.geometry}
        material={materials.boxMutter}
        position={[0.616, 0.408, 0.705]}
        rotation={[Math.PI / 2, 0, 1.568]}
        scale={0.007}
      />
      <mesh
        geometry={nodes.kolbenBaugruppe.geometry}
        material={materials.boxkolbenBaugruppe}
        position={[-0.083, 0.408, 0.705]}
        rotation={[Math.PI / 2, 0, 1.568]}
        scale={0.007}
      />
      <mesh
        geometry={nodes.kolbenStange.geometry}
        material={materials.boxkolbenStange}
        position={[-0.789, 0.408, 0.705]}
        rotation={[Math.PI / 2, 0, 1.568]}
        scale={0.007}
      />
      <mesh
        geometry={nodes.abschlussDeckel.geometry}
        material={materials.boxabschlussDeckel}
        position={[-0.566, 0.055, 0.705]}
        rotation={[Math.PI / 2, 0, 1.568]}
        scale={0.007}
      />
      <mesh
        geometry={nodes.bundSchraube.geometry}
        material={materials.boxbundSchraube}
        position={[0.104, 0.055, 0.705]}
        rotation={[Math.PI / 2, 0, 1.568]}
        scale={0.007}
      />
      <mesh
        geometry={nodes.lagerDeckel.geometry}
        material={materials.boxlagerDeckel}
        position={[0.787, 0.055, 0.705]}
        rotation={[Math.PI / 2, 0, 1.568]}
        scale={0.007}
      />
      <mesh
        geometry={nodes.schrauberGelb.geometry}
        material={materials.schrauberGelb}
        position={[-1.474, -0.263, -0.205]}
        rotation={[-1.222, -0.018, -3.068]}
        scale={0.023}
      />
      <mesh
        geometry={nodes.schrauberBlau.geometry}
        material={materials.schrauberBlau}
        position={[-1.474, -0.263, -0.625]}
        rotation={[-1.222, -0.018, -3.068]}
        scale={0.023}
      />
      <mesh
        geometry={nodes.scanner.geometry}
        material={materials.scanner}
        position={[-1.217, -0.393, 0.448]}
        rotation={[-1.609, 0, -0.142]}
        scale={-0.011}
      />
      <group
        position={[0.994, 0.002, 0.54]}
        rotation={[0, 0, -1.366]}
        scale={0.074}
      >
        <mesh
          geometry={nodes.lagerdeckel002.geometry}
          material={materials.lagerdeckel}
        />
        <mesh
          geometry={nodes.lagerdeckel002_1.geometry}
          material={materials.middle}
        />
      </group>
      <group
        position={[0, 0.327, 0.436]}
        rotation={[0, 0, -1.644]}
        scale={-0.056}
      >
        <mesh geometry={nodes.Cube_1.geometry} material={materials.rot} />
        <mesh geometry={nodes.Cube_2.geometry} material={materials.weiß} />
      </group>
      <group
        position={[-0.177, 0.327, 0.45]}
        rotation={[0, 0, -1.644]}
        scale={-0.056}
      >
        <mesh geometry={nodes.Cube001_1.geometry} material={materials.rot} />
        <mesh geometry={nodes.Cube001_2.geometry} material={materials.weiß} />
      </group>
      <group
        position={[-0.177, 0.376, 0.45]}
        rotation={[0, 0, -1.644]}
        scale={-0.056}
      >
        <mesh geometry={nodes.Cube002_1.geometry} material={materials.rot} />
        <mesh geometry={nodes.Cube002_2.geometry} material={materials.weiß} />
      </group>
      <group
        position={[-0.075, 0.376, 0.45]}
        rotation={[0, 0, -1.644]}
        scale={-0.056}
      >
        <mesh geometry={nodes.Cube003_1.geometry} material={materials.rot} />
        <mesh geometry={nodes.Cube003_2.geometry} material={materials.weiß} />
      </group>
      <mesh
        geometry={nodes.Abschlussdeckel001.geometry}
        material={materials.abschlussdeckel}
        position={[-0.7, 0, 0.543]}
        rotation={[-0.191, -0.027, 1.782]}
        scale={0.095}
      />
      <mesh
        geometry={nodes.mutter002.geometry}
        material={materials.mutter}
        position={[0.793, 0.266, 0.489]}
        scale={0.004}
      />
      <mesh
        geometry={nodes.kolbenstange.geometry}
        material={materials.kolbenstange}
        position={[-0.689, 0.392, 0.512]}
        rotation={[-2.043, -0.001, 1.565]}
        scale={-0.004}
      />
      <mesh
        geometry={nodes.Schraube001.geometry}
        material={materials.schraube}
        position={[0.176, 0.027, 0.504]}
        rotation={[0.267, 0.662, -1.468]}
        scale={0.006}
      />
      <mesh
        geometry={nodes.Zylinder001.geometry}
        material={materials.zylinder}
        position={[1.484, 0.386, 0.578]}
        scale={[0.086, 0.077, 0.086]}
      />
    </group>
  )
}

export default function WorkPlaceWithoutAnything() {
  return (
    <div>
      <Canvas shadows dpr={[1, 2]} style={{ width: `50%`, height: `50%`, position: `absolute`, left: 0 }}
        camera={{ position: [0, 3, -4] }}>
        <ambientLight intensity={1} />
        <Suspense fallback={null}>
          <WorkPlace />
          <Environment files="potsdamer_platz_1k.hdr" />
        </Suspense>
      </Canvas>
    </div>
  )
}