import React, { useEffect, useState } from 'react';
import { styled } from '@mui/material/styles';
import PrettyJson from './PrettyJson';
import { useNavigate } from 'react-router-dom';
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import { CardActionArea } from '@mui/material';
import LinearProgress, { linearProgressClasses } from '@mui/material/LinearProgress';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import moment from 'moment';

const BorderLinearProgress = styled(LinearProgress)(({ theme }) => ({
    height: 10,
    borderRadius: 5,
    [`&.${linearProgressClasses.colorPrimary}`]: {
        backgroundColor: theme.palette.grey[theme.palette.mode === 'light' ? 200 : 800],
    },
    [`& .${linearProgressClasses.bar}`]: {
        borderRadius: 5,
        backgroundColor: theme.palette.mode === 'light' ? '#1a90ff' : '#308fe8',
    },
}));

const ImageList = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch(`http://localhost:5000/images`);
            const data = await response.json();
            setImages(data);
        };

        fetchData();
    }, []);

    const [images, setImages] = useState([]);

    const calculateProgress = (image) => {
        const totalMasks = Object.keys(image.masks).length;
        let count = 0;

        for (const key in image.masks) {
            if (image.masks[key]['path'].length !== 0) {
                count++;
            }
        }
        return { total: totalMasks, count: count, progress: count / totalMasks };
    };

    return (
        <div className="row pt-4">
            <div className="container">
                <div className="row">
                    <div className="col-md-12 text-center mb-3">
                        <h2>labelanything</h2>
                        <p>Yet another SAM annotation tool</p>
                    </div>

                    {images.map(image => (
                        <div className="col-md-3 mb-3" key={image.id}>
                            <Card className="">
                                <CardActionArea onClick={() => { navigate(`/images/${image.id}`); }}>

                                    <CardMedia
                                        sx={{ height: 140 }}
                                        image={`http://localhost:5000/images/${image.id}/png`}
                                    >
                                        <Stack className="p-3" spacing={1}>
                                            <Stack direction="column-reverse" alignItems="flex-start" justifyContent="flex-start" spacing={1}>
                                                {calculateProgress(image).count / calculateProgress(image).total > 0 && calculateProgress(image).count / calculateProgress(image).total < 1 && <Chip size="small" label={"Started (" + calculateProgress(image).count + "/" + calculateProgress(image).total + ")"} color="warning" />}
                                                {calculateProgress(image).count / calculateProgress(image).total === 0 && <Chip size="small" label="Not Started" color="error" />}
                                                {calculateProgress(image).count / calculateProgress(image).total === 1 && <Chip size="small" label="Completed" color="success" />}
                                                {image.is_difficult && <Chip size="small" label="Difficult" color="warning" />}
                                            </Stack>
                                        </Stack>
                                    </CardMedia>
                                </CardActionArea>

                                <div className="p-3">
                                    <span><small>Last updated: {moment(image.date_updated, 'YYYY-MM-DD HH:mm:ss').fromNow()}</small></span>
                                </div>
                            </Card>
                        </div>
                    ))}
                </div>

                {/* <PrettyJson data={images} /> */}
            </div>
        </div>
    );
};

export default ImageList;
