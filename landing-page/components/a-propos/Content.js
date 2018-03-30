import React from "react";
import Link from "next/link";

export default class Content extends React.Component {
  render() {
    return (
      <div id="a-propos-content" className="container">
        <section className="section">
          <div
            className="content"
            dangerouslySetInnerHTML={{
              __html: this.props.data.contenu
            }}
          />
          <div>
            <div className="has-text-centered">
              <Link href="/#contact">
                <a className="button is-medium is-primary">Contactez-nous</a>
              </Link>
              {"  "}
              <Link href="/porteurs-aides#referencez-vous">
                <a className="button is-medium is-primary">
                  Référencer une aide
                </a>
              </Link>
            </div>
          </div>
        </section>

        <section className="section">
          <div>
            <h2 className="title is-2">Les prochaines étapes</h2>
            <div
              className="content"
              dangerouslySetInnerHTML={{
                __html: this.props.data.lesprochainesetapes
              }}
            />
          </div>
        </section>
      </div>
    );
  }
}
