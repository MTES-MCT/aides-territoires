import React from "react";
import Layout from "../../common/layouts/Layout";
import AideFormContainer from "../decorators/AideFormContainer";

class AideFormPage extends React.Component {
  render() {
    return (
      <Layout>
        <div className="container">
          <AideFormContainer />
        </div>
      </Layout>
    );
  }
}

export default AideFormPage;
