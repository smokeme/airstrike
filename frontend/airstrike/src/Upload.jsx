import { Modal, Button } from "react-bootstrap";
import * as React from "react";

export default function Upload({ show, handleClose, selectedItem, handleUpload }) {
    const [file, setFile] = React.useState(null);
    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Upload shellcode</Modal.Title>
            </Modal.Header>
            <Modal.Body>Upload shellcode to be loaded to session {selectedItem}.

                <input type="file" onChange={(e) => setFile(e.target.files[0])} />
            </Modal.Body>

            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                    Cancel
                </Button>
                <Button variant="primary" onClick={() => handleUpload(selectedItem, file)}>
                    Upload
                </Button>
            </Modal.Footer>
        </Modal>);
}
