import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
    return (
        <div className="row m-3">
        <div className="col-md-4 offset-md-4 text-center">
            <Link to="/"><h1 className='m-0'>label<span style={{color: "#777"}}>anything</span></h1></Link>
            <p>An <a href="https://segment-anything.com/">Segment Anything</a> based image annotator</p>
        </div>
        </div>
    );
};

export default Header;