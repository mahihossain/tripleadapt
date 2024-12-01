import React, { Suspense, useRef, useState } from "react"
import {
  useGLTF,
  OrbitControls,
  Environment,
} from "@react-three/drei"
import { Canvas, useThree, useFrame } from "@react-three/fiber"
import { useDrag } from "react-use-gesture"
import { Schrauber, Messschieber } from "./Tools"


function ToggleButton({ isOn, handleClick }) {
  const sliderStyles = {
    position: 'relative',
    display: 'inline-block',
    width: '60px',
    height: '34px',
    margin: '10px'
  }

  const switchStyles = {
    position: 'absolute',
    cursor: 'pointer',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: isOn ? '#8ADF28' : '#ccc',
    transition: '.4s',
    borderRadius: '34px'
  }

  const circleStyles = {
    position: 'absolute',
    height: '26px',
    width: '26px',
    left: isOn ? '15px' : '-10px', // Adjust position based on the toggle state
    bottom: '4px',
    backgroundColor: 'white',
    transition: '.4s',
    borderRadius: '50%'
  }

  return (
    <div style={sliderStyles} onClick={handleClick}>
      <div style={switchStyles}>
        <span style={circleStyles}></span>
      </div>
    </div>
  )
}


function Cylinder({ onDoubleClick, ...props }) {
  const { nodes, materials } = useGLTF('/Zylinder_ad_ld/Cylinder_ad_ld.gltf')
  const [position, setPosition] = useState([0, 0, 0])
  const { size, viewport } = useThree()
  const aspect = size.width / viewport.width
  const adRef = useRef()

  const bind = useDrag(({ offset: [z] }) => {
    const [x, y,] = position
    setPosition([x / aspect, -y / aspect, z / aspect])
  }, { pointerEvents: true })

  if (props.appear) {
    return (
      <mesh geometry={nodes.Zylinder.geometry} material={materials.zylinder}
        position={position} rotation={[0, 0, 0]} scale={4.3} />
    )
  }
  else {
    return (
      <mesh>

      </mesh>
    )
  }

}

function Abschlussdeckel({ ...props }) {
  const { nodes, materials } = useGLTF('/Zylinder_ad_ld/Cylinder_ad_ld.gltf')
  const [position, setPosition] = useState([4, 8, -1])
  const { size, viewport } = useThree()
  const aspect = size.width / viewport.width
  const bind = useDrag(({ offset: [x] }) => {
    const [, y, z] = position
    setPosition([x / aspect, -y / aspect, z / aspect])
  }, { pointerEvents: true })

  var matColor = '#E6241D'
  var flag = false

  if (position[2] > -2 && position[2] < 0) {
    matColor = '#8ADF28'
    if (position[0] < -12) {
      flag = true
      props.putAbschlussdeckel()
    }
  }

  if (props.appear && flag) {
    return (
      <mesh geometry={nodes.Abschlussdeckel.geometry} material={materials.abschlussdeckel}
        position={position} rotation={[2.5 * Math.PI, 1.0033888 * Math.PI, 0.0081555 * Math.PI]} scale={4.3} material-color={matColor} />
    )
  }
  else if (props.appear) {
    return (
      <mesh geometry={nodes.Abschlussdeckel.geometry} material={materials.abschlussdeckel}
        material-color={matColor} position={position} rotation={[2.5 * Math.PI, 1.0033888 * Math.PI, 0.0081555 * Math.PI]}
        scale={4.3} {...bind()} />
    )
  }
  else {
    return (
      <mesh>

      </mesh>
    )
  }

}

function Kolbenstange({ ...props }) {
  const { nodes, materials } = useGLTF('/Zylinder_ad_ld/Cylinder_ad_ld.gltf')
  const [position, setPosition] = useState([-10, 10, -5])
  const { size, viewport } = useThree()
  const aspect = size.width / viewport.width
  const bind = useDrag(({ offset: [x] }) => {
    const [, y, z] = position
    setPosition([x / aspect, -y / aspect, z / aspect])
  }, { pointerEvents: true })

  var matColor = '#E6241D'
  var flag = false

  if (position[2] > -2 && position[2] < 0) {
    matColor = '#8ADF28'
    if (position[2] > -0.33 && position[2] < 0) {
      flag = true
      props.putKolbenstange()
    }
  }

  if (props.appear && flag) {
    return (
      <mesh geometry={nodes.kolbenstange.geometry} material={materials.kolbenstange}
        position={position} rotation={[2.5 * Math.PI, 0 * Math.PI, 1.5 * Math.PI]} scale={.17} />
    )
  }
  else if (props.appear) {
    return (
      <mesh geometry={nodes.kolbenstange.geometry} material={materials.kolbenstange}
        material-color={matColor} position={position} rotation={[2.5 * Math.PI, 0 * Math.PI, 1.5 * Math.PI]}
        scale={.17} {...bind()} />
    )
  }
  else {
    return (
      <mesh>

      </mesh>
    )
  }


}

function Lagerdeckel({ ...props }) {
  const { nodes, materials } = useGLTF('/Zylinder_ad_ld/Cylinder_ad_ld.gltf')
  const [position, setPosition] = useState([0.1, 8, -1])
  const { size, viewport } = useThree()
  const aspect = size.width / viewport.width
  const bind = useDrag(({ offset: [x] }) => {
    const [, y, z] = position
    setPosition([x / aspect, -y / aspect, z / aspect])
  }, { pointerEvents: true })


  var matColor = '#E6241D'
  var flag = false

  if (position[2] > -2 && position[2] < 0) {
    matColor = '#8ADF28'
    if (position[0] > 3) {
      flag = true
      props.putLagerdeckel()
    }
  }


  if (props.appear && flag) {
    return (
      <mesh position={position} rotation={[1.5 * Math.PI, 1.00633 * Math.PI, 1 * Math.PI]} scale={4.3} material-color={matColor}>
        <mesh geometry={nodes.lagerdeckel.geometry} material={materials.lagerdeckel} />
        <mesh geometry={nodes.lagerdeckel_1.geometry} material={materials.middle} />
      </mesh>
    )
  }
  else if (props.appear) {
    return (
      <mesh position={position} rotation={[1.5 * Math.PI, 1.00633 * Math.PI, 1 * Math.PI]} scale={4.3} {...bind()} material-color={matColor}>
        <mesh geometry={nodes.lagerdeckel.geometry} material={materials.lagerdeckel} />
        <mesh geometry={nodes.lagerdeckel_1.geometry} material={materials.middle} />
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

function Baugruppe({ ...props }) {
  const { nodes, materials } = useGLTF('/Zylinder_ad_ld/Cylinder_ad_ld.gltf')
  const [position, setPosition] = useState([0.1, 8, -1])
  const { size, viewport } = useThree()
  const aspect = size.width / viewport.width
  const bind = useDrag(({ offset: [x] }) => {
    const [, y, z] = position
    setPosition([x / aspect, -y / aspect, z / aspect])
  }, { pointerEvents: true })


  var matColor = '#E6241D'
  var flag = false

  if (position[2] > -2 && position[2] < 0) {
    matColor = '#8ADF28'
    if (position[0] < -10) {
      flag = true
      props.putKolbenbaugruppe()
    }
  }

  if (props.appear && flag) {
    return (
      <mesh {...props} position={position} rotation={[0, 0, 0]} dispose={null} scale={2.3} material-color={matColor}>
        <mesh geometry={nodes.baugruppe.geometry} material={materials.rot} />
        <mesh geometry={nodes.baugruppe_1.geometry} material={materials.weiß} />
      </mesh>
    )
  }
  else if (props.appear) {
    return (
      <mesh {...props} position={position} rotation={[0, 0, 0]} dispose={null} scale={2.3} {...bind()} material-color={matColor}>
        <mesh geometry={nodes.baugruppe.geometry} material={materials.rot} />
        <mesh geometry={nodes.baugruppe_1.geometry} material={materials.weiß} />
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


function Schraube({ ...props }) {
  const { nodes, materials } = useGLTF('/Schraube.gltf')
  const { size, viewport } = useThree()
  const aspect = size.width / viewport.width
  const [positionOne, setPositionOne] = useState([8, -2.5, 2.5])
  const bindOne = useDrag(({ offset: [x] }) => {
    const [, y, z] = positionOne
    setPositionOne([x / aspect, y, z])
  }, { pointerEvents: true })

  const [positionTwo, setPositionTwo] = useState([8, 2.5, -2.5])
  const bindTwo = useDrag(({ offset: [x] }) => {
    const [, y, z] = positionTwo
    setPositionTwo([x / aspect, y, z])
  }, { pointerEvents: true })

  const [positionThree, setPositionThree] = useState([-20, 2.5, 2.5])
  const bindThree = useDrag(({ offset: [x] }) => {
    const [, y, z] = positionThree
    setPositionThree([x / aspect, y, z])
  }, { pointerEvents: true })

  const [positionFour, setPositionFour] = useState([-20, -2.3, -2.3])
  const bindFour = useDrag(({ offset: [x] }) => {
    const [, y, z] = positionFour
    setPositionFour([x / aspect, y, z])
  }, { pointerEvents: true })

  const rotateMesh = React.useRef()
  useFrame(({ clock }) => {
    // rotateMesh.current.rotation.x = clock.elapsedTime() 
  })

  if (props.appearOne) {
    console.log(positionOne)
    if (positionOne[0] < 4 && positionOne[0] > 3) {
      return (
        <mesh geometry={nodes.Schraube.geometry} material={materials.schraube}
          position={positionOne} rotation={[1 * Math.PI, 1 * Math.PI, .5 * Math.PI]} scale={.3}
          ref={rotateMesh} />
      )
    }
    else {
      return (
        <mesh geometry={nodes.Schraube.geometry} material={materials.schraube}
          position={positionOne} rotation={[1 * Math.PI, 1 * Math.PI, .5 * Math.PI]} scale={.3} ref={rotateMesh} {...bindOne()} />
      )
    }
  }
  else if (props.appearTwo) {
    if (positionTwo[0] < 4 && positionTwo[0] > 3) {
      return (
        <mesh geometry={nodes.Schraube.geometry} material={materials.schraube}
          position={positionTwo} rotation={[1 * Math.PI, 1 * Math.PI, .5 * Math.PI]} scale={.3} />
      )
    }
    else {
      return (
        <mesh geometry={nodes.Schraube.geometry} material={materials.schraube}
          position={positionTwo} rotation={[1 * Math.PI, 1 * Math.PI, .5 * Math.PI]} scale={.3} {...bindTwo()} />
      )
    }
  }
  else if (props.appearThree) {
    if (positionThree[0] < -12 && positionThree[0] > -13) {
      return (
        <mesh geometry={nodes.Schraube.geometry} material={materials.schraube}
          position={positionThree} rotation={[1 * Math.PI, 0 * Math.PI, .5 * Math.PI]} scale={.3} />
      )
    }
    else {
      return (
        <mesh geometry={nodes.Schraube.geometry} material={materials.schraube}
          position={positionThree} rotation={[1 * Math.PI, 0 * Math.PI, .5 * Math.PI]} scale={.3} {...bindThree()} />
      )
    }
  }
  else if (props.appearFour) {
    if (positionFour[0] < -12 && positionFour[0] > -13) {
      return (
        <mesh geometry={nodes.Schraube.geometry} material={materials.schraube}
          position={positionFour} rotation={[1 * Math.PI, 0 * Math.PI, .5 * Math.PI]} scale={.3} />
      )
    }
    else {
      return (
        <mesh geometry={nodes.Schraube.geometry} material={materials.schraube}
          position={positionFour} rotation={[1 * Math.PI, 0 * Math.PI, .5 * Math.PI]} scale={.3} {...bindFour()} />
      )
    }
  }
  else {
    return (
      <mesh>

      </mesh>
    )
  }

}

function Mutter({ ...props }) {
  const { nodes, materials } = useGLTF('/Zylinder_ad_ld/Cylinder_ad_ld.gltf')
  const [position, setPosition] = useState([0, 5, -6])
  const { size, viewport } = useThree()
  const aspect = size.width / viewport.width
  const bind = useDrag(({ offset: [z] }) => {
    const [x, y,] = position
    setPosition([x / aspect, -y / aspect, z / aspect])
  }, { pointerEvents: true })


  var matColor = '#E6241D'
  var flag = false


  if (position[2] > -4 && position[2] < 2) {
    matColor = '#8ADF28'
    if (position[2] > -0.33 && position[2] < 0) {
      flag = true
      props.putMutter()

    }
  }

  if (props.appear && flag) {
    return (
      <mesh geometry={nodes.mutter.geometry} material={materials.mutter}
        position={position} rotation={[-1.004444 * Math.PI, 0.004444 * Math.PI, -1.5 * Math.PI]} scale={0.1} />
    )
  }
  else if (props.appear) {
    return (
      <mesh geometry={nodes.mutter.geometry} material={materials.mutter}
        material-color={matColor} position={position} rotation={[-1.004444 * Math.PI, 0.004444 * Math.PI, -1.5 * Math.PI]}
        scale={0.1} {...bind()} />
    )
  }
  else {
    return (
      <mesh>

      </mesh>
    )
  }

}


export default function InteractiveCylinder({ data, ...props }) {

  const [enableOrbit, setEnableOrbit] = useState(false)

  const handleToggleOrbit = () => {
    setEnableOrbit(prevEnableOrbit => !prevEnableOrbit)
  }

  const toggleButtonContainerStyle = {
    position: 'absolute',
    top: 0,
    right: 0,
    padding: '10px', // Adjust padding as needed
    zIndex: 1000 // Make sure it's above other elements
  }

  const messageStyle = {
    position: 'absolute',
    bottom: 0,
    width: '100%',
    textAlign: 'center',
    color: enableOrbit ? '#8ADF28' : '#E6241D', // Green when on, red when off
    padding: '10px',
    fontSize: '20px',
    zIndex: 1000
  }


  return (
    <div className="interactiveCylinder">
      <div style={toggleButtonContainerStyle}>
        <ToggleButton
          isOn={enableOrbit}
          handleClick={() => setEnableOrbit(prevEnableOrbit => !prevEnableOrbit)}
        />
      </div>
      <div style={messageStyle}>
        {enableOrbit ? 'Rotation On' : 'Rotation Off'}
      </div>
      <Canvas shadows dpr={[1, 2]} style={{ width: `50%`, height: `80%`, position: `absolute`, right: 0 }} camera={{ position: [0, 10, -40] }}>
        <ambientLight intensity={1} />
        <Suspense fallback={null}>
          <Cylinder appear={true} />
          <Abschlussdeckel appear={data.abschlussdeckel} putAbschlussdeckel={props.putAbschlussdeckel} />
          <Kolbenstange appear={data.kolbenstange} putKolbenstange={props.putKolbenstange} />
          <Mutter appear={data.mutter} putMutter={props.putMutter} />
          <Schrauber blue={data.schrauber_blue} green={data.schrauber_green} grey={data.schrauber_grey} />
          <Messschieber appear={data.messschieber} />
          <Lagerdeckel appear={data.lagerdeckel} putLagerdeckel={props.putLagerdeckel} />
          <Baugruppe appear={data.baugruppe} putKolbenbaugruppe={props.putKolbenbaugruppe} />
          <Schraube appearOne={data.schraubeOne} appearTwo={data.schraubeTwo} appearThree={data.schraubeThree} appearFour={data.schraubeFour} />
          <Environment files="potsdamer_platz_1k.hdr" />
        </Suspense>
        {/* Conditional rendering of OrbitControls */}
        {enableOrbit && <OrbitControls
          minPolarAngle={Math.PI / 40}
          maxPolarAngle={Math.PI / 1}
          enableZoom={true}
          enablePan={false}
        />}
      </Canvas>
    </div>
  )
}