import { useEffect, useState } from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import { Table } from "react-bootstrap";

function App() {
  const [counter, setCounter] = useState(0);
  const [data, setData] = useState([]);

  const fetchData = () => {
    fetch(`/fetch-data`)
      .then((response) => response.json())
      .then((actualData) => {
        setData(actualData);
      })
      .catch((err) => {
        console.log(err.message);
      });
  };

  useEffect(() => {
    let interval;
    const updateCounter = () => {
      setCounter((currentValue) => currentValue + 1);
      fetchData();
    };
    interval = setInterval(() => {
      updateCounter();
    }, 5000);
    return () => {
      clearInterval(interval);
    };
  }, []);

  return (
    <div className="App m-5">
      <h4>Today's Cryptocurrency Prices by Market Cap</h4>'
      <br></br>
      <Table striped bordered hover>
        <tbody>
          <tr className="table_container">
            <th>Name</th>
            <th>Price</th>
            <th>1h%,</th>
            <th>24h%</th>
            <th>7d%</th>
            <th>Market Cap</th>
            <th>Volume</th>
            <th>Circulating Supply</th>
          </tr>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item.name}</td>
              <td>{item.price}</td>
              <td>{item.h_1}</td>
              <td>{item.h_24}</td>
              <td>{item.d_7}</td>
              <td>{item.market_cap}</td>
              <td>{item.volume}</td>
              <td>{item.circulating_Supply}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
}

export default App;
