import React from "react";
import AdminLayout from "modules/admin/layouts/AdminLayout";
import AideFormContainer from "modules/aide/decorators/AideFormContainer";

class AideFormPage extends React.Component {
  render() {
    return (
      <AdminLayout>
        <h1 className="title is-1">Créer une aide</h1>
        <AideFormContainer />
      </AdminLayout>
    );
  }
}

export default AideFormPage;
