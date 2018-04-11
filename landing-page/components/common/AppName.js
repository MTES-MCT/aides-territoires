import React, { Component } from "react";

const styles = (
  <style jsx>{`
    .part-1 {
      font-weight: normal;
    }
    .part-2 {
      font-weight: bold;
    }
    .part-3 {
      font-style: italic;
    }
  `}</style>
);

class AppName extends Component {
  render() {
    return (
      <div className="app-name">
        <span className="part-1">Aides-territoires.</span>
        <span className="part-2">
          beta.gouv
        </span>.<span className="part-3">fr</span>
        {styles}
      </div>
    );
  }
}

export default AppName;
