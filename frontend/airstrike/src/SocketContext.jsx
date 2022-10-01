import React, { createContext } from 'react';
import { io, Socket } from 'socket.io-client';

// using localstorage find url 
let url = localStorage.getItem('url') || 'http://192.168.17.131:8001';
url = prompt('Enter the url of the server', url);
localStorage.setItem('url', url);
const socket = io(url);
const SocketContext = createContext(socket);

socket.on('connect', () => console.log('connected to socket'));

const SocketProvider = ({ children }) => {
    return (
        <SocketContext.Provider value={socket}>{children}</SocketContext.Provider>
    );
};
export { SocketContext, SocketProvider };