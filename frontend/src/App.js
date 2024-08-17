import './App.css';
import Form from 'react-bootstrap/Form';
import {Button} from "react-bootstrap";
import {Table} from "react-bootstrap";
import {useState, useEffect} from "react";

function App() {
    const [uploadedFiles, setUploadedFiles] = useState([])
    const [filesToUpload, setFilesToUpload] = useState(null)
    const [status, setStatus] = useState("")

    function getUploads() {
        fetch("uploads/")
            .then(res => {
                return res.json()
            })
            .then(data => {
                setUploadedFiles(data)
            })
            .catch(error => {
                console.log(JSON.stringify(error))
            })
    }

    useEffect(() => {
        getUploads();
    }, [])


    const handleUpload = async () => {
        if (filesToUpload === null || filesToUpload.length === 0) {
            setStatus('Please select files to upload.');
            return;
        }

        const formData = new FormData();
        for (let i = 0; i < filesToUpload.length; i++) {
            formData.append('files', filesToUpload[i]);

        }

        fetch("/", {
            method: 'POST',
            body: formData,
        })
            .then(res => {
                getUploads()
                return res.json()
            })
            .catch(err => console.log(err))
    }

    const handleDownload = (filename) => {
        console.log(filename)
        fetch("uploads/" + filename)
            .then(response => {
                if (response.ok) {
                    return response.blob();
                }
                throw new Error("The response was not a file")
            })
            .then(blob => {
                const link = document.createElement('a');
                const url = window.URL.createObjectURL(blob);
                link.href = url;
                link.download = filename;
                document.body.appendChild(link);
                link.click();
                link.remove();
                window.URL.revokeObjectURL(url);
            })
            .catch(error => {
                console.error("There was an error with the fetch operation")
            })
    }

    const handleDelete = (filename) => {
        console.log(filename)
        fetch("uploads/" + filename, {method: 'DELETE'})
            .then(() => {
                getUploads()
            });
    }

    const handleFileChange = (e) => {
        setFilesToUpload(e.target.files)
        console.log(`files to upload are ${JSON.stringify(filesToUpload)}`)
    }

    return (
        <div className="App">
            <div className="row">
                <Form.Group controlId="formFileMultiple" className="mb-3">
                    <Form.Label>Select Files to upload</Form.Label>
                    <Form.Control type="file" multiple onChange={handleFileChange}/>
                </Form.Group>
                <Button variant="primary" onClick={handleUpload}>Upload</Button>
            </div>
            <Table>
                <thead>
                <tr>
                    <th>File Name</th>
                    <th>Download</th>
                    <th>Delete</th>

                </tr>
                </thead>
                <tbody>
                {uploadedFiles.map((filename, index) => (
                    <tr key={index}>
                        <td> {filename} </td>
                        <td><Button variant="success" onClick={() => handleDownload(filename)}> Download </Button></td>
                        <td><Button variant="danger" onClick={() => handleDelete(filename)}> Delete </Button></td>
                    </tr>
                ))}
                </tbody>
            </Table>
        </div>
    );
}

export default App;
