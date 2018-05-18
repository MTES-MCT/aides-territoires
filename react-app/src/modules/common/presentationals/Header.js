import React from "react";
import { Link } from "react-router-dom";
import injectSheet from "react-jss";
import classnames from "classnames";
import graphcms from "services/graphcms";
const styles = {};

class Header extends React.Component {
  state = {
    title: "",
    content: ""
  };
  async componentDidMount() {
    const data = await graphcms.request(`{
      Pagedaccueil(id:"cjfdxk4tpcy3v016424h68se6") {
        headertitre
        header
      }
    }
    `);
    this.setState({
      title: data.Pagedaccueil.headertitre,
      content: data.Pagedaccueil.header
    });
  }
  render() {
    return (
      <section id="aides-territoires" className="hero ">
        <header className={classnames("header")} id="aides-territoires">
          <div className="header-overlay ">
            <div className="hero-body ">
              <div className="container ">
                <h1 className="title">{this.state.title}</h1>
                <h2
                  className="subtitle"
                  dangerouslySetInnerHTML={{ __html: this.state.content }}
                />
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
