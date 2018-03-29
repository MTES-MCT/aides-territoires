import React from "react";
import DefaultLayout from "../components/common/DefaultLayout";
import Header from "../components/a-propos/Header";
import Content from "../components/a-propos/Content";
import Equipe from "../components/a-propos/Equipe";

class aProposPage extends React.Component {
  render() {
    return (
      <DefaultLayout>
        <Header />
        <Content />
        <Equipe />
      </DefaultLayout>
    );
  }
}

export default aProposPage;
