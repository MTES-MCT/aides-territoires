import React from "react";
import DefaultLayout from "../../layouts/DefaultLayout/DefaultLayout";

class ExamplePage extends React.Component {
  render() {
    const aide = this.props.location.state.aide;
    return (
      <DefaultLayout>
        <div className="container">
          <h1 className="title is-1">{aide.intitulé}</h1>
          <section className="section"> </section>
        </div>
      </DefaultLayout>
    );
  }
}

export default ExamplePage;
