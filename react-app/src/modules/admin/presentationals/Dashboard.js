import React, { Component } from "react";
import AideList from "../presentationals/AideList";
class Dashboard extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  render() {
    return (
      <div>
        <AideList />
      </div>
    );
  }
}

export default Dashboard;
