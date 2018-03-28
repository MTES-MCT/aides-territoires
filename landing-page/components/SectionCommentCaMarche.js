import React from "react";

export default class SectionCommentCaMarche extends React.Component {
  render() {
    return (
      <section id="comment-ca-marche" className="section">
        <div className="container ">
          <h2 className="section-title title is-3">Comment ça marche ?</h2>
          <div className="columns">
            <div className="column">
              <div className="numero">1</div>
              <h3 className="title is-4">Un territoire, un projet</h3>
              <p>Donnez nous votre localisation et votre projet </p>
            </div>
            <div className="column">
              <div className="numero">2</div>
              <h3 className="title is-4">Des aides</h3>
              <p>
                Nous vous aidons à identifier les meilleures aides publiques
                mobilisables
              </p>
            </div>
            <div className="column">
              <div className="numero">3</div>
              <h3 className="title is-4">Du temps gagné</h3>
              <p>
                passez plus de temps sur votre projet en activant les aides
                pertinentes au bon moment
              </p>
            </div>
          </div>
        </div>
      </section>
    );
  }
}
