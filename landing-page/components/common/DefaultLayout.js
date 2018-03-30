import React from "react";
import Navigation from "./Navigation";
import Head from "next/head";

export default class DefaultLayout extends React.Component {
  render() {
    return (
      <div className="default-layout">
        <Head>
          <meta
            name="viewport"
            content="initial-scale=1.0, width=device-width"
          />
          <link
            rel="icon"
            type="image/png"
            href="/static/images/logobeta.png"
          />
          <link rel="stylesheet" href="/static/css/bulma.css" />
          <link rel="stylesheet" href="/static/css/style.css" />
        </Head>
        <Navigation />
        {this.props.children}
      </div>
    );
  }
}
