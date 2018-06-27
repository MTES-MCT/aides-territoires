import React from "react";
import AdminLayout from "../layouts/AdminLayout";
import AdminAideForm from "../admin/AdminAideForm";

class AideFormPage extends React.Component {
  render() {
    // le bouton "cloner" peut nous envoyer une aide dans le state du routeur
    const aideToClone =
      this.props.location.state && this.props.location.state.aide
        ? this.props.location.state.aide
        : null;
    return (
      <AdminLayout>
        <h1 className="title is-1">Créer une aide</h1>
        <AdminAideForm
          cloning={aideToClone ? true : false}
          aide={aideToClone}
          operation={"creation"}
        />
      </AdminLayout>
    );
  }
}

export default AideFormPage;
