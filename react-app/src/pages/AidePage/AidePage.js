import React from "react";
import DefaultLayout from "../../layouts/DefaultLayout/DefaultLayout";
import { Link } from "react-router-dom";
import RaisedButton from "material-ui/RaisedButton";

class ExamplePage extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    const aide = this.props.location.state.aide;
    console.log(aide);
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
