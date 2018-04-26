import React from "react";
import Navigation from "modules/common/presentationals/Navigation";
import SideMenu from "../presentationals/SideMenu";
import "bulma/css/bulma.css";
import "./AdminLayout.css";

export default class DefaultLayout extends React.Component {
  render() {
    return (
      <div className="AdminLayout">
        <Navigation />
        <div className="columns">
          <div className="column column-menu is-3">
            <SideMenu />
          </div>
          <div className="column column-content is-9">
            {this.props.children}
          </div>
        </div>
      </div>
    );
  }
}
