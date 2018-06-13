import React from "react";
import PropTypes from "prop-types";

/**
 * Afficher un lien sous forme de bouton avec un loader
 * qui apparait au moment du clic.
 */
export default class ButtonSubmitWithLoader extends React.Component {
  static propTypes = {
    isLoading: PropTypes.bool.isRequired,
    onClick: PropTypes.func
  };

  render() {
    const { isLoading, ...props } = this.props;

    return (
      <button
        type="submit"
        className={`button is-info ${isLoading ? "is-loading" : ""}`}
        {...props}
      />
    );
  }
}
