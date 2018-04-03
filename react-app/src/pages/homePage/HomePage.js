import React from "react";
import DefaultLayout from "../../layouts/defaultLayout/DefaultLayout";

class HomePage extends React.Component {
  render() {
    return (
      <DefaultLayout>
        <div className="container">
          <section className="section">Page d'accueil</section>
        </div>
      </DefaultLayout>
    );
  }
}

export default HomePage;
