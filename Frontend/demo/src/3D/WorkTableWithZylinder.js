import { React, useState, Suspense } from "react"
import WorkPlaceWithoutAnything from "./WorkTableWithoutAnything"
import InteractiveCylinder from '../3D/FestoCylinderInteractive'
import { useGLTF, Environment } from "@react-three/drei"
import { Canvas } from "@react-three/fiber"



export function WorkPlace({ onMeshClick, ...props }) {
    const { nodes, materials } = useGLTF('/WorkTable/WorkTable.gltf')

    // Function to handle mesh clicks
    const handleMeshClick = (meshName) => {
        onMeshClick(meshName);
    };

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
                onPointerDown={() => handleMeshClick('mutter')}
            />
            <mesh
                geometry={nodes.kolbenBaugruppe.geometry}
                material={materials.boxkolbenBaugruppe}
                position={[-0.083, 0.408, 0.705]}
                rotation={[Math.PI / 2, 0, 1.568]}
                scale={0.007}
                onPointerDown={() => handleMeshClick('baugruppe')}
            />
            <mesh
                geometry={nodes.kolbenStange.geometry}
                material={materials.boxkolbenStange}
                position={[-0.789, 0.408, 0.705]}
                rotation={[Math.PI / 2, 0, 1.568]}
                scale={0.007}
                onPointerDown={() => handleMeshClick('kolbenstange')}
            />
            <mesh
                geometry={nodes.abschlussDeckel.geometry}
                material={materials.boxabschlussDeckel}
                position={[-0.566, 0.055, 0.705]}
                rotation={[Math.PI / 2, 0, 1.568]}
                scale={0.007}
                onPointerDown={() => handleMeshClick('abschlussdeckel')}
            />
            <mesh
                geometry={nodes.bundSchraube.geometry}
                material={materials.boxbundSchraube}
                position={[0.104, 0.055, 0.705]}
                rotation={[Math.PI / 2, 0, 1.568]}
                scale={0.007}
                onPointerDown={() => handleMeshClick('bundSchraube')}
            />
            <mesh
                geometry={nodes.lagerDeckel.geometry}
                material={materials.boxlagerDeckel}
                position={[0.787, 0.055, 0.705]}
                rotation={[Math.PI / 2, 0, 1.568]}
                scale={0.007}
                onPointerDown={() => handleMeshClick('lagerdeckel')}
            />
            <mesh
                geometry={nodes.schrauberGelb.geometry}
                material={materials.schrauberGelb}
                position={[-1.474, -0.263, -0.205]}
                rotation={[-1.222, -0.018, -3.068]}
                scale={0.023}
                onPointerDown={() => handleMeshClick('schrauber_yellow')}
            />
            <mesh
                geometry={nodes.schrauberBlau.geometry}
                material={materials.schrauberBlau}
                position={[-1.474, -0.263, -0.625]}
                rotation={[-1.222, -0.018, -3.068]}
                scale={0.023}
                onPointerDown={() => handleMeshClick('schrauber_blue')}
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

function putMutter() {
    console.log('putMutter')
}

export default function WorkTableWithZylinder(props) {
    var [states, setStates] = useState({
        abschlussdeckel: false,
        kolbenstange: false,
        mutter: false,
        schraubeOne: false,
        schraubeTwo: false,
        schraubeThree: false,
        schraubeFour: false,
        lagerdeckel: false,
        baugruppe: false,
        schrauber_blue: false,
        schrauber_green: false,
        messschieber: false,
        bundSchraubeClickCount: 0,
    })

    const handleMeshClick = (meshName) => {
        switch (meshName) {
            case 'abschlussdeckel':
                setStates(prev => ({ ...prev, abschlussdeckel: !states.abschlussdeckel }));
                props.pressabschlussdeckel()
                break;
            case 'lagerdeckel':
                setStates(prev => ({ ...prev, lagerdeckel: !states.lagerdeckel }));
                props.presslagerdeckel()
                break;
            case 'baugruppe':
                setStates(prev => ({ ...prev, baugruppe: !states.baugruppe }));
                props.presskolbenbaugruppe()
                break;
            case 'kolbenstange':
                setStates(prev => ({ ...prev, kolbenstange: !states.kolbenstange }));
                props.presskolbenstange()
                break;
            case 'mutter':
                setStates(prev => ({ ...prev, mutter: !states.mutter }));
                props.pressmutter()
                break;
            case 'schraubeOne':
                setStates(prev => ({ ...prev, schraubeOne: true, schraubeTwo: false, schraubeThree: false, schraubeFour: false }));
                break;
            case 'schraubeTwo':
                setStates(prev => ({ ...prev, schraubeTwo: true, schraubeOne: false, schraubeThree: false, schraubeFour: false }));
                break;
            case 'schraubeThree':
                setStates(prev => ({ ...prev, schraubeThree: true, schraubeTwo: false, schraubeOne: false, schraubeFour: false }));
                break;
            case 'schraubeFour':
                setStates(prev => ({ ...prev, schraubeFour: true, schraubeTwo: false, schraubeThree: false, schraubeOne: false }));
                break;
            case 'schrauber_blue':
                setStates(prev => ({ ...prev, schrauber_blue: !states.schrauber_blue, schrauber_green: false, schrauber_grey: false }));
                props.pressblauerSchrauber()
                break;
            case 'schrauber_yellow':
                setStates(prev => ({ ...prev, schrauber_green: true, schrauber_blue: false, schrauber_grey: false }));
                break;
            case 'schrauber_grey':
                setStates(prev => ({ ...prev, schrauber_grey: true, schrauber_blue: false, schrauber_green: false }));
                break;
            case 'messschieber':
                setStates(prev => ({ ...prev, messschieber: true }));
                props.pressMesschieber()
                break;
            case 'bundSchraube':
                // Cycling through the schraube states
                setStates(prev => ({
                    ...prev,
                    bundSchraubeClickCount: prev.bundSchraubeClickCount + 1,
                    schraubeOne: prev.bundSchraubeClickCount % 5 === 0,
                    schraubeTwo: prev.bundSchraubeClickCount % 5 === 1,
                    schraubeThree: prev.bundSchraubeClickCount % 5 === 2,
                    schraubeFour: prev.bundSchraubeClickCount % 5 === 3,
                }));
                break;
            default:
            // Default action if needed
        }
    };




    return (
        <>
            <div>
                <Canvas shadows dpr={[1, 2]} style={{ width: `50%`, height: `100%`, position: `absolute`, left: 0 }}
                    camera={{ position: [0, 3, -4] }}>
                    <ambientLight intensity={1} />
                    <Suspense fallback={null}>
                        <WorkPlace onMeshClick={handleMeshClick} />
                        <Environment files="potsdamer_platz_1k.hdr" />
                    </Suspense>
                </Canvas>
            </div>

            <InteractiveCylinder data={states}
                putAbschlussdeckel={props.putAbschlussdeckel}
                putKolbenstange={props.putKolbenstange}
                putMutter={props.putMutter}
                putLagerdeckel={props.putLagerdeckel}
                putKolbenbaugruppe={props.putKolbenbaugruppe} />
        </>
    )
}