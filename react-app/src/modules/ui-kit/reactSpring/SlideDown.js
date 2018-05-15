import React from "react";
import { Spring, animated } from "react-spring";
import PropTypes from "prop-types";

export default class SlideDown extends React.Component {
  static defaultProps = {
    maxHeight: 500,
    show: false
  };
  static propTypes = {
    maxHeight: PropTypes.number,
    show: PropTypes.bool
  };
  render() {
    return (
      <Spring
        native
        from={{ maxHeight: 0, overflow: "hidden" }}
        to={{
          maxHeight: this.props.show ? this.props.maxHeight : 0
        }}
      >
        {styles => (
          <animated.div style={styles}>{this.props.children}</animated.div>
        )}
      </Spring>
    );
  }
}
