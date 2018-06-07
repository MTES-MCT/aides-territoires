import React from "react";
import Navigation from "../ui/bulma/Navigation";
import "bulma/css/bulma.css";
import "bulma-tooltip/dist/bulma-tooltip.min.css";
import "./Layout.css";
import withConfig from "../decorators/withConfig";
import LogoAidesTerritoires from "../ui/brand/LogoAidesTerritoires";

const DefaultLayout = class extends React.PureComponent {
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
        <Navigation links={this.props.config.navigationLinks} />
        {this.props.children}
      </div>
    );
  }
};

export default withConfig(DefaultLayout);
