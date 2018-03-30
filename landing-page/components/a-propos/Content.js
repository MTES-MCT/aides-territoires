import React from "react";
import Link from "next/link";

export default class Content extends React.Component {
  render() {
    return (
      <div id="a-propos-content" className="container">
        <section className="section">
          <div className="sous-section">
            <h2 className="title is-3">A l’origine d’Aides-territoires </h2>
            <p>
              L’aventure Aides-territoires part d’un constat, partagé à tous les
              niveaux : l’accès aux aides publiques (financement,
              accompagnement, distribuées « classiquement » ou par appels à
              projet) pour les projets d’aménagement du territoire est une
              véritable jungle en raison de la multiplicité des aides et des
              guichets qui les diffusent. Le simple fait de rester informé des
              nouvelles aides demande la mise en place d’une veille très
              chronophage, au détriment du temps passé sur le projet en
              lui-même. Cette difficulté est susceptible d’accentuer les
              inégalités entre les collectivités, et cela avant même d’entamer
              le processus de sélection et de candidature auxdites aides.
            </p>
          </div>
          <div className="sous-section">
            <h2 className="title is-3">
              Le service proposé par Aides-territoires
            </h2>
            <p>
              Nous voulons vous faciliter l’accès aux aides publiques
              pertinentes pour vos projets. Notre version pilote facilite
              l’identification des aides adaptées à vos projets de quartiers
              durables (comme c’est le cas par exemple des projets
              d’EcoQuartiers). Cette entrée par type de projet vous permet de
              gagner du temps avec des aides préqualifiées à toutes les étapes
              de votre projet, et quelles qu’en soient les caractéristiques.
              Pour vous assurer une sélection pertinente et la plus complète,
              nous sollicitons les experts de ces sujets. Le projet a commencé
              il y a 3 mois à peine, n’hésitez pas à nous contacter ou à nous
              remonter une aide qui ne serait pas référencée dans notre base !{" "}
            </p>
          </div>
          <div className="sous-section">
            <h2 className="title is-3">La base de données Aides-territoires</h2>
            <p>
              Aides-territoires fonctionne grâce à une base d’aides dynamique et
              mise à jour régulièrement. Nous mettons en place des partenariats
              avec les porteurs d’aides pour faciliter la diffusion des aides et
              la mise à jour de notre base. Vous voulez faire partie de nos
              partenaires ? Contactez-nous ! Vous portez une aide en particulier
              ou vous connaissez une aide qui n’est pas référencée ?
              Référencez-la  Si les critères proposés dans ce formulaire ne
              correspondent pas à votre aide, contactez-nous, d’autres projets
              arrivent. Aides-territoires est partenaire et partage sa base de
              données avec le site initié par la Direction Régionale de
              l’Environnement de l’Aménagement et du Logement (DREAL) Nouvelle
              Aquitaine et qui propose un accès thématique aux aides financières
              disponibles pour les projets des territoires.
            </p>
          </div>
          <div>
            <div className="has-text-centered">
              <Link href="/#contact">
                <a className="button is-medium is-primary">Contactez-nous</a>
              </Link>
              {"  "}
              <Link href="/porteurs-aides#referencez-vous">
                <a className="button is-medium is-primary">
                  Référencer une aide
                </a>
              </Link>
            </div>
          </div>
        </section>

        <hr />
        <section className="section">
          <div>
            <h2 className="title is-2">Les prochaines étapes</h2>
            <p>
              Une fois notre concept validé sur l’entrée pilote « quartier
              durable », nous ouvrirons l’outil à d’autres types de projets
              (thématiques, échelles différentes) Nous affinerons également le
              parcours « quartier durable » en fonction des retours de nos
              premiers utilisateurs, et travaillerons à la simplification des
              démarches pour les chefs de projet (Dites le nous une fois, )
            </p>
          </div>
        </section>
      </div>
    );
  }
}
