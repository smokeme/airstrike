import * as React from "react"
import { SocketContext } from './SocketContext';

function Header() {
    const socket = React.useContext(SocketContext);
    let clearDb = () => {
        socket.emit("cleardb");
    }
    return (
        <div className="d-flex flex-column flex-md-row align-items-center p-3 mb-3 box-shadow border-bottom">
            <h5 className="my-0 mr-md-auto font-weight-normal">AirStrike</h5>
            <nav className="my-2 my-md-0 mr-md-3">
                <a className="p-2 text-dark" href="#" onClick={() => clearDb()}>
                    Clear
                </a>
            </nav>
        </div>
    )
}
export default Header;