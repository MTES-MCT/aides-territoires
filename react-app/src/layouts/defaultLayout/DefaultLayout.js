import React from "react";
import Navigation from "../../presentationals/navigation/Navigation";
import Header from "../../presentationals/header/Header";
import ImageTown from "../../presentationals/imageTown/ImageTown";
import { Step, Stepper, StepLabel } from "material-ui/Stepper";

const styles = {
  pageContent: {
    paddingTop: "50px"
  }
};

class DefaultLayout extends React.Component {
  render() {
    return (
      <div>
        <Navigation />
        {/*<Header />*/}
        <div className="container section">
          <Stepper activeStep={1}>
            <Step>
              <StepLabel>Territoire</StepLabel>
            </Step>
            <Step>
              <StepLabel>Phase du projet</StepLabel>
            </Step>
            <Step>
              <StepLabel>thématiques</StepLabel>
            </Step>
          </Stepper>
        </div>
        <div style={styles.pageContent} className="page-content">
          {this.props.children}
        </div>
        <ImageTown />
      </div>
    );
  }
}

export default DefaultLayout;
