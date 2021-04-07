// init
const logoIdList = ["logo1", "logo2", "logo3", "logo4", "logo5"];
let carousel = {};
let currentIndex = 0;
showLogos();

/**
 * Display up to 5 backer logos at the same time
 * Replace them every 4 seconds
 */
function showLogos() {
  logoIdList.forEach((logoId, index) => {
    carousel[logoId] = document.getElementsByClassName(logoId);

    // first hide all the logos
    for (i = 0; i < carousel[logoId].length; i++) {
      if (carousel[logoId][i]) {
        carousel[logoId][i].className = carousel[logoId][i].className.replace("active", "hidden");
      }
    }
    // then show only the logos from the currentIndex
    if (carousel[logoId][currentIndex]) {
      carousel[logoId][currentIndex].className = carousel[logoId][currentIndex].className.replace("hidden", "active");
    }
  });

  // increment currentIndex or go back to 0
  currentIndex = (currentIndex === carousel[logoIdList[0]].length - 1) ? 0 : currentIndex + 1;

  // run every 4 seconds
  setTimeout(showLogos, 4000);
}
