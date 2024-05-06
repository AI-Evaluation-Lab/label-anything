import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
// import PrettyJson from './PrettyJson';
import { useNavigate } from 'react-router-dom';

import Card from '@mui/material/Card';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Avatar from '@mui/material/Avatar';
import Chip from '@mui/material/Chip';
import Button from '@mui/material/Button';
import EastIcon from '@mui/icons-material/East';
import Header from './Header';


const ImageDetails = () => {
  const navigate = useNavigate();
  
  const { id } = useParams();
  const [imageData, setImageData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(`http://localhost:5000/images/${id}`);
      const data = await response.json();
      setImageData(data);
    };
    fetchData();
  }, [id]);

  const calculateProgress = (image) => {
    const totalMasks = Object.keys(image.masks).length;
    let count = 0;

    for (const key in image.masks) {
      if (image.masks[key].length !== 0) {
        count++;
      }
    }
    // console.log(total, )
    return { total: totalMasks, count: count, progress: count / totalMasks };
  };

  return (
    <>
    <Header/>
    <div className="row m-3">
      <div className="container">
        {imageData ? (
          <div className="col-md-8 offset-md-2">
            <Card>
              <img className="img-fluid" src={`http://localhost:5000/images/${id}/png`} alt={imageData.title} />
              <div className="row p-3">
                <div className="col-md-12 ">
                  <h3>Masks</h3>
                  {calculateProgress(imageData).count === 0 && <p className="m-0">There are no masks for this specific image.</p>}
                </div>
              </div>
              <div className="row">
                <List className="p-3" sx={{ width: '100%', bgcolor: 'background.paper' }}>
                  {Object.keys(imageData.masks).map((d) => (
                    <>
                      <ListItem alignItems="" secondaryAction={
                        <React.Fragment>
                          {imageData.masks[d].path !== "" && (
                            <Button onClick={()=>{navigate(`/images/${imageData.id}/annotate/${d}`, { state: { imageData: imageData } });}} size="small" variant="contained" endIcon={<EastIcon />}>
                              <small>Redo Segmentation</small>
                            </Button>
                          )}  
                          {imageData.masks[d].path === "" && (
                            <Button onClick={()=>{navigate(`/images/${imageData.id}/annotate/${d}`, { state: { imageData: imageData } });}} size="small" variant="contained" endIcon={<EastIcon />}>
                              <small>Start Segmenting</small>
                            </Button>
                          )}
                        </React.Fragment>
                      }>
                        <ListItemAvatar>
                          {imageData.masks[d].path === "" && <Avatar sx={{ bgcolor: imageData.masks[d].background }}>{d}</Avatar>}
                          {imageData.masks[d].path !== "" && <Avatar src={`http://localhost:5000/images/${imageData.id}/mask/${d}/png`}>{d}</Avatar>}
                        </ListItemAvatar>
                        <ListItemText
                          id={d}
                          primary={
                            <React.Fragment>
                              {imageData.masks[d].label}
                              {imageData.masks[d].path === "" && <Chip className="ml-2" size="small" label="Not Started" />}
                              {imageData.masks[d].path !== "" && <Chip className="ml-2" size="small" color="success" label="Mask Ready" />}
                            </React.Fragment>
                          }
                          secondary={<React.Fragment>{imageData.masks[d].description}</React.Fragment>}
                        />
                      </ListItem>
                    </>
                  ))}
                </List>
              </div>
              {/* <PrettyJson data={imageData}/> */}
            </Card>
          </div>
        ) : (
          <p>Loading...</p>
        )}
      </div>
    </div>
    </>
  );
};

export default ImageDetails;
