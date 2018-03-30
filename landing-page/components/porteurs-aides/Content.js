import React from "react";

export default class Content extends React.Component {
  render() {
    return (
      <section id="description" className="section">
        <div className="container">
          <div className="text">
            <div
              dangerouslySetInnerHTML={{
                __html: this.props.data.textebloc1
              }}
            />
            <br />
          </div>
          <div className="has-text-centered">
            <a
              href="https://goo.gl/forms/lVd7CcukMQU7Ral82"
              className="button is-primary is-large"
            >
              Référencez vos aides compatibles
            </a>
          </div>
          <br />
          <br />
          <div
            className="content text"
            dangerouslySetInnerHTML={{
              __html: this.props.data.textebloc2
            }}
          />
        </div>
      </section>
    );
  }
}
