import React from "react";
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";
import Slide from "@material-ui/core/Slide";

class SearchResultsActionBar extends React.Component {
  state = {
    showModal: false
  };
  handleButtonClick = () => {
    this.setState({
      showModal: true
    });
  };
  render() {
    return (
      <div>
        <ActionsBarDialog
          show={this.state.showModal}
          handleClose={() => this.setState({ showModal: false })}
        />
        <Button variant="outlined" onClick={this.handleButtonClick}>
          Imprimer mes résultats
        </Button>
        <Button variant="outlined" onClick={this.handleButtonClick}>
          Partager mes résultats
        </Button>
        <Button variant="outlined" onClick={this.handleButtonClick}>
          Etre alerté de nouvelles aides
        </Button>
      </div>
    );
  }
}

function Transition(props) {
  return <Slide direction="up" {...props} />;
}

const ActionsBarDialog = ({ show, handleClose }) => {
  return (
    <Dialog
      open={show}
      TransitionComponent={Transition}
      keepMounted
      onClose={handleClose}
      aria-labelledby="alert-dialog-slide-title"
      aria-describedby="alert-dialog-slide-description"
    >
      <DialogTitle id="alert-dialog-slide-title">{""}</DialogTitle>
      <DialogContent>
        <DialogContentText id="alert-dialog-slide-description">
          Cette fonctionnalité sera bientôt disponible !
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} color="primary">
          D'accord !
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default SearchResultsActionBar;
