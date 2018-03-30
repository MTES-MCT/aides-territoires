import React from "react";

export default class BulmaCard extends React.Component {
  render() {
    return (
      <div className="card" style={{ borderRadius: "5px" }}>
        <div className="card-image">
          <figure className="image">
            <img src={this.props.image} alt="Placeholder image" />
          </figure>
        </div>

        <div className="card-content">
          <div className="content">{this.props.children}</div>
        </div>
        {/*
        <footer className="card-footer">
          <a href="#" className="card-footer-item">
            Save
          </a>
          <a href="#" className="card-footer-item">
            Edit
          </a>
          <a href="#" className="card-footer-item">
            Delete
          </a>
        </footer>
        */}
      </div>
    );
  }
}
