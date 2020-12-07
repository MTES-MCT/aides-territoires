let logosIndex = 0;
showLogos();

function showLogos() {
  let i;
  let logo1 = document.getElementsByClassName("logo1");
  let logo2 = document.getElementsByClassName("logo2");
  let logo3 = document.getElementsByClassName("logo3");
  
  for (i = 0; i < logo1.length; i++) {
	logo1[i].className = logo1[i].className.replace("active", "hidden");
	logo2[i].className = logo2[i].className.replace("active", "hidden"); 
	logo3[i].className = logo3[i].className.replace("active", "hidden");
  }

  logosIndex++;
  if (logosIndex > logo1.length) {
	  logosIndex = 1
	}    
	logo1[logosIndex-1].className = logo1[logosIndex-1].className.replace("hidden", "active");  
	logo2[logosIndex-1].className = logo2[logosIndex-1].className.replace("hidden", "active");
	logo3[logosIndex-1].className = logo3[logosIndex-1].className.replace("hidden", "active"); 

  setTimeout(showLogos, 2500);
}