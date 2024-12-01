/*
Auto-generated by: https://github.com/pmndrs/gltfjsx
*/

import React, { useRef } from 'react'
import { useGLTF } from '@react-three/drei'

export function Model(props) {
  const { nodes, materials } = useGLTF('/Baugruppe.gltf')
  return (
    <group {...props} dispose={null}>
      <mesh geometry={nodes.baugruppe.geometry} material={materials.rot} />
      <mesh geometry={nodes.baugruppe_1.geometry} material={materials.weiß} />
    </group>
  )
}

useGLTF.preload('/Baugruppe.gltf')