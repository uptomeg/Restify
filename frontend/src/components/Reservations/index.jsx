import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCalendarAlt, faTag } from '@fortawesome/free-solid-svg-icons';

function Reservation(props) {
    const imageUrl = 'https://picsum.photos/1000/1000';
    return (
        <article className="postcard light blue">
          <a className="postcard__img_link" href="ReservationUser.html">
            <img className="postcard__img" src={imageUrl} alt="Image Title" />
          </a>
          <div className="postcard__text t-dark">
            <h1 className="postcard__title blue">
              <a href="#">{props.property.name}</a>
            </h1>
            <div className="postcard__subtitle small">
              <time dateTime={`${props.startDate} – ${props.endDate}`}>
                <FontAwesomeIcon icon={faCalendarAlt} className="mr-2" />
                {props.startDate} – {props.endDate}
              </time>
            </div>
            <div className="postcard__bar"></div>
            <div className="d-flex flex-row justify-content-between">
              <div className="postcard__preview-txt">{props.property.description}</div>
              <h3>{props.price}</h3>
            </div>
            <ul className="postcard__tagbox">
              <li className="tag__item">
                <FontAwesomeIcon icon={faTag} className="mr-2" />
                {props.status}
              </li>
            </ul>
          </div>
        </article>
      );
}
export default Reservation;
