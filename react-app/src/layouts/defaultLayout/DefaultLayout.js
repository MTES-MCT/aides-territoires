import React from "react";
import Navigation from "../../presentationals/navigation/Navigation";
import Header from "../../presentationals/header/Header";
import ImageTown from "../../presentationals/imageTown/ImageTown";

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
        {/*<Header />*/}
        <div style={styles.pageContent} className="page-content">
          {this.props.children}
        </div>
        <ImageTown />
      </div>
    );
  }
}

export default DefaultLayout;
