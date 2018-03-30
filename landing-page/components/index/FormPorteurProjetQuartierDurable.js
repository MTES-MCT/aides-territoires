import React from "react";

export default class SendInBlueInscrivezVous extends React.Component {
  render() {
    return (
      <section id="inscription" className="section lancez-votre-recherche">
        <p className="text container">
          Nous travaillons dur pour créer ce nouveau service ! Il sera
          disponible pour les projets d’aménagement de quartiers durables au
          cours du 2ème trimestre 2018. Laissez nous votre contact pour faire
          partie des premiers utilisateurs :
        </p>
        <iframe
          width="100%"
          height="850"
          src="https://my.sendinblue.com/users/subscribe/js_id/35zg8/id/1"
          frameBorder="0"
          scrolling="auto"
          allowFullScreen
          style={{
            background: "transparent",
            display: "block",
            marginLeft: "auto",
            marginRight: "auto",
            maxWidth: "100%"
          }}
        />
      </section>
    );
  }
}
