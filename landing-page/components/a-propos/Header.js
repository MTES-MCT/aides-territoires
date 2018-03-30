import React from "react";

export default class Header extends React.Component {
  render() {
    return (
      <section id="aides-territoires" className="hero ">
        <header className="header ">
          <div className="header-overlay ">
            <div className="hero-body ">
              <div className="container ">
                <h1 className="title ">{this.props.data.titredansleheader}</h1>
                <h2 className="subtitle ">
                  <div
                    dangerouslySetInnerHTML={{
                      __html: this.props.data.texteduheader
                    }}
                  />
                </h2>
              </div>
            </div>
          </div>
        </header>
      </section>
    );
  }
}
