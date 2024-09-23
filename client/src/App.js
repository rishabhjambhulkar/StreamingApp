import React, { useEffect, useRef, useState } from 'react';
import Hls from 'hls.js';
import Draggable from 'react-draggable';
import { ResizableBox } from 'react-resizable';
import axios from 'axios';
import 'react-resizable/css/styles.css';

function App() {
  const videoRef = useRef();
  const [overlayContent, setOverlayContent] = useState('Custom Overlay');
  const [overlaySize, setOverlaySize] = useState({ width: 200, height: 100 });
  const [overlays, setOverlays] = useState([]);
  const [userId, setUserId] = useState('');
  const [newOverlay, setNewOverlay] = useState(null);
  const [currentOverlayPosition, setCurrentOverlayPosition] = useState(null); // Store drag position independently

const handleStream = async () => {

  try {
    const response = await axios.get('http://localhost:5000/stream'); // Assuming the backend is running on the same origin
    console.log(response.data);  // Should log "Streaming started in a separate thread!" or "Streaming is already running."
  } catch (error) {
    console.error('Error starting the stream:', error);
  }
}



  // console.log('overlays', overlays)
  // Fetch overlays from the server
  const fetchOverlays = async () => {
    console.log('Fetching overlays', userId);
    try {
      const response = await axios.post('http://localhost:5000/api/overlays', {
        userId: userId // Send userId in the request body
      });
      console.log(response);
      setOverlays(response.data);
      
     

    } catch (error) {
      console.error('Error fetching overlays:', error);
    }
  };

  // Save overlay function
  const saveOverlay = async (overlayData) => {
    try {
      await axios.post('http://localhost:5000/api/overlay', overlayData);
      fetchOverlays(); // Refresh overlays after saving
    } catch (error) {
      console.error('Error saving overlay:', error);
    }
  };


// Update overlay function
const updateOverlay = async (overlay) => {
  console.log('Updating overlay', overlayContent);
  // Create an updated overlay object with the current state

  const updatedOverlay = {
    _id: overlay._id,
    userId: overlay.userId,
    position:  overlay.position, // Use the stored position
    size: overlay.size,
    content: { type: 'text', value: overlayContent }
  };

  console.log(currentOverlayPosition, overlaySize, overlayContent);
  try {
    const response = await axios.post(`http://localhost:5000/api/updateOverlay`, updatedOverlay);
    console.log(response.data);
    fetchOverlays(); // Refresh overlays after updating
  } catch (error) {
    console.error('Error updating overlay:', error);
  }
};

  // Delete overlay
  const deleteOverlay = async (overlayId, e) => {
    e.stopPropagation(); // Prevent the click event from bubbling up
    console.log(overlayId);
    try {
      await axios.delete(`http://localhost:5000/api/delete`, {
        data: {
          overlayId: overlayId, // Include the overlayId to delete
        },
      });
      fetchOverlays(); // Refresh overlays after deletion
    } catch (error) {
      console.error('Error deleting overlay:', error);
    }
  };

  // Create a new overlay
  const createNewOverlay = () => {
    const newOverlayPosition = {
      x: Math.random() * (window.innerWidth - 300), // Random position within window width
      y: Math.random() * (window.innerHeight - 1400) // Random position within window height
    };

    const overlay = {
      userId,
      position: newOverlayPosition,
      size: overlaySize,
      content: { type: 'text', value: overlayContent }
    };
    setNewOverlay(overlay);
    setCurrentOverlayPosition(newOverlayPosition); // Set initial position for new overlay
  };

  // Handle overlay position change
  const onStop = (e, data) => {
    if (newOverlay) {
      const updatedOverlay = {
        ...newOverlay,
        position: { x: data.x, y: data.y }
      };
      setCurrentOverlayPosition(updatedOverlay.position); // Update position but don't save yet
      setNewOverlay(updatedOverlay);
    }
  };

  // When the overlay is resized
  const onResize = (e, { size }) => {
    console.log(size,e)
    if (newOverlay) {
      setOverlaySize({ width: size.width, height: size.height });
      setNewOverlay({
        ...newOverlay,
        size: { width: size.width, height: size.height }
      });
    }
  };

  // Handle text editing
  const handleContentChange = (e) => {
    setOverlayContent(e.target.innerText);
    console.log( 'overlay content',overlayContent)
    if (newOverlay) {
      setNewOverlay({
        ...newOverlay,
        content: { type: 'text', value: e.target.innerText }
      });
    }
  };

  // HLS Stream Setup
  useEffect(() => {
    if (Hls.isSupported()) {
      const hls = new Hls();
      hls.loadSource('http://localhost:5000/hls/pipe.m3u8');
      hls.attachMedia(videoRef.current);
    }
  }, []);

  return (
    <div className="video-container" style={{ position: 'relative', marginLeft: '10%', marginTop: '5%', width: '80%', height: 'auto' }}>
      <video ref={videoRef} controls style={{ width: '100%', height: 'auto' }} />

      {/* User ID Input */}
      <div style={{ margin: '10px 0' }}>
        <input
          type="text"
          placeholder="Enter User ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          style={{ padding: '10px', width: '200px' }}
        />
        <button onClick={fetchOverlays} style={{ marginLeft: '10px' }}>Load Overlays</button>
        <button onClick={createNewOverlay} style={{ marginLeft: '10px' }}>Create Overlay</button>
        <button  onClick={handleStream}>
            Start Streaming
          </button>
      </div>

      {/* Render existing overlays */}
      {overlays.map((overlay) => (
        <Draggable
          key={overlay._id}
          position={{ x: overlay.position.x, y: overlay.position.y }}
          handle=".drag-handle"  
          onStop={(e, data) => {
            const updatedOverlay = {
              userId: overlay.userId,
              position: { x: data.x, y: data.y },
              size: overlay.size,
              content: overlay.content,
              _id: overlay._id
            };
            
            setOverlays((prevOverlays) =>
              prevOverlays.map((o) =>
                o._id === overlay._id ? updatedOverlay : o
              )
            );

            setCurrentOverlayPosition(updatedOverlay.position); 
          }}
        >
          <ResizableBox
              width={overlay.size.width}
              height={overlay.size.height}
              onResizeStop={(e, { size }) => {
                const updatedOverlay = {
                  ...overlay,
                  size: { width: size.width, height: size.height }
                };

                //Update the overlays state with the new size
                setOverlays((prevOverlays) =>
                  prevOverlays.map((o) =>
                    o._id === overlay._id ? updatedOverlay : o
                  )
                );

              
              }}
              minConstraints={[100, 50]}
              maxConstraints={[600, 300]}
              resizeHandles={['se']}
              handleStyles={{
                se: {
                  position: 'absolute',
                  bottom: '0px',
                  right: '0px',
                  width: '20px',
                  height: '20px',
                  background: 'white',
                  cursor: 'se-resize',
                }
              }}
            >
                <style>
    {`
      .react-resizable-handle-se::after {
        content: '';
        position: absolute;
        width: 12px;
        height: 12px;
        border-right: 2px solid white;
        border-bottom: 2px solid white;
        right: 3px;
        bottom: 3px;
        transform: rotate(0deg);
      }
    `}
  </style>
            <div
              style={{
                position: 'absolute',
                background: 'rgba(0,0,0,0.5)',
                color: 'white',
                padding: '10px',
                width: '100%',
                height: '100%',
              }}
            >
              <div
              className="drag-handle"
                style={{
                  backgroundColor: '#333',
                  color: '#fff',
                  padding: '5px',
                  cursor: 'move',
                  userSelect: 'none',
                  marginBottom: '5px'
                }}
              >
                Drag Me
              </div>

              <div
                contentEditable
                suppressContentEditableWarning
                onBlur={handleContentChange}
                style={{
                  width: '100%',
                  height: '100%',
                  whiteSpace: 'pre-wrap',
                  outline: 'none'
                }}
              >
                {overlay.content.value}
              </div>

              <div style={{ marginTop: '10px' }}>
                <button onClick={() => saveOverlay(overlay)} style={{ marginRight: '5px' }}>
                  Save Overlay
                </button>
                <button onClick={() => updateOverlay(overlay)} style={{ marginRight: '5px' }}>
                  Update Overlay
                </button>
                <button onClick={(e) => deleteOverlay(overlay._id, e)}>
                  Delete Overlay
                </button>
                <button className="no-drag" onClick={() => setOverlays([])}>
                  Cancel
                </button>
              </div>
            </div>
          </ResizableBox>
        </Draggable>
      ))}

      {/* Render the new overlay if it exists */}
      {newOverlay && (
  <Draggable
    position={newOverlay.position}
    onStop={onStop}
    handle=".drag-handle"  // Restrict dragging to only this handle
    // cancel=".no-drag"  // Prevent dragging on other elements
  >
    <ResizableBox
      width={newOverlay.size.width}
      height={newOverlay.size.height}
      onResize={onResize}
      minConstraints={[100, 50]}
      maxConstraints={[600, 300]}
      resizeHandles={['se']}
      handleStyles={{
        se: {
        
          backgroundColor: 'white',
          cursor: 'se-resize',
        }
      }}
    >
            <style>
          {`
            .react-resizable-handle-se::after {
              content: '';
              position: absolute;
              width: 12px;
              height: 12px;
              border-right: 2px solid white;
              border-bottom: 2px solid white;
              right: 3px;
              bottom: 3px;
              transform: rotate(0deg);
            }
          `}
        </style>
      <div
        style={{
          position: 'absolute',
          background: 'rgba(0,0,0,0.5)',
          color: 'white',
          padding: '10px',
          width: '100%',
          height: '100%',
        }}
      >
        {/* "Drag Me" section */}
        <div
          className="drag-handle" // Dragging allowed here
          style={{
            backgroundColor: '#333',
            color: '#fff',
            padding: '5px',
            cursor: 'move',
            userSelect: 'none',
            marginBottom: '5px'
          }}
        >
          Drag Me
        </div>

        {/* Content area - non-draggable */}
        <div
          className="no-drag" // Make this area non-draggable
          contentEditable
          suppressContentEditableWarning
          onBlur={handleContentChange}
          style={{
            width: '100%',
            height: '100%',
            whiteSpace: 'pre-wrap',
            outline: 'none'
          }}
        >
          {newOverlay.content.value}
        </div>

        <div style={{ marginTop: '10px' }}>
          <button className="no-drag" onClick={() => saveOverlay(newOverlay)} style={{ marginRight: '5px' }}>
            Save Overlay
          </button>
          <button className="no-drag" onClick={() => setNewOverlay(null)}>
            Cancel
          </button>
        </div>
      </div>
    </ResizableBox>
  </Draggable>
)}
    
    </div>
  );
}

export default App;
