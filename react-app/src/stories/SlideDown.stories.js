import React from "react";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import SlideDown from "../components/ui/reactSpring/SlideDown";

const links = [
  {
    title: "Aide-territoires",
    to: "/"
  },
  {
    title: "Rechercher un aide",
    to: "/recherche"
  },
  {
    title: "Contact",
    to: "https://www.aides-territoires.beta.gouv.fr/#contact"
  }
];

storiesOf("reactSpring", module).add("SlideDown", () => {
  return class extends React.PureComponent {
    render() {
      return (
        <SlideDown
          maxHeight={100}
          show={this.state.activeFilters.formeDeDiffusion}
        >
          Hello slide down
        </SlideDown>
      );
    }
  };
});
