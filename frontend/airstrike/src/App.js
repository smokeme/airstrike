import './App.css';
import Header from './Header';
import Container from 'react-bootstrap/Container';
import ListItems from './ListItems';
import { SocketProvider } from './SocketContext';
import airstrike from './svg.svg';

function App() {
  return (
    <Container fluid>
      <SocketProvider>
      <Header />
      </SocketProvider>
      <div className="pt-5 text-center">
        <div className="row">
          <div className="col-md-4 mx-auto">
            <img src={airstrike} className="img" style={{ height: 100 }} />
            <p className="lead">Available Sessions</p>
          </div>
        </div>
      </div>
      <div className="text-center"> 
      <SocketProvider>
        <ListItems  />
      </SocketProvider>
      </div>
    </Container>
  );
}

export default App;
