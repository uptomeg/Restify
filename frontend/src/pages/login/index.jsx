import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useNavigate } from 'react-router-dom';
import { ajax } from '../../ajax';
import './login.css';



function LoginPage() {
  return (
    <div>
      <Header />
      <MainContent />
      <Footer />
    </div>
  );
}

function Header() {
  return <div className="header"></div>;
}

function MainContent() {
  return (
    <div className="container d-flex flex-column flex-lg-row justify-content-evenly mt-5 pt-5">
      <Heading />
      <LoginForm />
    </div>
  );
}

function Heading() {
  return (
    <div className="text-center text-lg-start mt-lg-5 pt-lg-5">
      <h1 className="text-warning fw-bold fs-lg">Restify</h1>
      <p className="w-75 mx-auto mx-lg-0 fs-4 writer">
        Your home everywhere you go.
      </p>
    </div>
  );
}

function LoginForm() {
const [error, setError] = useState("");
const navigate = useNavigate();
function handle_submit(event) {
    let data = new FormData(event.target);

    ajax("/api/token/", {
        method: "POST",
        body: data,
    })
    .then(request => request.json())
    .then(json => {
        if ('access' in json) {
            localStorage.setItem('access', json.access);
            localStorage.setItem('username', data.get('username'));
            navigate('/'); //note主页面
        }
        else if ('detail' in json) {
            setError(json.detail);
        }
        else {
            setError("Unknown error while signing in.")
        }
    })
    .catch(error => {
        setError(error);
    });

    event.preventDefault();
}


  return (
    <div style={{ maxWidth: '28rem', width: '100%' }}>
      <div className="bg-success-subtle shadow rounded p-3 input-group-lg">
      <form onSubmit={handle_submit}>
      <input
        type="text"
        className="form-control my-3"
        placeholder="Enter your username"
        id="username" name="username"
        required
      />
      <input
        type="password"
        className="form-control my-3"
        placeholder="Password"
        id="password" name="password"
        required
      />
      <button type="submit" className="btn btn-primary w-100 my-3 rounded-9">
        Log In
      </button>
      <p className="error">{error}</p>
    </form>
    <hr />
    <div className="text-center my-4">
          <p className="text-secondary">New to Restify?</p>
          <button className="btn btn-warning btn-lg" data-bs-toggle="modal" data-bs-target="#createModal">Create New Account</button>
    </div>
    <SignUpSection />
  </div>
</div>

);
}



function SignUpSection() {
  return (
    <div className="modal fade" id="createModal" tabindex="-1" aria-labelledby="createModalLabel" aria-hidden="true">
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header">
            <h1 className="modal-title fs-5 fw-bold">Create your account</h1>
            <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div className="modal-body">
            <SignUpForm />
          </div>
        </div>
      </div>
    </div>
  );
}

function SignUpForm() {
    const [error, setError] = useState("");

    function handle_submit(event) {
        let data = new FormData(event.target);

        ajax("/accounts/signup/", {
          method: "POST",
          body: data,
        })
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
          window.location.reload();
        }
      })
      .catch(error => {
          setError(error);
      });
  
      event.preventDefault();
  }
  
  return (
    <form onSubmit={handle_submit}>
      <div className="row">
        <div className="col">
          <input type="text" className="form-control" placeholder="First name" id="first_name" name="first_name"/>
        </div>
        <div className="col">
          <input type="text" className="form-control" placeholder="Last name" id="last_name" name="last_name"/>
        </div>
      </div>
      <input
        type="text"
        className="form-control my-3"
        placeholder="Your username"
        name="username"
        required
      />
      <input
        type="email"
        className="form-control my-3"
        placeholder="Your email address or phone number"
        name="email"
      />
      <input
        type="password" 
        className="form-control my-3"
        placeholder="Your password"
        name="password"
        required
      />
      <input
        type="password" 
        className="form-control my-3"
        placeholder="Password Confirmation"
        id="password_confirm" name="password_confirm"
        required
      />
      <p className="error">{error}</p>
        <div>
            <div className="form-check">
                <input
                    className="form-check-input"
                    type="checkbox"
                    id="check1"
                    name="option1"
                    value="something"
                    required
                />
                <label className="form-check-label text-secondary fs-sm">
                By clicking Sign Up, you agree to our terms and policies
                </label>
            </div>
        </div>
        <div className="text-center mt-3">
                <button type="submit" className="btn btn-success btn-lg">
                Sign Up
                </button>
        </div>
    </form>
    );
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
        
export default LoginPage;
