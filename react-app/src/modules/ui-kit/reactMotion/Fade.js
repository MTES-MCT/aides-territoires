import React, { Component } from "react";
import { Motion, spring } from "react-motion";
import PropTypes from "prop-types";

export default class Fade extends Component {
  state = {
    show: false
  };
  static propTypes = {
    show: PropTypes.bool.isRequired
  };
  render() {
    return (
      <Motion
        defaultStyle={{
          opacity: 0
        }}
        style={{
          opacity: spring(this.props.show ? 1 : 0)
        }}
      >
        {interpolatingStyle => {
          return <span style={interpolatingStyle}>{this.props.children}</span>;
        }}
      </Motion>
    );
  }
}
