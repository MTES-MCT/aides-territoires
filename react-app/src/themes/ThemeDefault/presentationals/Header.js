import React from "react";
import AppLoader from "../../../modules/generic/presentationals/AppLoader";
import { Link } from "react-router-dom";

export default class Header extends React.Component {
  render() {
    return (
      <section id="aides-territoires" className="hero ">
        <header className="header" id="aides-territoires">
          <div className="header-overlay ">
            <div className="hero-body ">
              <div className="container ">
                <h2 className="subtitle ">
                  <strong>
                    Identifiez en quelques clics toutes les aides disponibles
                    sur votre territoire pour vos projets d'aménagement durable.
                  </strong>
                </h2>
              </div>
            </div>
          </div>
        </header>
      </section>
    );
  }
}
