import React, { useState } from 'react';
const backendUrl = 'http://127.0.0.1:5000';
function App() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${backendUrl}/upload`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      console.log(data.message);
    } catch (error) {
      console.error("Error uploading file: ", error);
    }
  };

  const fetchResults = async () => {
    const response = await fetch(`${backendUrl}/results`);
    const data = await response.json();
    setResults(data);
  };

  return (
    <div>
      <h1>OCR Application</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      <button onClick={fetchResults}>Fetch Results</button>
      <ul>
        {results.map((result, index) => (
          <li key={index}>
            <p>Image: {result.gcs_path}</p>
            <p>Text: {result.text}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;


// import React, { useState } from 'react';

// function App() {
//     const [file, setFile] = useState(null);
//     const [status, setStatus] = useState('');
//     const [output, setOutput] = useState('');

//     const handleFileChange = (e) => {
//         setFile(e.target.files[0]);
//     };

//     const handleUpload = async () => {
//         if (!file) {
//             alert('Please select a file before uploading.');
//             return;
//         }

//         const formData = new FormData();
//         formData.append('file', file);

//         const response = await fetch('http://<BACKEND_IP>:5000/upload', {
//             method: 'POST',
//             body: formData,
//         });
//         const data = await response.json();
//         setStatus(data.message);
//     };

//     const handleCheckOutput = async () => {
//         const response = await fetch('http://<BACKEND_IP>:5000/output');
//         const data = await response.json();
//         setOutput(data.text);
//     };

//     return (
//         <div>
//             <h1>OCR App</h1>
//             <input type="file" onChange={handleFileChange} />
//             <button onClick={handleUpload}>Upload</button>
//             <button onClick={handleCheckOutput}>Check Output</button>
//             <p>Status: {status}</p>
//             <textarea value={output} readOnly />
//         </div>
//     );
// }

// export default App;

