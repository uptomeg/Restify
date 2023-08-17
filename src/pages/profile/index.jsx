import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import { ajax_or_login } from "../../ajax";

function ProfilePage() {
    return (
      <div>
        <Header />
        <Profile />
        <Footer />
      </div>
    );
  }
  

  function Header() {
    return <div className="header"></div>;
  }
  

  function Footer() {
    return (
    <footer className="text-center text-lg-start bg-light text-muted fixed-bottom">
    <div
        className="text-center p-4"
        style={{ backgroundColor: 'rgba(0, 0, 0, 0.05)' }}
        >
        © 2023 Copyright
    </div>
    </footer>
);
}


function Profile() {
  const navigate = useNavigate();
  const [profileData, setProfileData] = useState({
    avatar: '',
    name: '',
    description: '',
    firstName: '',
    lastName: '',
    email: '',
    phone: ''
  });

  useEffect(() => {
    ajax_or_login("/accounts/profile/", {}, navigate)
    .then(response => response.json())
    .then(json => setProfileData(json))
}, [navigate]);

  const defaultAvatar = 'https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3.webp';

  return (
    <div className="container py-5">
      <div className="row">
        <div className="my-auto">
          <div className="card mb-4 back">
            <div className="card-body text-center">
              <img
                src={profileData.avatar || defaultAvatar}
                alt="avatar"
                className="rounded-circle img-fluid"
                style={{ width: '150px' }}
              />
              <h5 className="my-3">{profileData.name}</h5>
              <p className="text-muted mb-4">{profileData.description}</p>
              <div className="d-flex justify-content-center mb-2">
                <a href="/editprofile/">
                  <button type="button" className="btn btn-warning rounded-9">
                    Edit Profile
                  </button>
                </a>
              </div>
            </div>
          </div>
        </div>

        <div className="my-auto">
          <div className="card mb-4">
            <div className="card-body">
              <div className="row">
                <div className="col-sm-3">
                  <p className="mb-0">First Name</p>
                </div>
                <div className="col-sm-9">
                  <p className="text-muted mb-0">{profileData.first_name}</p>
                </div>
              </div>
              <hr />
              <div className="row">
                <div className="col-sm-3">
                  <p className="mb-0">Last Name</p>
                </div>
                <div className="col-sm-9">
                  <p className="text-muted mb-0">{profileData.last_name}</p>
                </div>
              </div>
              <hr />
              <div className="row">
                <div className="col-sm-3">
                  <p className="mb-0">Email</p>
                </div>
                <div className="col-sm-9">
                  <p className="text-muted mb-0">{profileData.email}</p>
                </div>
              </div>
              <hr />
              <div className="row">
                <div className="col-sm-3">
                  <p className="mb-0">Phone</p>
                </div>
                <div className="col-sm-9">
                  <p className="text-muted mb-0">{profileData.phone_number}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProfilePage;
