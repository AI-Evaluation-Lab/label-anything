import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

import { useParams, useLocation } from 'react-router-dom';
import AnnotationControls from './AnnotatorControls';
import AdditiveSubtractiveSwitch from './AdditiveSubtractiveSwitch';


const ImageAnnotator = () => {
    const { id, type } = useParams();
    const navigate = useNavigate();

    const [jsonData, setJsonData] = useState(null)
    useEffect(() => {
      const fetchJSON = async () => {
        try {
          const response = await fetch(`${process.env.PUBLIC_URL}/masks.json`);
          const data = await response.json();
          const typeInfo = data.filter(d=>d.type == type)[0]
          console.log(typeInfo, type)
          setJsonData(typeInfo);
        } catch (error) {
          console.error('Error fetching JSON data:', error);
        }
      };
  
      fetchJSON();
    }, []);
    
    const imageUrl = `http://localhost:5000/images/${id}/png`
    const [markers, setMarkers] = useState([]);
    const [labels, setLabels] = useState([]);
    const [markerType, setMarkerType] = useState(['additive']);
    // const [imageUrl, setImageUrl] = useState(`http://localhost:5000/images/${id}/png`);
    const [maskUrl, setMaskUrl] = useState(imageUrl);
    const [refreshFlag, setRefreshFlag] = useState(false);
    const [imageWidth, setImageWidth] = useState(0);
    const [imageHeight, setImageHeight] = useState(0);
    const [shouldRenderMask, setShouldRenderMask] = useState(true);

    const markerTypeToLabel = {
      "additive": 1,
      "subtractive": 0
    } 

    const labelToColor = {
      1:"green",
      0: "red" 
    }

    // useEffect(() => {
    //     fetchMask();
    // }, [refreshFlag]);

    useEffect(() => {
      if (markers.length ==0) {
        console.log('Ooh', markers)
        setMaskUrl(imageUrl)
      }

      if (markers.length > 0) {
          fetchMask();
      }
    }, [markers]);

    const fetchMask = () => {
      

        axios.get(`http://localhost:5000/images/${id}/mask`, { params: { markers: JSON.stringify(markers), labels: JSON.stringify(labels) }, responseType: 'blob' })
            .then(response => {
                setMaskUrl(URL.createObjectURL(response.data));
                setShouldRenderMask(true);
                setRefreshFlag(false);
            })
            .catch(error => {
                console.error('Error fetching mask:', error);
            });
    };

    const addMarker = (event) => {
        const { offsetX, offsetY } = event.nativeEvent;
        console.log("Oiya", markerType)
        setMarkers(prevMarkers => [...prevMarkers, { x: offsetX, y: offsetY }]);
        setLabels(prevLabels=> [...prevLabels, markerTypeToLabel[markerType]])
        // fetchMask();
    };

    const saveMarkers = () => {
      // save markers
      axios.patch(`http://localhost:5000/images/${id}/mask`, {
        markers: JSON.stringify(markers),
        labels: JSON.stringify(labels),
        type: type
      }, {
        responseType: 'blob'
      })
        .then(response => {
          setMaskUrl(URL.createObjectURL(response.data));
          setShouldRenderMask(true);
          setRefreshFlag(false);
          
        }).then(()=> {
          console.log('trigger navigate')
          navigate(`/images/${id}`)
        })
        .catch(error => {
          console.error('Error fetching mask:', error);
        });
    };

    const handleImageLoad = (event) => {
        setImageWidth(event.target.width);
        setImageHeight(event.target.height);
    };

    const handleUndo = () => {
      // markers.pop()
      setMarkers(prevMarkers => prevMarkers.slice(0, -1))
      setLabels(prevLabels => prevLabels.slice(0, -1))
      // fetchMask()
    
    }

    const handleMarkerTypeChange= (newType) => {
      // markers.pop()
      setMarkerType(newType)
      console.log(newType)
      // fetchMask()
    
    }

    return (
        <div style={{ position: 'relative', margin: '0 auto', width: 'fit-content', backgroundColor: "black" }}>
            <div style={{ position: 'relative', overflow: 'scroll' }}>
                <img
                    src={imageUrl}
                    alt="Annotated Image"
                    onClick={addMarker}
                    style={{ display: 'block', margin: '0 auto' }}
                    onLoad={handleImageLoad}
                />
                {shouldRenderMask && (
                    <div style={{ position: 'absolute', top: 0, left: 0 }}>
                        <img
                            src={maskUrl}
                            alt="Mask"
                            style={{
                                position: 'relative',
                                top: 0,
                                left: 0,
                                width: imageWidth,
                                height: imageHeight,
                                opacity: 0.5,
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
                            }}
                        />
                    </div>
                )}
                {markers.map((marker, index) => 
                    {
                      const color = labelToColor[labels[index]]
                      return (<div
                        key={index}
                        style={{
                            position: 'absolute',
                            left: marker.x,
                            top: marker.y,
                            width: 10,
                            height: 10,
                            backgroundColor: color,
                            borderRadius: '50%',
                            border: '2px solid white',
                            transform: 'translate(-50%, -50%)',
                        }}
                    />)}
                )}
            </div>
            <div style={{ position: 'fixed', top: '2%', left: '43%', translate: 'translateX(-50%)', zIndex: 10000}}>
              <AnnotationControls handleUndo={handleUndo} handleSave={saveMarkers} disableUndo={markers.length==0}/>
            </div>

            {jsonData && <div className="p-3" style={{borderRadius:'10px', position: 'fixed', top: '2%', left: '2%', translate: 'translateX(-50%)', zIndex: 10000, backgroundColor:'rgba(0,0,0,0.3)', color:'#fff'}}>
              <span><small>Currently labeling:</small></span>
              <h3 >{jsonData.label}</h3>
            </div>}

            <div style={{ position: 'fixed', top: '85vh', left: '41%', translate: 'translateX(-50%)', zIndex: 10000}}>
              <AdditiveSubtractiveSwitch onChange={handleMarkerTypeChange} value={markerType}/>
            </div>
            {/* <button style={{ position: 'absolute', top: 15, left: 15 }} onClick={saveMarkers}>Save Markers</button> */}
        </div>
    );
};

export default ImageAnnotator;
