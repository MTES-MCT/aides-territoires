import React from "react";
import DefaultLayout from "../../layouts/DefaultLayout/DefaultLayout";
import { Link } from "react-router-dom";
import RaisedButton from "material-ui/RaisedButton";
import Avatar from "material-ui/Avatar";
import Chip from "material-ui/Chip";
import SvgIconFace from "material-ui/svg-icons/action/face";
import { blue300, indigo900 } from "material-ui/styles/colors";

const styles = {
  chip: {
    margin: 4
  },
  wrapper: {
    display: "flex",
    flexWrap: "wrap"
  }
};

function handleRequestDelete() {
  // alert("You clicked the delete button.");
}

function handleClick() {
  // alert("You clicked the Chip.");
}

class ParcoursCriteres extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      results: ""
    };
  }
  render() {
    return (
      <DefaultLayout>
        <div className="container">
          <section className="section has-text-centered">
            <h2 className="title is-2">Critères</h2>
            <div style={styles.wrapper}>
              <Chip
                onRequestDelete={handleRequestDelete}
                onClick={handleClick}
                style={styles.chip}
              >
                Quartier durable
              </Chip>

              <Chip
                onRequestDelete={handleRequestDelete}
                onClick={handleClick}
                style={styles.chip}
              >
                <Avatar color="#444" icon={<SvgIconFace />} />
                Critère 2
              </Chip>

              <Chip onClick={handleClick} style={styles.chip}>
                <Avatar size={32}>A</Avatar>
                Critère 3
              </Chip>

              <Chip
                backgroundColor={blue300}
                onRequestDelete={handleRequestDelete}
                onClick={handleClick}
                style={styles.chip}
              >
                <Avatar size={32} color={blue300} backgroundColor={indigo900}>
                  new
                </Avatar>
                Critère 4
              </Chip>
            </div>
          </section>
          <div className="has-text-centered">
            <Link to="/parcours/phase">
              <RaisedButton label="Continuer" primary={true} />
            </Link>
          </div>
        </div>
      </DefaultLayout>
    );
  }
}

export default ParcoursCriteres;
