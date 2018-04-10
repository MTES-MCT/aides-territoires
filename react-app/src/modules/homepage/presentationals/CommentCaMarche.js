import React from "react";

export default class SectionCommentCaMarche extends React.Component {
  render() {
    return (
      <section id="comment-ca-marche" className="section">
        <div className="container ">
          <h2 className="section-title title is-3">
            {this.props.data.commentcamarchetitre}
          </h2>
          <div className="columns">
            <div className="column">
              <div className="numero">1</div>
              <h3 className="title is-4">
                {this.props.data.commentcamarchebloc1titre}
              </h3>
              <div
                dangerouslySetInnerHTML={{
                  __html: this.props.data.commentcamarchebloc1
                }}
              />
            </div>
            <div className="column">
              <div className="numero">2</div>
              <h3 className="title is-4">
                {this.props.data.commentcamarchebloc2titre}
              </h3>
              <div
                dangerouslySetInnerHTML={{
                  __html: this.props.data.commentcamarchebloc2
                }}
              />
            </div>
            <div className="column">
              <div className="numero">3</div>
              <h3 className="title is-4">
                {this.props.data.commentcamarchebloc3titre}
              </h3>
              <div
                dangerouslySetInnerHTML={{
                  __html: this.props.data.commentcamarchebloc3
                }}
              />
            </div>
          </div>
        </div>
      </section>
    );
  }
}
