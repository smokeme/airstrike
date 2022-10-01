import * as React from "react";
import Upload from "./Upload";
import { SocketContext } from './SocketContext';

export default function ListItems() {
    const [items, setItems] = React.useState([]);
    const [show, setShow] = React.useState(false);
    const [selectedItem, setSelectedItem] = React.useState(null);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const socket = React.useContext(SocketContext);
    socket.on("sessions", (data) => {
        setItems(data);
    });
    let handleLoad = (id) => {
        setSelectedItem(id);
        handleShow();
    };
    let handleUpload = (id, file) => {
        socket.emit("load", { "id": id, "file": file });
        handleClose();
    }
    let fixTime = (time) => {
        time = time.replace(" seconds", "");
        time = parseInt(time);
        let hours = Math.floor(time / 3600);
        let minutes = Math.floor((time - (hours * 3600)) / 60);
        let seconds = time - (hours * 3600) - (minutes * 60);
        if (hours < 10) { hours = "0" + hours; }
        if (minutes < 10) { minutes = "0" + minutes; }
        if (seconds < 10) { seconds = "0" + seconds; }
        return hours + ':' + minutes + ':' + seconds;
    }

    return (
        <div className="row">
            <Upload show={show} handleUpload={handleUpload} handleClose={handleClose} selectedItem={selectedItem} />
            <div className="col-md-12">
                <div className="table-responsive">
                    <table className="table table-bordered ">
                        <thead className="thead-dark">
                            <tr>
                                <th>ID</th>
                                <th >Status</th>
                                <th>User</th>
                                <th>Domain</th>
                                <th>Machine</th>
                                <th>Process</th>
                                <th>Version</th>
                                <th>Arch</th>
                                <th>PID</th>

                                <th>Last Seen</th>
                                <th>IP</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="mytable">

                            {items.map((item) => (
                                <tr key={item.id}>
                                    <td>{item.id}</td>
                                    <td><span class={!item.loaded ? "badge badge-success" : "badge badge-danger"}>{!item.loaded ? "Alive" : "Loaded"}</span></td>
                                    <td>{item.username}</td>
                                    <td>{item.domain}</td>
                                    <td>{item.machine}</td>
                                    <td>{item.process}</td>
                                    <td>{item.version}</td>
                                    <td>{item.arch}</td>
                                    <td>{item.pid}</td>
                                    <td>{fixTime(item.lastupdated)}</td>
                                    <td>{item.ip}</td>
                                    <td>
                                        <button onClick={() => handleLoad(item.id)} className="btn btn-primary btn-sm">Load</button>
                                    </td>
                                </tr>
                            ))
                            }
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    )
}