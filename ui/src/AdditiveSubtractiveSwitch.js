import React from 'react';
import ToggleButton from '@mui/material/ToggleButton';
import Card from '@mui/material/Card';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';

import AddCircleIcon from '@mui/icons-material/AddCircle';
import RemoveCircleIcon from '@mui/icons-material/RemoveCircle';

const AdditiveSubtractiveSwitch = ({value, onChange}) => {

  return (
    <>
    {/* <div className="text-center p-3">
        Choose mask type
    </div> */}
          
    <Card>

    <ToggleButtonGroup
    value={value}
    color={value == 'additive' ? "primary": 'error'}
    exclusive
    // onChange={onChange}
    aria-label="marker nature (additive or subtractive)"
  >
    <ToggleButton size="small" onClick={() => {onChange('additive')}} value="additive" aria-label="left aligned">
        <AddCircleIcon className="mr-2" />
        Additive
    </ToggleButton>
    <ToggleButton size="small" onClick={() => {onChange('subtractive')}} value="subtractive" aria-label="left aligned">
        <RemoveCircleIcon className="mr-2" />
        Subtractive
    </ToggleButton>
  </ToggleButtonGroup>
  </Card>
  </>
  );
};

export default AdditiveSubtractiveSwitch;