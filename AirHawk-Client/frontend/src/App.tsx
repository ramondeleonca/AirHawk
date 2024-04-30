import { useMemo, useState } from "react";
import CameraFeed from "./components/camera-feed";
import { Button } from "./components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { io } from "socket.io-client";
import { Download, MoveDown, MoveLeft, MoveRight, MoveUp, RotateCcw, RotateCw, Sunset, Upload } from "lucide-react";
import { Dialog, DialogClose, DialogContent, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "./components/ui/dialog";
import { Input } from "./components/ui/input";

export default function App() {
    const [sensors, setSensors] = useState({state: {present: false}});
    const socket = useMemo(() => io(), []);

    socket.on("sensors", data => {
        console.log(data);
        setSensors(data);
    });

    const addSensor = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const data = new FormData(e.currentTarget);
        fetch("/sensor/add/" + data.get("port"))
    }

    return (
        <div className="w-full h-full">
            <Tabs defaultValue="surveillance" className="w-full h-full p-2">
                <TabsList className="w-full">
                    <TabsTrigger value="surveillance">Surveillance</TabsTrigger>
                    <TabsTrigger value="sensors">Sensors</TabsTrigger>
                    <TabsTrigger value="drone">Drone</TabsTrigger>
                </TabsList>
                <TabsContent value="surveillance" className="relative h-full w-full">
                    <div className="h-[75%] w-full overflow-hidden rounded-sm grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
                        <CameraFeed url="/camera/0" />
                        <CameraFeed url="/camera/1" />
                        <CameraFeed url="/camera/2" />
                    </div>
                </TabsContent>
                <TabsContent value="sensors">
                    <div className="p-4">
                        <Dialog>
                            <DialogTrigger><Button>Add sensor</Button></DialogTrigger>
                            <DialogContent>
                                <DialogHeader>
                                    <DialogTitle>Add sensor</DialogTitle>
                                    
                                    <form onSubmit={addSensor}>
                                        <Input name="port" placeholder="Port" type="text"></Input>
                                    </form>

                                    <DialogFooter>
                                        <DialogClose>
                                            <Button type="submit">Add</Button>
                                        </DialogClose>
                                    </DialogFooter>
                                </DialogHeader>
                            </DialogContent>
                        </Dialog>
                        <div className="sensors">
                            <div>
                                <Sunset color={sensors["state"]["present"] ? "red" : "green"} size={52}></Sunset>
                                <h1>{sensors["state"]["present"] ? "PRESENCE" : "NO PRESENCE"}</h1>
                            </div>
                        </div>
                    </div>
                </TabsContent>
                <TabsContent value="drone">
                    <div className="p-4 flex">
                        <div className="w-1/2">
                            <CameraFeed url="/drone/camera"></CameraFeed>
                        </div>
                        <div className="w-1/2 px-4">
                            <h1 className="mb-8 text-5xl font-semibold">Controls</h1>
                            <Button onClick={() => fetch("/drone/connect")}>Connect</Button>
                            <div className="flex">
                                <Button className="mr-4" onClick={() => fetch("/drone/takeoff")}>Takeoff</Button>
                                <Button onClick={() => fetch("/drone/land")}>Land</Button>
                            </div>

                            <div className="mt-4">
                                <div className="w-fit">
                                    <div>
                                        <Button className="m-1" onClick={() => fetch("/drone/ccw")}><RotateCcw></RotateCcw></Button>
                                        <Button className="m-1" onClick={() => fetch("/drone/fwd")}><MoveUp></MoveUp></Button>
                                        <Button className="m-1" onClick={() => fetch("/drone/cw")}><RotateCw></RotateCw></Button>
                                    </div>
                                    <div className="flex justify-between">
                                        <Button className="m-1" onClick={() => fetch("/drone/left")}><MoveLeft></MoveLeft></Button>
                                        <Button className="m-1" onClick={() => fetch("/drone/right")}><MoveRight></MoveRight></Button>
                                    </div>
                                    <div>
                                        <Button className="m-1" onClick={() => fetch("/drone/up")}><Upload></Upload></Button>
                                        <Button className="m-1" onClick={() => fetch("/drone/back")}><MoveDown></MoveDown></Button>
                                        <Button className="m-1" onClick={() => fetch("/drone/dn")}><Download></Download></Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </TabsContent>
            </Tabs>
        </div>
    );
}