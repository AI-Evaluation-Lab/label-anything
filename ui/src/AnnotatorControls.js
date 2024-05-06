import React from 'react';
// import { makeStyles } from '@mui/styles';
import Fab from '@mui/material/Fab';
import Tooltip from '@mui/material//Tooltip';
import UndoIcon from '@mui/icons-material/Undo';
import SaveIcon from '@mui/icons-material/Save';
import CommentIcon from '@mui/icons-material/Comment';

import Stack from '@mui/material/Stack';

// const useStyles = makeStyles((theme) => ({
//   root: {
//     position: 'fixed',
//     bottom: theme.spacing(2),
//     right: theme.spacing(2),
//   },
//   fab: {
//     margin: theme.spacing(1),
//   },
// }));

const AnnotationControls = (props) => {
//   const classes = useStyles();

  const handleUndo = () => {
    // Handle undo action
    console.log('Undo Clicked')
  };

  const handleSave = () => {
    // Handle save action
    console.log('Save Clicked')

  };

  const handleComment = () => {
    // Handle comment action
    console.log('Comment Clicked')

  };

  return (
    <div>
        <Stack className="p-3" spacing={1}>
            <Stack direction="row" alignItems="center" spacing={1}>
    <Tooltip  title="Undo">
        <Fab color="default" size="small" disabled={props.disableUndo} onClick={props.handleUndo}>
          <UndoIcon />
        </Fab>
      </Tooltip>
      <Tooltip  title="Save">
        <Fab color="primary" disabled={props.disableUndo} onClick={props.handleSave}>
          <SaveIcon />
        </Fab>
      </Tooltip>
      <Tooltip  title="Comment">
        <Fab color="primary" size="small" disabled={props.disableUndo} onClick={handleComment}>
          <CommentIcon />
        </Fab>
      </Tooltip>

      </Stack>
      </Stack>
    </div>
  );
};

export default AnnotationControls;