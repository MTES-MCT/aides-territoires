import React from "react";
import Layout from "modules/common/layouts/Layout";
import AideFormContainer from "modules/aide/decorators/AideFormContainer";

class AideFormPage extends React.Component {
  render() {
    return (
      <Layout>
        <div className="section container">
          <AideFormContainer />
        </div>
      </Layout>
    );
  }
}

export default AideFormPage;
