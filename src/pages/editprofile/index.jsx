import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import { ajax_or_login } from "../../ajax";

function EditProfilePage() {
    return (
      <div>
        <Header />
        <EditProfile />
        <Footer />
      </div>
    );
  }
  

  function Header() {
    return <div className="header"></div>;
  }
  

  function Footer() {
    return (
    <footer className="text-center text-lg-start bg-light text-muted absolute-bottom">
    <div
        className="text-center p-4"
        style={{ backgroundColor: 'rgba(0, 0, 0, 0.05)' }}
        >
        © 2023 Copyright
    </div>
    </footer>
);
}


function EditProfile() {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [profileData, setProfileData] = useState([]);
//   {
//     avatar: '',
//     first_name: '',
//     last_name: '',
//     username:'',
//     email: '',
//     phone_number: '',
//     description: ''
//   }


  useEffect(() => {
    ajax_or_login("/accounts/profile/", {}, navigate)
    .then(response => response.json())
    .then(json => setProfileData(json))
}, [navigate]);



function handle_submit(event) {
    let data = new FormData(event.target);

    ajax_or_login("/accounts/profile/", {
        method: "PUT",
        body: data,
    }, navigate)
    .then(request => request.json())
    .then(json => {
        let errorMessages = [];
        for (let key in json) {
            if (Array.isArray(json[key])) {
                errorMessages.push(`${key}: ${json[key].join(', ')}`);
            }else if (key === 'error') {
              errorMessages.push(json[key]);
          }
        }
        if (errorMessages.length > 0) {
            setError(errorMessages.join('; '));
        }else{
            navigate("/yourprofile/");
        }
    })
    .catch(error => {
        setError(error);
    });
    
    event.preventDefault();
}


  const handleCancel = () => {
    navigate('/yourprofile/');
  };
  
  const defaultAvatar = 'https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3.webp';
  return (
    <div className="row">
    <form onSubmit={handle_submit}>
      <div className="my-auto">
        <div className="card mb-4 back">
          <div className="card-body text-center">
          <img
                src={profileData.avatar || defaultAvatar}
                alt="avatar"
                className="rounded-circle img-fluid"
                style={{ width: '150px' }}
              />
            <p className="text-muted">Upload new avatar</p>
            <div className="d-flex justify-content-center mb-2">
              <input
                className="form-control form-control-sm"
                id="formFileSm"
                type="file"
                placeholder="Upload new image"
                name="avatar"
              />
            </div>
          </div>
        </div>

        <div className="my-auto">
          <div className="card mb-4">
            <div className="card-body">
              <div className="row">
                <div className="col-sm-3">
                  <p className="mb-0 my-3">First Name</p>
                </div>
                <div className="col-sm-9">
                  <input
                    type="text"
                    className="form-control my-3"
                    defaultValue={profileData.first_name}
                    name="first_name"
                  />
                </div>
              </div>
              <div className="row">
                <div className="col-sm-3">
                  <p className="mb-0 my-3">Last Name</p>
                </div>
                <div className="col-sm-9">
                  <input
                    type="text"
                    className="form-control my-3"
                    defaultValue={profileData.last_name}
                    name="last_name"
                  />
                </div>
              </div>

              {/* <div className="row">
                <div className="col-sm-3">
                  <p className="mb-0 my-3">Username</p>
                </div>
                <div className="col-sm-9">
                  <input
                    type="text"
                    className="form-control my-3"
                    defaultValue={profileData.username}
                    name="username"
                  />
                </div>
              </div> */}

              <div className="row">
                <div className="col-sm-3">
                  <p className="mb-0 my-3">Email</p>
                </div>
                <div className="col-sm-9">
                  <input
                    type="text"
                    className="form-control my-3"
                    defaultValue={profileData.email}
                    name="email"
                  />
                </div>
              </div>


              <div className="row">
                <div className="col-sm-3">
                  <p className="mb-0 my-3">Phone Number</p>
                </div>
                <div className="col-sm-9">
                  <input
                    type="text"
                    className="form-control my-3"
                    defaultValue={profileData.phone_number}
                    name="phone_number"
                  />
                </div>
              </div>
            
              <div className="row">
                <div className="col-sm-3">
                  <p className="mb-0 my-3">Password</p>
                </div>
                <div className="col-sm-9">
                  <input
                    type="text"
                    className="form-control my-3"
                    defaultValue={profileData.password}
                    name="password"
                  />
                </div>
              </div>

              <div className="row">
                <div className="col-sm-3">
                  <p className="mb-0 my-3">Confirmed Password</p>
                </div>
                <div className="col-sm-9">
                  <input
                    type="text"
                    className="form-control my-3"
                    defaultValue={profileData.password_confirmation}
                    name="password_confirm"
                  />
                </div>
              </div>
              
              <p className="error">{error}</p>

              <div className="d-flex flex-row-reverse">
                <button
                  type="submit"
                  id="submit"
                  name="submit"
                  className="btn btn-warning rounded-9 me-2"
                >
                  Update
                </button>
                <button
                  type="button"
                  id="submit"
                  name="submit"
                  className="btn btn-secondary me-2 rounded-9"
                  onClick={handleCancel}
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </form>
    </div>
  );
}

export default EditProfilePage;
