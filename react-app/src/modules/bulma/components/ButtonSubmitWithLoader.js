import React from "react";
import Link from "next/link";
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
  // note : je met l'évènement sur un div wrapper
  // car le onClick n'est plus capturé par React à l'intérieur
  // de la balise "Link" de Next.js :-/
  render() {
    return (
      <button
        onClick={e => this.props.onClick(e)}
        type="submit"
        className={`button is-dark ${this.props.isLoading ? "is-loading" : ""}`}
      >
        {this.props.children}
      </button>
    );
  }
}
