import React from "react";

const loaderSize = "60px";

class PageLoader extends React.Component {
  render() {
    return (
      <div style={{ textAlign: "center" }}>
        <div
          style={{
            width: loaderSize,
            height: loaderSize,
            margin: "2rem auto"
          }}
          class="loader"
        />
        {this.props.children}
      </div>
    );
  }
}

export default PageLoader;
