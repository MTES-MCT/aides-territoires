import React from "react";
import { Link } from "react-router-dom";
import injectSheet from "react-jss";
import classnames from "classnames";
const styles = {};

class Header extends React.Component {
  render() {
    return (
      <section id="aides-territoires" className="hero ">
        <header className={classnames("header")} id="aides-territoires">
          <div className="header-overlay ">
            <div className="hero-body ">
              <div className="container ">
                <h1 className="title">Un outil pour les collectivités</h1>
                <h2 className="subtitle ">
                  Identifiez en quelques clics toutes les aides disponibles sur
                  votre territoire pour vos projets d'aménagement durable.
                  <br />
                  <br />
                  Un service actuellement expérimenté pour les projets de
                  quartiers durables.
                </h2>
                <div className="button is-large is-primary">
                  <Link
                    className="button-lancez-la-recherche js-scrollTo "
                    to="/recherche"
                  >
                    Lancer la recherche
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </header>
      </section>
    );
  }
}

export default injectSheet(styles)(Header);
