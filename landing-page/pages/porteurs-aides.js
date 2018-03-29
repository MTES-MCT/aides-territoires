import React from "react";
import DefaultLayout from "../components/common/DefaultLayout";
import Header from "../components/porteurs-aides/Header";
import Content from "../components/porteurs-aides/Content";
import FormPorteurProjetToutType from "../components/porteurs-aides/FormPorteurProjetToutType";

class porteurAidePage extends React.Component {
  render() {
    return (
      <DefaultLayout>
        <Header />
        <Content />
        <FormPorteurProjetToutType />
      </DefaultLayout>
    );
  }
}

export default porteurAidePage;
