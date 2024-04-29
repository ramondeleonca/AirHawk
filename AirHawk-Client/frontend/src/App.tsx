import CameraFeed from "./components/camera-feed";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";

export default function App() {
    return (
        <div className="w-full h-full">
            <Tabs defaultValue="surveillance" className="w-full h-full p-2">
                <TabsList className="w-full">
                    <TabsTrigger value="surveillance">Surveillance</TabsTrigger>
                    <TabsTrigger value="network">Network</TabsTrigger>
                    <TabsTrigger value="drone">Drone</TabsTrigger>
                </TabsList>
                <TabsContent value="surveillance" className="relative h-full w-full">
                    <div className="h-[75%] w-full overflow-hidden rounded-sm grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
                        <CameraFeed url="/camera/0" />
                        <CameraFeed url="/camera/1" />
                        <CameraFeed url="/camera/2" />
                    </div>
                    <div className="h-[10%]">
                        asdad
                    </div>
                </TabsContent>
                <TabsContent value="network">
                    <div className="p-4">
                        <p>Network content</p>
                    </div>
                </TabsContent>
                <TabsContent value="drone">
                    <div className="p-4">
                        <p>Drone content</p>
                    </div>
                </TabsContent>
            </Tabs>
        </div>
    );
}