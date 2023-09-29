import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import { ajax_or_login } from "../../ajax";
import styled from '@emotion/styled';

function CreatePropertyPage() {
    return (
      <div>
        <Header />
        <CreateProperty />
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


function CreateProperty() {
  const [images, setImages] = useState([]);
  // const [periodPrices, setPeriodPrices] = useState([{ price: "", startDate: "" }]);
  const navigate = useNavigate();
  const [error, setError] = useState("");

// function handle_submit(event) {
//     let data = new FormData(event.target);

//     ajax_or_login("/property/create/", {
//         method: "POST",
//         body: data,
//     }, navigate)
//     .then(request => request.json())
//     .then(json => {
//         let errorMessages = [];
//         for (let key in json) {
//             if (Array.isArray(json[key])) {
//                 errorMessages.push(`${key}: ${json[key].join(', ')}`);
//             }else if (key === 'error') {
//               errorMessages.push(json[key]);
//           }
//         }
//         if (errorMessages.length > 0) {
//             setError(errorMessages.join('; '));
//         }else{
//             navigate("/yourprofile/");
//         }
//     })
//     .catch(error => {
//         setError(error);
//     });
    
//     event.preventDefault();
// }

// function handle_submit(event) {
//   event.preventDefault();
//   let data = new FormData(event.target);

//   ajax_or_login("/property/create/", {
//     method: "POST",
//     body: data,
//   })
//     .then((request) => request.json())
//     .then((json) => {
//       let propertyId = json.id;
//       const uploadPromises = images.map((image) => {
//         const imageData = new FormData();
//         imageData.append("property", propertyId);
//         imageData.append("image", image);

//         return fetch(`/property/upload-image/${propertyId}/`, {
//           method: "POST",
//           body: imageData,
//         });
//       });

//       return Promise.all(uploadPromises).then(() => json);
//     })
//     .then((json) => {
//       let errorMessages = [];
//       for (let key in json) {
//         if (Array.isArray(json[key])) {
//           errorMessages.push(`${key}: ${json[key].join(", ")}`);
//         } else if (key === "error") {
//           errorMessages.push(json[key]);
//         }
//       }
//       if (errorMessages.length > 0) {
//         setError(errorMessages.join("; "));
//       } else {
//         navigate("/yourprofile/");
//       }
//     })
//     .catch((error) => {
//       setError(error);
//     });
// }

// function renderPeriodPriceInputs() {
//   return periodPrices.map((_, index) => (
//     <div key={index}>
//       <label htmlFor={`price-${index}`}>Price:</label>
//       <input
//         type="number"
//         id={`price-${index}`}
//         name={`price-${index}`}
//         step="0.01"
//         min="0"
//         required
//       />

//       <label htmlFor={`start_date-${index}`}>Start Date:</label>
//       <input
//         type="date"
//         id={`start_date-${index}`}
//         name={`start_date-${index}`}
//         required
//       />
//     </div>
//   ));
// }





function handle_submit(event) {
  event.preventDefault();

  let data = new FormData(event.target);

  ajax_or_login("/property/create/", {
    method: "POST",
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

        // Array.from(periodPrices).forEach((periodprice) => {
        //   const priceData = new FormData();
        //   const price = periodprice.get('price');
        //   const startDate = periodprice.get('start_date');
        //   priceData.append("price", price);
        //   priceData.append("start_date", startDate);

        //   ajax_or_login(`/property/add-price/${propertyId}/`, {
        //       method: "POST",
        //       body: priceData,
        //   }, navigate).then(request => request.json()).then(json => {
        //     let errorMessages = [];
        //     for (let key in json) {
        //         if (Array.isArray(json[key])) {
        //             errorMessages.push(`${key}: ${json[key].join(', ')}`);
        //         }else if (key === 'error') {
        //           errorMessages.push(json[key]);
        //       }
        //     }
        //     if (errorMessages.length > 0) {
        //         setError(errorMessages.join('; '));
        //     }
        // })
        // .catch(error => {
        //     setError(error);
        // });
        // });
        
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

// function handleAddPeriodPrice() {
//   setPeriodPrices([...periodPrices, { price: "", startDate: "" }]);
// }


const ImageContainer = styled.div`
  width: 140px;
  height: 140px;
  background-color: rgb(233, 236, 239);
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 5px;
`;

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
                        <h4 className="pt-sm-2 pb-1 mb-0 text-nowrap">Create Property</h4>
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
                                    <input className="form-control" type="text" name="name" placeholder="Enter your property name"  />
                                  </div>
                                </div>
                              </div>
                              <div className="row">
                                <div className="col">
                                  <div className="form-group">
                                    <label>Location</label>
                                    <input className="form-control" type="text" name="location" placeholder="Enter your address" />
                                  </div>
                                </div>
                              </div>
                              <div className="row">
                                <div className="col mb-3">
                                  <div className="form-group">
                                    <label>Description</label>
                                    <textarea className="form-control" name="description" rows="5" placeholder="Describe your property!"></textarea>
                                  </div>
                                </div>
                              </div>
                              <div className="row">
                                <div className="col">
                                  <div className="form-group">
                                    <label>Capacity</label>
                                    <input className="form-control" type="number" name="capacity" placeholder="Enter capacity" />
                                  </div>
                                </div>
                              </div>
                              <div className="row">
                                <div className="col">
                                  <div className="form-group">
                                    <label>Number of rooms</label>
                                    <input className="form-control" type="number" name="room_number" placeholder="Enter number of rooms"/>
                                  </div>
                                </div>
                              </div>
                              <div className="row">
                                <div className="col">
                                  <div className="form-group">
                                    <label>Number of beds</label>
                                    <input className="form-control" type="number" name="bed_number" placeholder="Enter number of beds"/>
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
};



export default CreatePropertyPage;
