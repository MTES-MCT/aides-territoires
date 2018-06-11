import React from "react";
import Navigation from "./Navigation";
import Head from "next/head";
import injectSheet from "react-jss";
import { meta } from "../../content/_config.md";

const Layout = ({ children }) => {
  return (
    <div>
      <Head>
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
        <link rel="icon" type="image/png" href="/static/images/favicon.png" />
        <link rel="stylesheet" href="/static/css/global.css" />
      </Head>
      {<Navigation links={meta.navigationLinks} />}
      {children}
    </div>
  );
};

const styles = {
  "@global": {
    border: "solid red 1px"
  }
};

export default injectSheet(styles)(Layout);
