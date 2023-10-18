// import logo from './logo.svg';
// import './App.css';
// import React, { useState, useEffect } from 'react';

// function App() {

//   const [data, setData] = useState([]);
//   // Other state variables, if needed

//   useEffect(() => {
//     fetchData(); // Call the function to fetch data
//   }, []); // Empty dependency array to run once on mount

//   // Function to fetch data
//   const fetchData = async () => {
//     try {
//       const response = await fetch('http://127.0.0.1:5000/user/getall');
//       const jsonData = await response.json();
//       setData(jsonData); // Update the state with fetched data
//       console.log(data[0].email)
//     } catch (error) {
//       console.error('Error fetching data:', error);
//     }
//   };

//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload------yes
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Sign-up
//         </a>
//       </header>
//     </div>
//   );
// }zzzz

// export default App;

import React, { useState } from 'react';
import axios from 'axios';

function MyComponent() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    // Add other fields as needed
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Send a POST request with Axios
      const response = await axios.post('http://127.0.0.1:5000/user/signup', formData);
      
      // Handle the response from the server (e.g., show a success message)
      console.log('Response:', response.data);
    } catch (error) {
      // Handle any errors (e.g., display an error message)
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h2>Submit Data to Database</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          placeholder="Name"
          value={formData.name}
          onChange={handleInputChange}
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleInputChange}
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleInputChange}
        />
        {/* Add other input fields as needed */}
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default MyComponent;
