import React from "react";
import Layout from "../../common/layouts/Layout";
import AideFormContainer from "../decorators/AideFormContainer";

class AideFormPage extends React.Component {
  render() {
    return (
      <Layout>
        <div>Je suis la page du formulaire d'aides </div>
        <AideFormContainer />
      </Layout>
    );
  }
}

export default AideFormPage;
