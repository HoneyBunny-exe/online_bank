import './component/styles/App.css';
import Navbar from "./component/Navbar/Navbar";
import Home from "./component/pages/Home/Home";
import CardItem from "./component/pages/Home/CardItem";
import CardList from "./component/pages/Home/CardList";
import AppRouter from "./component/AppRouter";

function App() {
  return (
    <div className="App">
      <Navbar/>
        <AppRouter/>
    </div>
  );
}

export default App;
