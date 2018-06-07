import React from "react";
const Modal = class extends React.PureComponent {
  state = {
    visible: false
  };
  constructor(props) {
    super(props);
  }

  render() {
    return <div className="Modal">{this.props.children}</div>;
  }
};

export default Modal;
