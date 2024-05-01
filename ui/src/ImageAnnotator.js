import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ImageAnnotator = () => {
  const [markers, setMarkers] = useState([]);
  const [imageUrl, setImageUrl] = useState('http://localhost:5000/image/1183.png');
  const [maskUrl, setMaskUrl] = useState('http://localhost:5000/image/1183.png');
  const [refreshFlag, setRefreshFlag] = useState(false); // State variable to force a re-render
  const [imageWidth, setImageWidth] = useState(0);
  const [imageHeight, setImageHeight] = useState(0);
  const [shouldRenderMask, setShouldRenderMask] = useState(true); // State variable to toggle mask rendering

  useEffect(() => {
    fetchMask(); // Fetch the initial mask
  }, [refreshFlag]);



  const fetchMask = () => {
    // Fetch the mask from the backend, passing the current markers
    axios.get('http://localhost:5000/getMask', { params: { markers: JSON.stringify(markers) }, responseType: 'blob' })
      .then(response => {
        setMaskUrl(URL.createObjectURL(response.data)); // Set the image URL to force re-render of the image
        setShouldRenderMask(true); // Toggle the state to force re-render of the mask
        setRefreshFlag(false); // Reset the refreshFlag after fetch
      })
      .catch(error => {
        console.error('Error fetching mask:', error);
      });
  };

  const addMarker = (event) => {
    const { offsetX, offsetY } = event.nativeEvent;
    const newMarker = { x: offsetX, y: offsetY };
    setMarkers([...markers, newMarker]);
    // setRefreshFlag(!refreshFlag); // Set the refreshFlag to trigger a re-render
    fetchMask(); // Trigger the GET request when the user clicks on the image
  };

  const saveMarkers = () => {
    // Make an API call to save markers
    axios.post('https://api.example.com/save', { markers })
      .then(response => {
        console.log('Markers saved:', response.data);
      })
      .catch(error => {
        console.error('Error saving markers:', error);
      });
  };

  const handleImageLoad = (event) => {
    setImageWidth(event.target.width);
    setImageHeight(event.target.height);
  };

  return (
    <div style={{ position: 'relative', display: 'inline-block' }}>
      <img
        src={imageUrl}
        alt="Annotated Image"
        onClick={addMarker}
        style={{ position: 'relative' }}
        onLoad={handleImageLoad}
      />
      {shouldRenderMask && (
        <div style={{ position: 'absolute', top: 0, left: 0 }}>
          <img
            src={maskUrl} // Use the same image URL for the mask to force re-render
            alt="Mask"
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: imageWidth,
              height: imageHeight,
              opacity: 0.5, // Adjust the opacity as needed
            }}
          />
          <div
            onClick={addMarker}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: imageWidth,
              height: imageHeight,
            //   pointerEvents: 'none', // Allow clicks to pass through
            }}
          />
        </div>
      )}
      {markers.map((marker, index) => (
        <div
          key={index}
          style={{
            position: 'absolute',
            left: marker.x,
            top: marker.y,
            width: 10,
            height: 10,
            backgroundColor: 'red',
            borderRadius: '50%',
            transform: 'translate(-50%, -50%)',
          }}
        />
      ))}
      <button onClick={saveMarkers}>Save Markers</button>
    </div>
  );
};

export default ImageAnnotator;
