import React from "react";

const url = "/static/images/flat-design-town.png";

export default class extends React.Component {
  render() {
    // return <div style={style} className="image-town" />;
    return <img alt="quartier durable" src={url} className="image-town" />;
  }
}
