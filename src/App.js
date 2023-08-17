import { BrowserRouter, Route, Routes, useParams } from 'react-router-dom';
import './App.css';
import LoginPage from './pages/login';
import ProfilePage from './pages/profile';
import EditProfilePage from './pages/editprofile';
import EditPropertyPage from './pages/editproperty';
import CreatePropertyPage from './pages/createproperty';
import ReservationsPageC from './pages/reservationlist/indexclient';
import ReservationsPageH from './pages/reservationlist/indexhost';




function App() {
  return <BrowserRouter>
    <Routes>
      <Route path="/login/" exact element={<LoginPage />} />
    </Routes>
    <Routes>
      <Route path="/yourprofile/" exact element={<ProfilePage />} />
    </Routes>
    <Routes>
      <Route path="/editprofile/" exact element={<EditProfilePage />} />
    </Routes>
    <Routes>
      <Route path="/createproperty/" exact element={<CreatePropertyPage />} />
    </Routes>
    <Routes>
      <Route path="/editproperty/:pk" exact element={<EditPropertyPage />} />
    </Routes>
    <Routes>
      <Route path="/reservationsclient/" exact element={<ReservationsPageC />} />
    </Routes>
    <Routes>
      <Route path="/reservationshost/" exact element={<ReservationsPageH />} />
    </Routes>
  </BrowserRouter>;
}

export default App;
