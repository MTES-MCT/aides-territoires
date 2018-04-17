import React from "react";
import Link from "next/link";

/**
 * Afficher un lien sous forme de bouton avec un loader
 * qui apparait au moment du clic.
 */
export default class ButtonLink extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoading: false
    };
  }
  handleClick = () => {
    this.setState({ isLoading: true });
  };
  // note : je met l'évènement sur un div wrapper
  // car le onClick n'est plus capturé par React à l'intérieur
  // de la balise "Link" de Next.js :-/
  render() {
    return (
      <div onClick={this.handleClick}>
        <Link {...this.props}>
          <div
            className={`button is-info ${
              this.state.isLoading ? "is-loading" : ""
            }`}
          >
            {this.props.children}
          </div>
        </Link>
      </div>
    );
  }
}
