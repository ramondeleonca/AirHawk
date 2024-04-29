type Props = { url: string };
export default function CameraFeed(props: Props) {
    return (
        <div className="relative min-h-24">
            <h1 className="absolute w-full h-full flex items-center justify-center font-bold text-4xl z-10">NO VIDEO</h1>
            <img src={props.url} alt="" className="w-full object-contain z-20 relative"></img>
            <h1 className="absolute bottom-0 left-1 text-stroke text-2xl z-30 font-bold">{`${props.url}`}</h1>
        </div>
    );
}