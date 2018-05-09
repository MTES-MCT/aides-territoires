import React, { Component } from "react";
import { Motion, spring } from "react-motion";
import PropTypes from "prop-types";

export default class SlideDown extends Component {
  state = {
    show: false
  };
  static propTypes = {
    show: PropTypes.bool.isRequired,
    maxHeight: PropTypes.number
  };
  static defaultProps = {
    maxHeight: 1000
  };
  render() {
    return (
      <Motion
        defaultStyle={{
          maxHeight: 0
        }}
        style={{
          maxHeight: spring(this.props.show ? this.props.maxHeight : 0)
        }}
      >
        {interpolatingStyle => {
          return (
            <div style={{ ...interpolatingStyle, overflow: "hidden" }}>
              {this.props.children}
            </div>
          );
        }}
      </Motion>
    );
  }
}
