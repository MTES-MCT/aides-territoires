import React from "react";
import BulmaCard from "../common/BulmaCard";

export default class Equipe extends React.Component {
  render() {
    return (
      <div id="equipe" className="section container">
        <h2 className="title is-2">{this.props.data.titredublocequipe}</h2>
        <div
          className="content"
          dangerouslySetInnerHTML={{
            __html: this.props.data.textedublocequipe
          }}
        />
        <br />
        <div className="columns">
          <div className="column">
            <BulmaCard image={"/static/images/elise.jpeg"}>
              <div
                className="content"
                dangerouslySetInnerHTML={{
                  __html: this.props.data.presentationElise
                }}
              />
            </BulmaCard>
          </div>
          <div className="column">
            <BulmaCard image={"/static/images/yann.jpeg"}>
              <div
                className="content"
                dangerouslySetInnerHTML={{
                  __html: this.props.data.presentationYann
                }}
              />
            </BulmaCard>
          </div>
          <div className="column">
            <BulmaCard image={"/static/images/roxane.jpg"}>
              <div
                className="content"
                dangerouslySetInnerHTML={{
                  __html: this.props.data.presentationRoxane
                }}
              />
            </BulmaCard>
          </div>
        </div>
      </div>
    );
  }
}
