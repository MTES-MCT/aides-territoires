import React from "react";
import AppNavigation from "../ui/AppNavigation";
import "bulma/css/bulma.css";
import "bulma-tooltip/dist/bulma-tooltip.min.css";
import "./Layout.css";

export default class DefaultLayout extends React.PureComponent {
  render() {
    return (
      <div className="default-layout">
        {/*
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
        </Head>
        */}
        <AppNavigation />
        {this.props.children}
      </div>
    );
  }
}
