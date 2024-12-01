import React, { Suspense, useRef, useState } from 'react'
import {
    useGLTF,
    OrbitControls,
    Environment,
} from "@react-three/drei"
import { Canvas, useThree, useFrame } from "@react-three/fiber"

// Making a position variable to control the position of the meshes for the animation
// with objects for each mesh, one element is the position and the other element is the state variable
let states = {
    lagerdeckel: { position: [-4, -0.01, 0.07], active: false },
    abschlussdeckel: { position: [5, -0.06, 0.05], active: false },
    mutter: { position: [-5.93, 5, 0], rotation: [0, 0.1, 0], active: false },
    kolbenstange: { position: [-5.97, 5, -0.01], active: false },
    baugruppe: { position: [-5.9, 5, 0], active: false },
    kolbenstangeBaugruppe: {
        kolbenstangePosition: [-4, 0, -0.07], baugruppePosition: [-3.5, 0, 0], mutterPosition: [-2.7, 0, -0.05],
        rotation: [1.71, -1.6, 1.7], active: false
    },
    schraubeOne: { position: [-4, 0.48, 0.55], rotation: [0, 0, 1.53], active: false },
    schraubeTwo: { position: [-4, -0.55, -0.42], rotation: [0, 0, 1.53], active: false },
    schraubeThree: { position: [5, 0.43, -0.46], rotation: [0, 0, -1.53], active: false },
    schraubeFour: { position: [5, -0.59, 0.52], rotation: [0, 0, -1.53], active: false },

    schrauberBlau: { position: [-6.7, 1.8, -1.9], rotation: [0, 2, 0], active: false },
    schrauberGrau: { position: [3.58, -2.3, 0.3], rotation: [0, 1.8, 0], active: false },
}

export function FullCylinder({ ...props }) {
    const { nodes, materials } = useGLTF('/Zylinder_ad_ld/Cylinder_ad_ld.gltf')

    // Cylinder tranparency control block
    function makeCylinderTransparent() {
        materials.zylinder.transparent = true
        materials.zylinder.opacity = 0.2
    }

    function makeCylinderOpaque() {
        materials.zylinder.opacity = 1
    }


    // Mesh block
    function Lagerdeckel() {
        // Make a reference to the position variable using useRef
        const ref = useRef(nodes.lagerdeckel)
        // Update camera position
        const { camera } = useThree()

        // Initialize the color variable
        let color = "white"
        // Initialize a dummy material variable
        let materialLagerdeckel = materials.lagerdeckel
        let materialMiddle = materials.middle
        // The hervohebung is turned on make the color #fc8905
        if (props.states.hervorhebungLagerdeckel) {
            color = "#fc8905"
            materialLagerdeckel = materials.lagerdeckelDummy
            materialMiddle = materials.middleDummy
        }

        // Update the position variable every frame
        useFrame((_, delta) => {
            // Play the animation as long as the position variable is smaller than -1.63
            // and the props.states.lagerdeckel variable is true
            if (states.lagerdeckel.position[0] < -1.67 && props.states.lagerdeckel) {
                // Update the position variable
                ref.current.position.x += delta
                states.lagerdeckel.position[0] += delta
                // Update the camera position
                camera.position.x -= delta * 2
                camera.position.z -= delta * 0.5
            }
            // If the animation is finished, set the state variable to false
            else if (states.lagerdeckel.position[0] >= -1.67 && props.states.lagerdeckel) {
                states.lagerdeckel.active = true
            }
        })
        if (!states.lagerdeckel.active && props.states.lagerdeckel) {
            //this is the actual should be position={[-1.63, -0.01, 0.07]}
            // When the animation is not finished, return a mesh with a changing position and the useFrame hook
            // When the hervohebung is turned on, make the lagerdeckel #fc8905
            makeCylinderOpaque()
            camera.position.set(-3, 0, 2)
            return (
                <group position={states.lagerdeckel.position} rotation={[-1.58, -0.01, -3.14]} scale={[0.83, 0.89, 0.89]} ref={ref}>
                    <mesh geometry={nodes.lagerdeckel.geometry} material={materialLagerdeckel} material-color={color} />
                    <mesh geometry={nodes.lagerdeckel_1.geometry} material={materialMiddle} material-color={color} />
                </group>
            )
        }
        // When the animation is finished, return a mesh with a fixed position and without the useFrame hook
        else if (states.lagerdeckel.active && props.states.lagerdeckel) {
            return (
                <group position={states.lagerdeckel.position} rotation={[-1.58, -0.01, -3.14]} scale={[0.83, 0.89, 0.89]}>
                    <mesh geometry={nodes.lagerdeckel.geometry} material={materialLagerdeckel} material-color={color} />
                    <mesh geometry={nodes.lagerdeckel_1.geometry} material={materialMiddle} material-color={color} />
                </group>
            )
        }
        // If the state variable is false, return an empty mesh
        else
            return (
                <mesh></mesh>
            )
    }
    function Abschlussdeckel() {
        // Same logic as Lagerdeckel() function above but the position calculation is different
        // the start position should be 5 and the end position should be 2.27
        // So the whole calculation has to be changed and the logics too (>= instead of <=)
        const ref = useRef(nodes.Abschlussdeckel)

        // Camera position
        const { camera } = useThree()

        // Initialize the color variable
        let color = "white"
        // Initialize a dummy material variable
        let material = materials.abschlussdeckel
        // The hervohebung is turned on make the color #fc8905
        if (props.states.hervorhebungAbschlussdeckel) {
            color = "#fc8905"
            material = materials.abschlussdeckelDummy
        }

        // Update the position variable every frame
        useFrame((_, delta) => {
            if (states.abschlussdeckel.position[0] > 2.314 && props.states.abschlussdeckel) {
                ref.current.position.x -= delta
                states.abschlussdeckel.position[0] -= delta
                camera.position.x += delta * 2
                camera.position.z -= delta * 0.5
            }
            else if (states.abschlussdeckel.position[0] <= 2.314 && props.states.abschlussdeckel) {
                states.abschlussdeckel.active = true
            }
        })

        if (!states.abschlussdeckel.active && props.states.abschlussdeckel) {
            //position={[2.27, -0.06, 0.05]}
            makeCylinderOpaque()
            camera.position.set(2, 0, 2)
            return (
                <mesh geometry={nodes.Abschlussdeckel.geometry}
                    material={material} material-color={color} position={states.abschlussdeckel.position}
                    rotation={[1.58, -0.005, -0.01]} scale={0.9} ref={ref} />
            )
        }
        else if (states.abschlussdeckel.active && props.states.abschlussdeckel) {
            return (
                <mesh geometry={nodes.Abschlussdeckel.geometry}
                    material={material} material-color={color} position={states.abschlussdeckel.position}
                    rotation={[1.58, -0.005, -0.01]} scale={0.9} />
            )
        }
        else
            return (
                <mesh></mesh>
            )
    }


    // Ths function is responsible for only the initial animation of the Kolbenstange,
    // namely it comes left-above in the vertical position
    function Kolbenstange() {
        // postion={[-4, 0, -0.07]} rotation={[1.71, 0.01, 1.56]} scale={0.03}
        // Same logic as Lagerdeckel() function above, just the end position is different
        const ref = useRef(nodes.kolbenstange)
        // Camera position
        const { camera } = useThree()

        // Initialize the color variable
        let color = "white"
        // Initialize a dummy material variable
        let material = materials.kolbenstange

        // The hervohebung is turned on make the color #fc8905
        if (props.states.hervorhebungKolbenstange) {
            color = "#fc8905"
            material = materials.kolbenstangeDummy
        }

        useFrame((_, delta) => {
            if (states.kolbenstange.position[1] > 1 && props.states.kolbenstange) {
                ref.current.position.y -= delta
                states.kolbenstange.position[1] -= delta
            }
            else if (states.kolbenstange.position[1] <= 1 && props.states.kolbenstange) {
                states.kolbenstange.active = true
            }
        })

        if (!states.kolbenstange.active && props.states.kolbenstange) {
            camera.position.set(0, 0, 7)
            makeCylinderTransparent()
            return (
                <mesh geometry={nodes.kolbenstange.geometry}
                    material={material} material-color={color}
                    position={states.kolbenstange.position}
                    rotation={[1.71, -1.6, 1.7]} scale={[0.03, 0.045, 0.03]} ref={ref} />
            )
        }
        else if (states.kolbenstange.active && props.states.kolbenstange) {
            return (
                <mesh geometry={nodes.kolbenstange.geometry}
                    material={material} material-color={color}
                    position={states.kolbenstange.position}
                    rotation={[1.71, -1.6, 1.7]} scale={[0.03, 0.045, 0.03]} />
            )
        }
        else
            return (
                <mesh></mesh>
            )
    }
    function Baugruppe() {
        // position={[-0.04, 0, 0]} scale={0.46}
        // Same logic as Kolbenstange() function above, just the end position is different
        const ref = useRef(nodes.baugruppe)
        // Camera position
        const { camera } = useThree()

        // Initialize the color variable
        let colorWhite = "white"
        let colorRed = "red"
        // The hervohebung is turned on make the color #fc8905
        if (props.states.hervorhebungBaugruppe) {
            colorWhite = "#fc8905"
            colorRed = "#fc8905"
        }
        useFrame((_, delta) => {
            if (states.baugruppe.position[1] > 1.5 && props.states.baugruppe) {
                ref.current.position.y -= delta
                states.baugruppe.position[1] -= delta
            }
            else if (states.baugruppe.position[0] <= 1.5 && props.states.baugruppe) {
                states.baugruppe.active = true
            }
        })

        if (!states.baugruppe.active && props.states.baugruppe) {

            //position={[-0.04, 0, 0]} scale={0.46}>
            camera.position.set(0, 0, 7)
            makeCylinderTransparent()
            return (
                <group position={states.baugruppe.position} scale={[0.8, 0.4, 0.4]} ref={ref} rotation={[1.5, 1.6, 0.08]}>
                    <mesh geometry={nodes.baugruppe.geometry} material={materials.rot} material-color={colorRed} />
                    <mesh geometry={nodes.baugruppe_1.geometry} material={materials.weiß} material-color={colorWhite} />
                </group>
            )
        }
        else if (states.baugruppe.active && props.states.baugruppe) {
            return (
                <group position={states.baugruppe.position} scale={[0.8, 0.4, 0.4]} rotation={[1.5, 1.6, 0.08]}>
                    <mesh geometry={nodes.baugruppe.geometry} material={materials.rot} material-color={colorRed} />
                    <mesh geometry={nodes.baugruppe_1.geometry} material={materials.weiß} material-color={colorWhite} />
                </group>
            )
        }
        else
            return (
                <mesh></mesh>
            )
    }

    function Mutter() {
        // Same logic as Lagerdeckel() function above but with also rotation of the x-axis
        const ref = useRef(nodes.mutter)
        // Camera position
        const { camera } = useThree()

        // Initialize the color variable
        let color = "white"
        // Initialize a dummy material variable
        let material = materials.mutter

        // The hervohebung is turned on make the color #fc8905
        if (props.states.hervorhebungMutter) {
            color = "#fc8905"
            material = materials.mutterDummy
        }


        useFrame((_, delta) => {
            if (states.mutter.position[1] > 2.6 && props.states.mutter) {
                ref.current.position.y -= delta
                states.mutter.position[1] -= delta

                //rotation block
                ref.current.rotation.y += delta
                states.mutter.rotation[1] += delta

            }
            else if (states.mutter.position[1] <= 2.6 && props.states.mutter) {
                states.mutter.active = true
            }
        })

        if (!states.mutter.active && props.states.mutter) {
            //position={[-2.25, 0, -0.05]}
            camera.position.set(0, 0, 7)
            makeCylinderTransparent()
            return (
                <mesh geometry={nodes.mutter.geometry}
                    material={material} material-color={color} position={states.mutter.position}
                    rotation={states.mutter.rotation} scale={[-0.023, -0.03, -0.023]} ref={ref} />
            )
        }
        else if (states.mutter.active && props.states.mutter) {
            return (
                <mesh geometry={nodes.mutter.geometry}
                    material={material} material-color={color} position={states.mutter.position}
                    rotation={states.mutter.rotation} scale={[-0.023, -0.03, -0.023]} />
            )
        }
        else
            return (
                <mesh></mesh>
            )
    }

    // Animate the Kolbenstange and Baugruppe together in KolbenstangeBaugruppe() function
    function KolbenstangeBaugruppe() {
        // At first when props.states.kolbenstange is true the kolbenstange mesht should start from -10 and move to -7
        // Then the baugruppe mesh should start from -10 and move to -3
        // Then both of them together will move to -1.3 together
        // And after this two animations are done, they both will stay at -1.3
        // horizontal -> rotation = [1.71, 0.01, 1.56]
        const refKolbenstange = useRef(nodes.kolbenstange)

        // Camera position
        const { camera } = useThree()

        // Initialize the color variable
        let color = "white"
        let colorRed = "red"

        // Initialize a dummy material variables
        let materialKolbenstange = materials.kolbenstange
        let materialMutter = materials.mutter

        // The hervohebung is turned on make the color #fc8905
        if (props.states.hervorhebungKolbenstangeBaugruppe) {
            color = "#fc8905"
            colorRed = "#fc8905"
            materialKolbenstange = materials.kolbenstangeDummy
            materialMutter = materials.mutterDummy
        }

        // Animate the Kolbenstangebaugruppe by changing the position of the kolbenstange and baugruppe and mutter
        useFrame((_, delta) => {
            if (props.states.kolbenstangeBaugruppe && states.kolbenstangeBaugruppe.kolbenstangePosition[0] < 0.2) {
                states.kolbenstangeBaugruppe.kolbenstangePosition[0] += delta
                states.kolbenstangeBaugruppe.baugruppePosition[0] += delta
                states.kolbenstangeBaugruppe.mutterPosition[0] += delta
                refKolbenstange.current.position.x += delta
            }
            else if (props.states.kolbenstangeBaugruppe && states.kolbenstangeBaugruppe.kolbenstangePosition[0] >= 0.2) {
                states.kolbenstangeBaugruppe.active = true
            }


        }
        )

        if (!states.kolbenstangeBaugruppe.active && props.states.kolbenstangeBaugruppe) {
            camera.position.set(0, 0, 7)
            makeCylinderTransparent()
            return (
                <group ref={refKolbenstange}>
                    <mesh geometry={nodes.kolbenstange.geometry} material={materialKolbenstange} rotation={[1.71, 0.01, -1.56]}
                        position={states.kolbenstangeBaugruppe.kolbenstangePosition} material-color={color} scale={[0.03, 0.045, 0.03]} />
                    <group scale={[0.8, 0.4, 0.4]} position={states.kolbenstangeBaugruppe.baugruppePosition}>
                        <mesh geometry={nodes.baugruppe.geometry} material={materials.rot} material-color={colorRed} />
                        <mesh geometry={nodes.baugruppe_1.geometry} material={materials.weiß} material-color={color} />
                    </group>
                    <mesh geometry={nodes.mutter.geometry} material={materialMutter}
                        position={states.kolbenstangeBaugruppe.mutterPosition}
                        rotation={[0, 0, 1.6]} material-color={color} scale={[-0.023, -0.03, -0.023]} />
                </group>
            )
        }
        else if (states.kolbenstangeBaugruppe.active && props.states.kolbenstangeBaugruppe) {
            return (
                <group >
                    <mesh geometry={nodes.kolbenstange.geometry} material={materialKolbenstange}
                        position={states.kolbenstangeBaugruppe.kolbenstangePosition}
                        rotation={[1.71, 0.01, -1.56]}
                        material-color={color} scale={[0.03, 0.045, 0.03]} />
                    <group scale={[0.8, 0.4, 0.4]} position={states.kolbenstangeBaugruppe.baugruppePosition} >
                        <mesh geometry={nodes.baugruppe.geometry} material={materials.rot} material-color={colorRed} />
                        <mesh geometry={nodes.baugruppe_1.geometry} material={materials.weiß} material-color={color} />
                    </group>
                    <mesh geometry={nodes.mutter.geometry} material={materialMutter}
                        position={states.kolbenstangeBaugruppe.mutterPosition}
                        rotation={[0, 0, 1.6]} material-color={color} scale={[-0.023, -0.03, -0.023]} />
                </group>
            )
        }

        else
            return (
                <mesh></mesh>
            )
    }



    // Schrauben block
    function Schraube001() {
        // Animation same as Mutter
        // End position is position={[-1.55, 0.48, 0.55]} rotation={[0, 0, 1.53]} scale={0.06}

        const ref = useRef(nodes.Schraube001)

        // Update camera position
        const { camera } = useThree()

        // Initial color
        let color = "white"
        // Initial material
        let material = materials.schraubeOne


        if (props.states.hervorhebungSchraubeOne) {
            color = "#fc8905"
            material = materials.schraubeOneDummy
        }

        useFrame((_, delta) => {
            if (states.schraubeOne.position[0] < -1.48 && props.states.schraubeOne) {
                ref.current.position.x += delta
                ref.current.rotation.x += delta
                states.schraubeOne.position[0] += delta
                states.schraubeOne.rotation[0] += delta
                // Update the camera position
                camera.position.x -= delta
                camera.position.z += delta * 0.25
            }
            else if (states.schraubeOne.position[0] >= -1.48 && props.states.schraubeOne) {
                states.schraubeOne.active = true
            }
        })

        if (!states.schraubeOne.active && props.states.schraubeOne) {
            //position={[-2.25, 0, -0.05]}
            makeCylinderOpaque()
            camera.position.set(-3, 0, 2)
            return (
                <mesh geometry={nodes.Schraube001.geometry} material={material} material-color={color}
                    position={states.schraubeOne.position}
                    rotation={states.schraubeOne.rotation} scale={0.06} ref={ref} />
            )
        }
        else if (states.schraubeOne.active && props.states.schraubeOne) {
            return (
                <mesh geometry={nodes.Schraube001.geometry} material={material} material-color={color}
                    position={states.schraubeOne.position}
                    rotation={states.schraubeOne.rotation} scale={0.06} />
            )
        }
        else
            return (
                <mesh></mesh>
            )
    }
    function Schraube002() {

        // End position is position={[-1.58, -0.55, -0.42]} rotation={[0, 0, 1.53]} scale={0.06}
        // Animation logic and color logic is same as Schraube001

        const ref = useRef(nodes.Schraube002)

        // Camera position
        const { camera } = useThree()

        // Initial color
        let color = "white"
        // Initial material 
        let material = materials.schraubeTwo

        if (props.states.hervorhebungSchraubeTwo) {
            color = "#fc8905"
            material = materials.schraubeTwoDummy
        }

        useFrame((_, delta) => {
            if (states.schraubeTwo.position[0] < -1.48 && props.states.schraubeTwo) {
                ref.current.position.x += delta
                ref.current.rotation.x += delta
                states.schraubeTwo.position[0] += delta
                states.schraubeTwo.rotation[0] += delta
                // Update the camera position
                camera.position.x -= delta
                camera.position.z += delta * 0.25
            }
            else if (states.schraubeTwo.position[0] >= -1.48 && props.states.schraubeTwo) {
                states.schraubeTwo.active = true
            }
        })

        if (!states.schraubeTwo.active && props.states.schraubeTwo) {
            //position={[-2.25, 0, -0.05]}
            makeCylinderOpaque()
            camera.position.set(-3, 0, 2)
            return (
                <mesh geometry={nodes.Schraube002.geometry} material={material} material-color={color}
                    position={states.schraubeTwo.position}
                    rotation={states.schraubeTwo.rotation} scale={0.06} ref={ref} />
            )
        }
        else if (states.schraubeTwo.active && props.states.schraubeTwo) {
            return (
                <mesh geometry={nodes.Schraube002.geometry} material={material} material-color={color}
                    position={states.schraubeTwo.position}
                    rotation={states.schraubeTwo.rotation} scale={0.06} />
            )
        }
        else
            return (
                <mesh></mesh>
            )
    }
    function Schraube003() {

        // End position is position={[2.13, 0.43, -0.46]} rotation={[0, 0, -1.53]} scale={0.07}
        // Exactly same logic as Schraube001 and Schraube002 but with different position

        const ref = useRef(nodes.Schraube003)


        // Camera position
        const { camera } = useThree()

        // Initial color
        let color = "white"
        // Initial material
        let material = materials.schraubeThree

        if (props.states.hervorhebungSchraubeThree) {
            color = "#fc8905"
            material = materials.schraubeThreeDummy
        }

        useFrame((_, delta) => {
            if (states.schraubeThree.position[0] > 2 && props.states.schraubeThree) {
                ref.current.position.x -= delta
                ref.current.rotation.x -= delta
                states.schraubeThree.position[0] -= delta
                states.schraubeThree.rotation[0] -= delta

                camera.position.x += delta
                camera.position.z -= delta * 0.25
            }
            else if (states.schraubeThree.position[0] <= 2 && props.states.schraubeThree) {
                states.schraubeThree.active = true
            }
        })

        if (!states.schraubeThree.active && props.states.schraubeThree) {
            //position={[-2.25, 0, -0.05]}
            makeCylinderOpaque()
            camera.position.set(2, 0, 2)
            return (
                <mesh geometry={nodes.Schraube003.geometry} material={material} material-color={color}
                    position={states.schraubeThree.position}
                    rotation={states.schraubeThree.rotation} scale={0.07} ref={ref} />
            )
        }
        else if (states.schraubeThree.active && props.states.schraubeThree) {
            return (
                <mesh geometry={nodes.Schraube003.geometry} material={material} material-color={color}
                    position={states.schraubeThree.position}
                    rotation={states.schraubeThree.rotation} scale={0.07} />
            )
        }
        else
            return (
                <mesh></mesh>
            )

    }
    function Schraube004() {

        // End position is position={[2.16, -0.59, 0.52]} rotation={[0, 0, -1.53]} scale={0.06}
        // Exactly same logic as Schraube003

        const ref = useRef(nodes.Schraube004)


        // Camera position
        const { camera } = useThree()

        // Initial color
        let color = "white"
        // Initial material
        let material = materials.schraubeFour

        if (props.states.hervorhebungSchraubeFour) {
            color = "#fc8905"
            material = materials.schraubeFourDummy
        }

        useFrame((_, delta) => {
            if (states.schraubeFour.position[0] > 2.1 && props.states.schraubeFour) {
                ref.current.position.x -= delta
                ref.current.rotation.x -= delta
                states.schraubeFour.position[0] -= delta
                states.schraubeFour.rotation[0] -= delta

                camera.position.x += delta
                camera.position.z -= delta * 0.25
            }
            else if (states.schraubeFour.position[0] <= 2.1 && props.states.schraubeFour) {
                states.schraubeFour.active = true
            }
        })

        if (!states.schraubeFour.active && props.states.schraubeFour) {
            //position={[-2.25, 0, -0.05]}
            makeCylinderOpaque()
            camera.position.set(2, 0, 2)
            return (
                <mesh geometry={nodes.Schraube004.geometry} material={material} material-color={color}
                    position={states.schraubeFour.position}
                    rotation={states.schraubeFour.rotation} scale={0.06} ref={ref} />
            )
        }
        else if (states.schraubeFour.active && props.states.schraubeFour) {
            return (
                <mesh geometry={nodes.Schraube004.geometry} material={material} material-color={color}
                    position={states.schraubeFour.position}
                    rotation={states.schraubeFour.rotation} scale={0.06} />
            )
        }
        else
            return (
                <mesh></mesh>
            )

    }

    // Schrauber
    function SchrauberBlau() {
        const ref = useRef(nodes.Schrauber)
        useFrame((_, delta) => {
            if (props.states.schrauberBlau && states.schrauberBlau.rotation[1] < 4) {
                ref.current.rotation.y += 0.5 * delta
                states.schrauberBlau.rotation[1] += 0.5 * delta
                ref.current.rotation.x += 0.2 * delta
                states.schrauberBlau.rotation[0] += 0.2 * delta
            }
            else if (props.states.schrauberBlau && states.schrauberBlau.rotation[1] >= 4) {
                states.schrauberBlau.active = true
            }
        })
        if (props.states.schrauberBlau && !states.schrauberBlau.active)
            return (
                <mesh geometry={nodes.Schrauber.geometry} material={materials.schrauber}
                    material-color="blue" position={states.schrauberBlau.position}
                    rotation={states.schrauberBlau.rotation} scale={[0.1, 0.1, 0.1]} ref={ref} />
            )
        else
            return (
                <mesh></mesh>
            )
    }
    function SchrauberGrau() {
        // position: [-3, -1.2, 0.3], rotation: [0, -1.8, 0]
        // position: [-3, -2.3, -0.7], rotation: [0, -1.8, 0]
        // position: [3.6, -1.2, -0.7], rotation: [0, 1.8, 0]
        // position: [3.58, -2.3, 0.3], rotation: [0, 1.8, 0] 
        const [counter, setCounter] = useState(0)

        const { camera } = useThree()

        useFrame((_, delta) => {
            if (props.states.schrauberGrau && counter < 1) {
                camera.position.set(7.3, 0, 0.45)
                states.schrauberGrau.position = [3.58, -2.3, 0.3]
                states.schrauberGrau.rotation = [0, 1.8, 0]
                setCounter(counter + delta)
            }
            else if (props.states.schrauberGrau && counter < 2 && counter >= 1) {
                camera.position.set(7.3, 0, 0.45)
                states.schrauberGrau.position = [3.6, -1.2, -0.7]
                states.schrauberGrau.rotation = [0, 1.8, 0]
                setCounter(counter + delta)
            }
            else if (props.states.schrauberGrau && counter < 3 && counter >= 2) {
                camera.position.set(-7, 0, 0.8)
                states.schrauberGrau.position = [-3, -2.3, -0.7]
                states.schrauberGrau.rotation = [0, -1.8, 0]
                setCounter(counter + delta)
            }
            else if (props.states.schrauberGrau && counter < 4 && counter >= 3) {
                camera.position.set(-7, 0, 0.8)
                states.schrauberGrau.position = [-3, -1.2, 0.3]
                states.schrauberGrau.rotation = [0, -1.8, 0]
                setCounter(counter + delta)
            }
            else if (props.states.schrauberGrau && counter >= 4) {
                states.schrauberGrau.active = true
            }

        })
        if (props.states.schrauberGrau && !states.schrauberGrau.active) {
            return (
                <mesh geometry={nodes.Schrauber.geometry} material={materials.schrauber}
                    material-color="#51565c" position={states.schrauberGrau.position}
                    rotation={states.schrauberGrau.rotation} scale={[0.1, 0.1, 0.1]} />
            )
        }
        else
            return (
                <mesh></mesh>
            )
    }

    return (
        <group {...props} dispose={null}>
            <mesh geometry={nodes.Zylinder.geometry} material={materials.zylinder}
                position={[1.32, 0, 0]} scale={[1, 0.89, 1]} />
            <Lagerdeckel />
            <Abschlussdeckel />
            <Kolbenstange />
            <Baugruppe />
            <Mutter />
            <KolbenstangeBaugruppe />
            <SchrauberBlau />
            <SchrauberGrau />
            <Schraube001 />
            <Schraube002 />
            <Schraube003 />
            <Schraube004 />
        </group>
    )
}

export default function Recommendation3D({ data, ...props }) {
    return (
        <div>
            <Canvas shadows dpr={[1, 2]} style={{ width: '100%', height: '100%', position: `absolute` }}
                camera={{ position: [0, 0, 8] }}>
                <ambientLight intensity={1} />
                <Suspense fallback={null}>
                    <FullCylinder states={data} />
                    <Environment files="potsdamer_platz_1k.hdr" />
                </Suspense>
                <OrbitControls
                    minPolarAngle={Math.PI / 40}
                    maxPolarAngle={Math.PI / 1}
                    enableZoom={true}
                    enablePan={false}
                />
            </Canvas>
        </div>
    )
}