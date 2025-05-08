
//------------------------------------------
// FONCTION TO SCROLL TO TOP IF CLICK ON "ABOUT"

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}





$(document).ready(function(){



  //Fonction test quand appuis sur entré
  document.body.onkeyup = function(e){
    if(e.key === 'Enter' || e.keyCode === 13){
        //alert("Space pressed!");
        console.log('hello world');
        window.location.href = "/";
    }
  }






  // When the user scrolls down 50px from the top of the document, resize the header
  window.onscroll = function() {scrollFunction()};
  function scrollFunction() {
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
      document.getElementById("header").style.height = "30px";
      document.getElementById("header-content").style.cssText = 'align-items: center;  height: 30px';//padding: 0;// margin:0';
      document.getElementById("header_left-content").style.height = "30px";
      document.getElementById("logo").style.cssText = "padding-left: 40rem; margin-left: -39rem;";
      document.getElementById("logo-text").style.fontSize = "2rem";
      //document.getElementById("logo-img2").style.cssText = "height: 45%; position: absolute; bottom: 2px; right:31px;";
      //document.getElementById("logo-img3").style.cssText = "height: 35%; position: absolute; bottom: 17px; right:34px;";
    } else {
      document.getElementById("header").style.height = "64px";
      document.getElementById("header-content").style.cssText = "align-items: flex-end; padding: 0 2.5rem; height: 43px; margin:0 auto";
      document.getElementById("header_left-content").style.height = "inherit";
      document.getElementById("logo").style.padding = "0 1rem";
      document.getElementById("logo").style.cssText = "padding: 0 1rem; margin-left: 0rem;";
      if ($(document).width() > 850) {
        document.getElementById("logo-text").style.fontSize = "2rem";
      }
      //document.getElementById("logo-img2").style.cssText = "height: 45%; position: absolute; bottom: 4px; right:17px;";
      //document.getElementById("logo-img3").style.cssText = "height: 35%; position: absolute; bottom: 25px; right:23px;";

    }
  }


  //--------------------------------------------------------
  // Get the modal
  var modal = document.getElementById("modal-root");

  // Get the image and insert it inside the modal - use its "alt" text as a caption
  var img = document.getElementById("myImg");
  var modalImg = document.getElementById("img01");
  var captionText = document.getElementById("caption");
  img.onclick = function(){
    modal.style.display = "block";
    modalImg.src = this.src;
  }

  // Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[0];

  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    modal.style.display = "none";
  }


  $(document).on('keyup',function(evt) {
    if (evt.keyCode == 27) {
      modal.style.display = "none";
    }
  });

  var modal = document.querySelector('#modal-root');
  modal.addEventListener('click', function(e) {
      modal.style.display = "none";
  }, false);

  modal.children[1].addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      e.stopImmediatePropagation();
  }, false);

//--------------------------------------------------------






  //------------------------------------------
  // FONCTION TO CHANGE CLASS OF THE NAV BAR TO ACTIVATE THE CORRECT SECTION

  function changeNavClass(nav_element) {
    document.getElementById("nav-about").className = "nav-icons";
    document.getElementById("nav-research").className = "nav-icons";
    document.getElementById("nav-publication").className = "nav-icons";
    document.getElementById("nav-conference").className = "nav-icons";
    document.getElementById("nav-teaching").className = "nav-icons";

    document.getElementById(nav_element).className += " active";

    document.getElementById("location_icon").className = "fas fa-map-marker-alt";
    document.getElementById("research_icon").className = "fa fa-flask fa-fw";
    document.getElementById('book_icon').src="assets/images/icons/book-1.png"
    document.getElementById("gear1").style.display = "none";
    document.getElementById("gear2").style.display = "none";

  }
  //------------------------------------------
  // FONCTION TO KNOW WHERE THE SCROLL BAR IS

  $(window).scroll(function() {
     var hTr = $('#research').offset().top,
         hTp = $('#publication').offset().top,
         hTc = $('#conference').offset().top,
         hTt = $('#teaching').offset().top,
         //hH = $('#research').outerHeight(),
         wH = $(window).height(),
         wS = $(this).scrollTop();
      //console.log(wS, hTt-wH/2, hTt, hTr);
      if (wS < hTr-wH/4){
        //console.log("about");
        changeNavClass("nav-about");
      }

      if (wS > (hTr-wH/4) && wS < (hTp-wH/4)){
        //console.log("research");
        changeNavClass("nav-research");
        document.getElementById("research_icon").className = "fa fa-flask fa-fw anim_bubble";
      }

      if (wS > (hTp-wH/4) && wS < (hTc-wH/4)){
        //console.log("publication")
        if (document.getElementById("book_icon").src.includes("book-gif")!=true){
          changeNavClass("nav-publication");
          document.getElementById('book_icon').src="assets/images/icons/book-gif.gif"
        }
      }

      if (wS > (hTc-wH/4) && wS < (hTt-wH/2)){
        //console.log("conf");
        changeNavClass("nav-conference");
        document.getElementById("location_icon").className = "fas fa-map-marker-alt bounce";
      }

      if (wS > hTt-wH/1.5){
        //console.log("teach");
        changeNavClass("nav-teaching");
        document.getElementById("gear1").style.display = "block";
        document.getElementById("gear2").style.display = "block";      }
  });








});
