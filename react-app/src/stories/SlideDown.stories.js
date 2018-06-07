import React from "react";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import SlideDown from "../components/ui/reactSpring/SlideDown";
import { purple200 } from "material-ui/styles/colors";
import { withInfo } from "@storybook/addon-info";

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

storiesOf("reactSpring", module).add(
  "SlideDown",
  withInfo()(() => (
    <div>
      <SlideDown
        maxHeight={400}
        show={() => {
          setTimeout(() => {
            return true;
          }, 3000);
          return false;
        }}
      >
        <div style={{ height: "400px", background: purple200 }}>Sliding</div>
      </SlideDown>
    </div>
  ))
);
