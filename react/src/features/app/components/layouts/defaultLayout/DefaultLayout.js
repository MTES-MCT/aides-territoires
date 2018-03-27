import React from "react";
import Header from "../../presentationals/header/Header";

class DefaultLayout extends React.Component {
  render() {
    return (
      <div>
        <Header />
        <div className="page-content">{this.props.children}</div>
      </div>
    );
  }
}

export default DefaultLayout;
