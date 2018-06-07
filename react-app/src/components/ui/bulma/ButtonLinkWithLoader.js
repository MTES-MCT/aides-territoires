import React from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";

/**
 * Afficher un lien sous forme de bouton avec un loader
 * qui apparait au moment du clic.
 */
export default class ButtonLink extends React.Component {
  static propTypes = {
    to: PropTypes.string.isRequired
  };
  constructor(props) {
    super(props);
    this.state = {
      isLoading: false
    };
  }
  handleClick = () => {
    this.setState({ isLoading: true });
  };
  render() {
    return (
      <Link {...this.props} onClick={this.handleClick}>
        <div
          className={`button is-info ${
            this.state.isLoading ? "is-loading" : ""
          }`}
        >
          {this.props.children}
        </div>
      </Link>
    );
  }
}
