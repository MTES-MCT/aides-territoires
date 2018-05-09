import React, { Component } from "react";
import { Motion, spring } from "react-motion";
import PropTypes from "prop-types";

export default class SlideDown extends Component {
  state = {
    showDetails: false
  };
  static propTypes = {
    show: PropTypes.bool.isRequired,
    maxHeight: PropTypes.number
  };
  static defaultProps = {
    maxHeight: 1000
  };
  render() {
    console.log(this.props);
    return (
      <Motion
        defaultStyle={{
          overflow: "hidden",
          maxHeight: 0
        }}
        style={{
          overflow: "visible",
          maxHeight: spring(this.props.show ? this.props.maxHeight : 0)
        }}
      >
        {interpolatingStyle => {
          return <div style={interpolatingStyle}>{this.props.children}</div>;
        }}
      </Motion>
    );
  }
}
