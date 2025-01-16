import logo from './logo.svg';
import './App.css';
import Home from './components/Home';
import { Route,Routes } from 'react-router-dom';
function App() {
  return (
    <Routes>
      <Route path="/" element={<Home/>}/>
    </Routes>
  );
}

export default App;
