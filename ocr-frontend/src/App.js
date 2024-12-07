import React, { useState } from 'react';
import './App.css';

const backendUrl = 'http://127.0.0.1:5000';

function App() {
  const [file, setFile] = useState(null);
  const [taskId, setTaskId] = useState(null);
  const [result, setResult] = useState([]);
  const [selectedLanguages, setSelectedLanguages] = useState([]);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleLanguageChange = (e) => {
    const selectedOptions = Array.from(e.target.selectedOptions);
    setSelectedLanguages(selectedOptions.map(option => option.value));
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file to upload")
      return;
    }

    const languages = selectedLanguages.length > 0 ? selectedLanguages : ['eng'];

    const formData = new FormData();
    formData.append('file', file);
    formData.append('languages', languages.join('+'));

    try {
      const response = await fetch(`${backendUrl}/upload`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setTaskId(data.task_id);
      alert(`File uploaded successfully! Task ID: ${data.task_id}`);
    } catch (error) {
      console.error("Error uploading file: ", error);
      alert("Failed to upload the file.")
    }
  };

  const fetchResult = async () => {
    if (!taskId) {
      alert("No task ID available. Upload a file first");
      return;
    }

    try {
      const response = await fetch(`${backendUrl}/results/${taskId}`);
      const data = await response.json();
      if (data.error) {
        alert(data.error);
      } else {
        setResult(data);
      }
    } catch (error) {
      console.error("Error fetching results: ", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>OCR Application</h1>
      </header>
      <main>
        <div>
          <label htmlFor="fileInput">Select Image:</label>
          <input id="fileInput" type="file" onChange={handleFileChange} />
        </div>
        <div>
          <label htmlFor="languageSelect">Select Languages:</label>
          <select id="languageSelect" multiple onChange={handleLanguageChange}>
            <option value="eng">English</option>
            <option value="chi_sim">Chinese (Simplified)</option>
            <option value="hin">Hindi</option>
            <option value="spa">Spanish</option>
          </select>
        </div>
        <button onClick={handleUpload}>Upload</button>
        <button onClick={fetchResult}>Fetch Results</button>
        {result && (
          <div>
            <h3>Result:</h3>
            <p><strong>Image:</strong> {result.gcs_path}</p>
            <p><strong>Detected Text:</strong> {result.text}</p>
            <p><strong>Languages:</strong> {result.languages}</p>
          </div>
        )}
      </main>
      <footer>
        <p>&copy; 2024 OCR Application. All rights reserved.</p>
        <p>Authors: ChengYu Hsu & Sri Vamsi Andavarapu</p>
      </footer>
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

