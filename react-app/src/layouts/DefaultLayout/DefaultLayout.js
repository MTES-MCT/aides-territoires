import React from "react";
import Navigation from "../../presentationals/Navigation/Navigation";
import Header from "../../presentationals/Header/Header";
import ImageTown from "../../presentationals/ImageTown/ImageTown";

const styles = {
  pageContent: {
    paddingTop: "50px"
  }
};

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
