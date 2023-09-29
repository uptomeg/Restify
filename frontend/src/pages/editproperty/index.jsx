import React, { useState, useEffect } from 'react';
import { useNavigate , useParams } from "react-router-dom";
import { ajax_or_login } from "../../ajax";
import styled from '@emotion/styled';


function EditPropertyPage() {
    return (
      <div>
        <Header />
        <EditProperty />
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



function EditProperty() {
    const { pk } = useParams();
    const [propertyData, setPropertyData] = useState({});
  const [images, setImages] = useState([]);
  const navigate = useNavigate();
  const [error, setError] = useState("");
    // const [periodPrices, setPeriodPrices] = useState([{ price: "", startDate: "" }]);

    useEffect(() => {
        ajax_or_login(`/property/update/${pk}/`, {}, navigate)
          .then(response => response.json())
          .then(json => setPropertyData(json))
      }, [navigate, pk]);
    
      useEffect(() => {
        if (propertyData.images) {
          setImages(propertyData.images);
        }
      }, [propertyData]);
    
  
    const handleDeleteImage = (propertyId, imageId) => {
      ajax_or_login(`/property/delete-image/${propertyId}/${imageId}/`, {
        method: "DELETE",
      }, navigate)
        .then(() => {
          setImages(images.filter(image => image.id !== imageId));
        })
        .catch(error => {
          setError(error);
        });
    };

    // const handleDeleteProperty = () => {
    //     ajax_or_login(`/property/delete/${pk}/`, {
    //       method: "DELETE",
    //     }, navigate)
    //       .then(() => {
    //         navigate("/yourprofile/");
    //       })
    //       .catch(error => {
    //         setError(error);
    //       });
    //   };    
      
      
    function handle_submit(event) {
    event.preventDefault();
  
    let data = new FormData(event.target);
  
    ajax_or_login("/property/create/", {
      method: "PUT",
      body: data,
    }, navigate)
      .then((request) => request.json())
      .then((json) => {
        if ('id' in json) {
          const propertyId = json['id'];
  
          Array.from(images).forEach((image) => {
            const imageData = new FormData();
            imageData.append("image", image);
            ajax_or_login(`/property/upload-image/${propertyId}/`, {
                method: "POST",
                body: imageData,
            }, navigate).then(request => request.json()).then(json => {
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
              }
          })
          .catch(error => {
              setError(error);
          });
          });
        } else {
          let errorMessages = [];
          for (let key in json) {
            if (Array.isArray(json[key])) {
              errorMessages.push(`${key}: ${json[key].join(', ')}`);
            } else if (key === "error") {
              errorMessages.push(json[key]);
            }
          }
          if (errorMessages.length > 0) {
            setError(errorMessages.join("; "));
          } else {
            navigate("/yourprofile/");
          }
        }
      })
      .catch((error) => {
        setError(error);
      });
  }
  
  
  
  
  const handleImageChange = (event) => {
    // const newImages = Array.from(event.target.files);
    // setImages([...images, ...newImages]);
    const files = event.target.files;
    setImages([...images, ...files]);
  };
  
    return (
      <div className="container">
           <div className="row flex-lg-nowrap">
      <div className="col">
        <div className="row">
          <div className="col mb-3">
            <div className="card">
              <div className="card-body">
                <div className="e-profile">
                  <div className="row">
                    <div className="col-12 col-sm-auto mb-3">
                      <div className="mx-auto" style={{ width: '140px' }}>
                        <div className="d-flex justify-content-center align-items-center rounded" style={{ height: '140px', backgroundColor: 'rgb(233, 236, 239)' }}>
                          <span style={{ color: 'rgb(166, 168, 170)', font: 'bold 8pt Arial' }}>140x140</span>
                        </div>
                      </div>
                    </div>
                    <div className="col d-flex flex-column flex-sm-row justify-content-between mb-3">
                      <div className="text-center text-sm-left mb-2 mb-sm-0">
                        <h4 className="pt-sm-2 pb-1 mb-0 text-nowrap">Edit Property</h4>
                        <div className="mt-2">
                          <label htmlFor="image-upload" className="btn btn-warning">
                            <i className="fa fa-fw fa-camera"></i>
                            <span>Change Photo</span>
                          </label>
                        </div>
                      </div>
                      <div className="text-center text-sm-right">
                        <span className="badge badge-secondary">Hotel</span>
                        <div className="text-muted">
                          <small>Available from Dec 2017</small>
                        </div>
                      </div>
                    </div>
                  </div>
                  <ul className="nav nav-tabs">
                    <li className="nav-item">
                      <a href="" className="active nav-link">
                        Settings
                      </a>
                    </li>
                  </ul>
                  <div className="tab-content pt-3">
                    <div className="tab-pane active">
        <form className="form" onSubmit={handle_submit}>
                          <div className="row">
                            <div className="col">
                              <div className="row">
                                <div className="col">
                                  <div className="form-group">
                                    <label>Property Name</label>
                                    <input className="form-control" type="text" name="name" defaultValue={propertyData.name}  />
                                  </div>
                                </div>
                              </div>
                              <div className="row">
                                <div className="col">
                                  <div className="form-group">
                                    <label>Location</label>
                                    <input className="form-control" type="text" name="location" defaultValue={propertyData.location}  />
                                  </div>
                                </div>
                              </div>
                              <div className="row">
                                <div className="col mb-3">
                                  <div className="form-group">
                                    <label>Description</label>
                                    <textarea className="form-control" name="description" rows="5" defaultValue={propertyData.description} ></textarea>
                                  </div>
                                </div>
                              </div>
                              <div className="row">
                                <div className="col">
                                  <div className="form-group">
                                    <label>Capacity</label>
                                    <input className="form-control" type="number" name="capacity" defaultValue={propertyData.capacity} />
                                  </div>
                                </div>
                              </div>
                              <div className="row">
                                <div className="col">
                                  <div className="form-group">
                                    <label>Number of rooms</label>
                                    <input className="form-control" type="number" name="room_number" defaultValue={propertyData.room_number}/>
                                  </div>
                                </div>
                              </div>
                              <div className="row">
                                <div className="col">
                                  <div className="form-group">
                                    <label>Number of beds</label>
                                    <input className="form-control" type="number" name="bed_number" defaultValue={propertyData.bed_number}/>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                          <hr />
                          <p className="error">{error}</p>
                          <div className="row">
                            <div className="col d-flex justify-content-end">
                              <button className="btn btn-warning" type="submit">
                                Save Changes
                              </button>
                            </div>
                          </div>
                          {/* <div>{renderPeriodPriceInputs()}</div>
                          <button type="button" onClick={handleAddPeriodPrice}>
                            Add Period Price
                          </button> */}
                          <input type="file" id="image-upload" onChange={handleImageChange} />
                          {/* <input
                            type="file"
                            id="image-upload"
                            multiple
                            style={{ display: 'none' }}
                            onChange={handleImageChange}
                          /> */}
                        </form>




        {/* Render images and delete buttons */}
        <div>
          {images.map((image) => (
            <div key={image.id}>
              <img src={image.url} alt="" width="100" />
              <button
                type="button"
                onClick={() => handleDeleteImage(pk, image.id)}
              >
                Delete Image
              </button>
            </div>
          ))}
        </div>
        <div className="text-center my-4">
          <p className="text-secondary">Do you want to delete this property?</p>
          <button className="btn btn-warning btn-lg" data-bs-toggle="modal" data-bs-target="#createModal">Delete</button>
        </div>
        <DeleteSection />


        {/* Delete property button */}
        {/* <button type="button" onClick={handleDeleteProperty}>
          Delete Property
        </button> */}
      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="col-12 col-md-3 mb-3">
              <div className="card">
                <div className="card-body">
                  <h6 className="card-title font-weight-bold">Support</h6>
                  <p className="card-text">Get fast, free help from our friendly assistants.</p>
                  <a href="message.html">
                    <button type="button" className="btn btn-warning">
                      Contact Us
                    </button>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    );
  }
  
 
  


  function DeleteSection() {
    return (
      <div className="modal fade" id="createModal" tabindex="-1" aria-labelledby="createModalLabel" aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h1 className="modal-title fs-5 fw-bold">Warning</h1>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div className="modal-body">
              <DeleteForm />
            </div>
          </div>
        </div>
      </div>
    );
  }
  
  function DeleteForm() {
    const { pk } = useParams();
      const [error, setError] = useState("");
      const navigate = useNavigate();

      const handleDeleteProperty = () => {
      ajax_or_login(`/property/delete/${pk}/`, {
        method: "DELETE",
      }, navigate)
        .then(() => {
          navigate("/yourprofile/");
        })
        .catch(error => {
          setError(error);
        });
    };
 

  
    
    return (
      <form onSubmit={handleDeleteProperty}>
          <p>Are you sure you want to delete this property? This action cannot be undone.</p>
          <div className="text-center mt-3">
                  <button type="submit" className="btn btn-danger btn-lg">
                  DELETE
                  </button>
          </div>
      </form>
      );
  }
   



export default EditPropertyPage;
