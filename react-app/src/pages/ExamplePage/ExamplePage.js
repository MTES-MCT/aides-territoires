import React from "react";
import DefaultLayout from "../../layouts/DefaultLayout/DefaultLayout";
import { Link } from "react-router-dom";
import RaisedButton from "material-ui/RaisedButton";

class ExamplePage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  render() {
    return (
      <DefaultLayout>
        <div className="container">
          <section className="section">Hello </section>
        </div>
      </DefaultLayout>
    );
  }
}

export default ExamplePage;
