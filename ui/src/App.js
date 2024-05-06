import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ImageList from './ImageList';
import ImageDetails from './ImageDetails';
import ImageAnnotator from './ImageAnnotator';


function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<ImageList />} />
                <Route path="/images/:id" element={<ImageDetails />} />
                <Route path="/images/:id/annotate/:type" element={<ImageAnnotator />} />
            </Routes>
        </Router>
    );
}

export default App;