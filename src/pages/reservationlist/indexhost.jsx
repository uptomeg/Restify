import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useNavigate } from 'react-router-dom';
import { ajax_or_login } from '../../ajax';
import './style.css';
import Reservation from '../../components/Reservations';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus, faGlobeAsia, faTag } from '@fortawesome/free-solid-svg-icons';
import Pagination from 'react-bootstrap/Pagination';



function ReservationsPageH() {
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

function MainContent(){
    const navigate = useNavigate();
    const [ reservationshost, setReservationshost ] = useState([]);
    const [currentPage, setCurrentPage] = useState({
        pending: 1,
        denied: 1,
        expired: 1,
        approved: 1,
        cancelled: 1,
        terminated: 1,
        completed: 1,
      });
      const itemsPerPage = 5;

    useEffect(() => {
        ajax_or_login("/reservations/host/all/", {}, navigate)
          .then(response => response.json())
          .then(json => {
            if (json === null) {
              setReservationshost([]);
            } else if (Array.isArray(json)) {
              setReservationshost(json);
            } else {
              console.error('Unexpected data format:', json);
            }
          });
      }, [navigate]);

    
    // useEffect(() => {
    //     ajax_or_login("/reservations/host/all/", {}, navigate)
    //     .then(response => response.json())
    //     .then(json => setReservationshost(json))
    // }, [navigate]);


      const pendingReservations = filterAndSortReservations(reservationshost, "pending");
      const confirmedReservations = filterAndSortReservations(reservationshost, "approved");
      const cancelledReservations = filterAndSortReservations(reservationshost, "cancelled");
      const deniedReservations = filterAndSortReservations(reservationshost, "denied");
      const expiredReservations = filterAndSortReservations(reservationshost, "expired");
      const terminatedReservations = filterAndSortReservations(reservationshost, "terminated");
      const completedReservations = filterAndSortReservations(reservationshost, "completed");

      function filterAndSortReservations(reservations, status, tabName) {
        return reservations
          .filter(reservation => reservation.status === status)
          .sort((a, b) => new Date(a.date) - new Date(b.date))
          .slice(
            (currentPage[tabName] - 1) * itemsPerPage,
            currentPage[tabName] * itemsPerPage,
          );
      }

      function renderPagination(tabName, totalItems, itemsPerPage, currentPage, setCurrentPage) {
        const totalPages = Math.ceil(totalItems / itemsPerPage);
        const items = [];
      
        for (let number = 1; number <= totalPages; number++) {
          items.push(
            <Pagination.Item
              key={number}
              active={number === currentPage[tabName]}
              onClick={() => setCurrentPage({ ...currentPage, [tabName]: number })}
            >
              {number}
            </Pagination.Item>,
          );
        }
      
        return (
          <Pagination>
            <Pagination.Prev
              onClick={() =>
                setCurrentPage(prev => ({
                  ...prev,
                  [tabName]: prev[tabName] > 1 ? prev[tabName] - 1 : prev[tabName],
                }))
              }
            />
            {items}
            <Pagination.Next
              onClick={() =>
                setCurrentPage(prev => ({
                  ...prev,
                  [tabName]: prev[tabName] < totalPages ? prev[tabName] + 1 : prev[tabName],
                }))
              }
            />
          </Pagination>
        );
      }
      

    return (
            <div className="container py-5">
              <div className="d-flex justify-content-between">
                <h1>My Reservations</h1>
                <div>
                  <p>Create New Properties!</p>
                  <div className="d-flex justify-content-center">
                    <a href="CreateProperty.html">
                      <button type="button" className="btn btn-warning btn-lg btn-floating">
                        <FontAwesomeIcon icon={faPlus} />
                      </button>
                    </a>
                  </div>
                </div>
              </div>
              <ul className="nav nav-tabs mb-3" id="myTab0" role="tablist">
                <li className="nav-item" role="presentation">
                  <button
                    className="nav-link"
                    id="home1"
                    data-mdb-toggle="tab"
                    data-mdb-target="#home0"
                    type="button"
                    role="tab"
                    aria-controls="home"
                    aria-selected="true"
                  >
                    pending
                  </button>
                </li>
                <li className="nav-item" role="presentation">
                  <button
                    className="nav-link"
                    id="home2"
                    data-mdb-toggle="tab"
                    data-mdb-target="#home0"
                    type="button"
                    role="tab"
                    aria-controls="home2"
                    aria-selected="false"
                  >
                    denied
                  </button>
                </li>
                <li className="nav-item" role="presentation">
                  <button
                    className="nav-link"
                    id="home3"
                    data-mdb-toggle="tab"
                    data-mdb-target="#home0"
                    type="button"
                    role="tab"
                    aria-controls="home3"
                    aria-selected="false"
                  >
                    expired
                  </button>
                </li>
                <li className="nav-item" role="presentation">
                  <button
                    className="nav-link"
                    id="home4"
                    data-mdb-toggle="tab"
                    data-mdb-target="#home0"
                    type="button"
                    role="tab"
                    aria-controls="home4"
                    aria-selected="false"
                  >
                    approved
                  </button>
                </li>
                <li className="nav-item" role="presentation">
                  <button
                    className="nav-link"
                    id="home5"
                    data-mdb-toggle="tab"
                    data-mdb-target="#profile0"
                    type="button"
                    role="tab"
                    aria-controls="home5"
                    aria-selected="false"
                  >
                    cancelled
                  </button>
                </li>
                <li className="nav-item" role="presentation">
                  <button
                    className="nav-link"
                    id="home6"
                    data-mdb-toggle="tab"
                    data-mdb-target="#profile0"
                    type="button"
                    role="tab"
                    aria-controls="home6"
                    aria-selected="false"
                  >
                    terminated
                  </button>
                </li>
                <li className="nav-item" role="presentation">
                  <button
                    className="nav-link"
                    id="home7"
                    data-mdb-toggle="tab"
                    data-mdb-target="#profile0"
                    type="button"
                    role="tab"
                    aria-controls="home7"
                    aria-selected="false"
                  >
                    completed
                  </button>
                </li>
              </ul>
              <div className="tab-content" id="myTabContent0">
                {/* <pending /> */}
                <div
                className="tab-pane fade show active"
                id="home1"
                role="tabpanel"
                aria-labelledby="home-tab0"
                >
                <section className="light">
                <div className="container py-2">
                {pendingReservations.map(reservation => <Reservation {...reservation} />)}
                {renderPagination("pending", pendingReservations.length, itemsPerPage, currentPage, setCurrentPage)}
                </div>
                </section>
                </div>
                {/* <denied /> */}
                <div className="tab-pane fade" id="profile0" role="tabpanel" aria-labelledby="home2">
                <section className="light">
                    <div className="container py-2">
                    {deniedReservations.map(reservation => <Reservation {...reservation} />)}
                    {renderPagination("denied",deniedReservations.length, itemsPerPage, currentPage, setCurrentPage)}
                    </div>
                </section>
                </div>
                <div className="tab-pane fade" id="profile2" role="tabpanel" aria-labelledby="home3">
                <section className="light">
                    <div className="container py-2">
                    {expiredReservations.map(reservation => <Reservation {...reservation} />)}
                    {renderPagination("expired",expiredReservations.length, itemsPerPage, currentPage, setCurrentPage)}
                    </div>
                </section>
                </div>
                <div className="tab-pane fade" id="profile3" role="tabpanel" aria-labelledby="home4">
                <section className="light">
                    <div className="container py-2">
                    {confirmedReservations.map(reservation => <Reservation {...reservation} />)}
                    {renderPagination("confirmed",confirmedReservations.length, itemsPerPage, currentPage, setCurrentPage)}
                    </div>
                </section>
                </div>
                <div className="tab-pane fade" id="profile4" role="tabpanel" aria-labelledby="home5">
                <section className="light">
                    <div className="container py-2">
                    {cancelledReservations.map(reservation => <Reservation {...reservation} />)}
                    {renderPagination("cancelled",cancelledReservations.length, itemsPerPage, currentPage, setCurrentPage)}
                    </div>
                </section>
                </div>
                <div className="tab-pane fade" id="profile5" role="tabpanel" aria-labelledby="home6">
                <section className="light">
                    <div className="container py-2">
                    {terminatedReservations.map(reservation => <Reservation {...reservation} />)}
                    {renderPagination("terminated",terminatedReservations.length, itemsPerPage, currentPage, setCurrentPage)}
                    </div>
                </section>
                </div>
                <div className="tab-pane fade" id="profile6" role="tabpanel" aria-labelledby="home7">
                <section className="light">
                    <div className="container py-2">
                    {completedReservations.map(reservation => <Reservation {...reservation} />)}
                    {renderPagination("completed", completedReservations.length, itemsPerPage, currentPage, setCurrentPage)}
                    </div>
                </section>
                </div>
              </div>
            </div>
          );
        };
    

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
  
  
  
export default ReservationsPageH;