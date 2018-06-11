import React from "react";
import injectSheet from "react-jss";
import uiConfig from "../../ui.config";
import Link from "next/link";
import PropTypes from "prop-types";

const MemberType = PropTypes.shape({
  nom: PropTypes.string.isRequired,
  bio: PropTypes.string,
  photoUrl: PropTypes.string
});

/**
 * MemberLIST
 */
let MemberList = ({ classes, members, href }) => {
  return (
    <div className={classes.root}>
      {members.map(member => <Member key={member.nom} member={member} />)}
    </div>
  );
};
MemberList.propTypes = {
  member: PropTypes.arrayOf(MemberType)
};
MemberList = injectSheet({
  root: { display: "flex" },
  [uiConfig.breakpoints.smallScreen]: {
    root: {
      display: "block"
    }
  }
})(MemberList);

/**
 * Member
 */
let Member = ({ classes, member, href }) => {
  return (
    <div className={classes.root}>
      <img className={classes.photo} src={member.photoUrl} />
      <h4>{member.nom}</h4>
      <div className={classes.bio}>{member.bio}</div>
    </div>
  );
};
Member.propTypes = {
  member: MemberType
};
Member = injectSheet({
  root: { width: "300px", margin: "2rem" },
  photo: { width: "100%" },
  bio: { color: "#444" }
})(Member);

export default MemberList;
