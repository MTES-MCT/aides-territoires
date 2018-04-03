import React from "react";
import Navigation from "../../presentationals/navigation/Navigation";
import Header from "../../presentationals/header/Header";

class DefaultLayout extends React.Component {
  render() {
    return (
      <div>
        <Navigation />
        <Header />
        <div className="page-content">{this.props.children}</div>
      </div>
    );
  }
}

export default DefaultLayout;
