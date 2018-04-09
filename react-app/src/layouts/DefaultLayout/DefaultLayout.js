import React from "react";
import Navigation from "../../presentationals/Navigation/Navigation";
import ImageTown from "../../presentationals/ImageTown/ImageTown";

class DefaultLayout extends React.Component {
  render() {
    return (
      <div>
        <Navigation />
        {this.props.children}
        <ImageTown />
      </div>
    );
  }
}

export default DefaultLayout;
